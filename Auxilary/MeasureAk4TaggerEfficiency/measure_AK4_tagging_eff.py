import numpy as np
import matplotlib.pyplot as plt
import gzip
import ROOT
import json
from argparse import ArgumentParser

parser=ArgumentParser()
parser.add_argument('-d', type=str, dest='dataset',action='store', required=True)
parser.add_argument('-y', type=str, dest='year',action='store', required=True)
args = parser.parse_args()
dataset = args.dataset
year = args.year
'''
if year == "2022":
    corr_year = "2022_Summer22"
    key = "particleNet_comb" 
if year == "2022EE":
    corr_year = "2022_Summer22EE"
    key = "particleNet_comb" 
if year == "2023":
    corr_year = "2023_Summer23"
    key = "particleNet_comb" 
if year == "2023BPix":
    corr_year = "2023_Summer23BPix"
    key = "particleNet_comb" 
if year == "2024":
    corr_year = "2024_Summer24"
    key = "UParTAK4_kinfit"
SF_file = f"/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/{corr_year}/btagging.json.gz"
if year == "2024":
   SF_file = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/2024_Summer24/btagging_preliminary.json.gz" 
with gzip.open(SF_file, "rt") as f:
    SF = json.load(f)
for sf in SF["corrections"]:
    if sf["name"] == key:
        for ssf in sf["data"]:
            print(ssf)



f_name = f"{year}_{dataset}.root"
f_name = "test.root"
'''
with open("../../outputList/output_btagging_2p1_BDT.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        if year + "_" in line and dataset + "_" in line and "Template" not in line:
            f_name = line.strip()
            break
print(f"processing: {year} {dataset} {f_name}")
#exit()
wps = [0, 1, 2, 3, 4, 5]
flavors = [0, 4, 5]
pts = [20.0, 30.0, 50.0, 70.0, 100.0, 140.0, 200.0, 300.0, 600.0, 1000.0]
#pts = [20, 50.0,  100.0, 200.0, 300.0, 600.0, 1000.0, 2000.0]
pts = [20.0, 30.0, 50.0, 70.0, 100.0, 140.0, 200.0, 300.0, 600.0, 1000.0]
absetas = [0, 0.8, 2.4]
N_all = {}
N_tagged = {}
for wp in wps:
    N_all[wp] = {}
    N_tagged[wp] = {}
    for flavor in flavors:
        N_all[wp][flavor] = {}
        N_tagged[wp][flavor] = {}
        for pt in pts:
            N_all[wp][flavor][pt] = {}
            N_tagged[wp][flavor][pt] = {}
            for abseta in absetas:
                N_all[wp][flavor][pt][abseta] = 0
                N_tagged[wp][flavor][pt][abseta] = 0

f = ROOT.TFile.Open(f_name, "READ")
tree = f.Get("Events")
Nprocessed = 0
for entry in tree:
    if entry.MX < 200 or entry.MY < 200:
        continue
    Jet_etas = entry.Jet_eta
    Jet_pts = entry.Jet_pt_nom
    Jet_flavors = entry.Jet_hadronFlavour
    Jet_score_discretes = entry.Jet_tagger_discrete
    for i in range(len(Jet_etas)):
        Nprocessed += 1
        jet_flavor = Jet_flavors[i]
        jet_score_discrete = Jet_score_discretes[i]
        jet_abseta = abs(Jet_etas[i])
        jet_pt = Jet_pts[i]
        if jet_score_discrete == -1 or jet_abseta > 2.4:
            continue
        for _abseta_l in absetas:
            if jet_abseta > _abseta_l:
                abseta_l = _abseta_l
        for _pt_l in pts:
            if jet_pt > _pt_l:
                pt_l = _pt_l
        #print(jet_flavor, jet_score_discrete, jet_abseta, jet_pt)
        for wp in wps:
            if wp <= jet_score_discrete:
                tagged = 1
            else: 
                tagged = 0
            N_all[wp][jet_flavor][pt_l][abseta_l] += 1
            N_tagged[wp][jet_flavor][pt_l][abseta_l] += tagged
            
#print(Nprocessed)
#print(N_all)

eff = {}
for wp in wps:
    eff[wp] = {}
    for flavor in flavors:
        eff[wp][flavor] = {}
        for i in range(len(pts) - 1):
            pt_low = pts[i]
            pt_up = pts[i+1]
            eff[wp][flavor][f"{pt_low}_{pt_up}"] = {}
            for j in range(len(absetas) - 1):
                abseta_low = absetas[j]
                abseta_up = absetas[j+1]
                if N_all[wp][flavor][pt_low][abseta_low] > 0:
                    eff[wp][flavor][f"{pt_low}_{pt_up}"][f"{abseta_low}_{abseta_up}"] = N_tagged[wp][flavor][pt_low][abseta_low]/ N_all[wp][flavor][pt_low][abseta_low]
                else:
                    eff[wp][flavor][f"{pt_low}_{pt_up}"][f"{abseta_low}_{abseta_up}"] = 1

with open(f"btagging_effs/{year}_{dataset}_AK4_btagging_eff.txt", "w") as f:
    json.dump(eff, f, indent = 4)

with open(f"btagging_effs/N_{year}_{dataset}_AK4_btagging_eff.txt", "w") as f:
    json.dump(N_all, f, indent = 4)

wp_map = {0:"0", 1:"L", 2:"M", 3:"T", 4:"XT", 5:"XXT"}
flavor_map = {0:"u/d/s/g", 4: "c", 5: "b"}
for wp in wps:
    for flavor in flavors:
        zpos = np.zeros((len(absetas) - 1, len(pts) - 1))
        for i in range(len(pts) - 1):
            pt_low = pts[i]
            for j in range(len(absetas) - 1):
                abseta_low = absetas[j]
                if N_all[wp][flavor][pt_low][abseta_low] > 0:
                    zpos[j,i] = N_tagged[wp][flavor][pt_low][abseta_low]/ N_all[wp][flavor][pt_low][abseta_low]
                else:
                    zpos[j,i] = np.nan
        
        fig, ax = plt.subplots()
        mesh = ax.pcolormesh(pts, absetas, zpos, cmap='viridis', shading='auto', vmin = 0, vmax = 1)
        
        # Label each cell at its center
        for i in range(zpos.shape[0]):
            for j in range(zpos.shape[1]):
                if not np.isnan(zpos[i, j]):
                    ax.text(pts[j] + 0.5 * (pts[j + 1] - pts[j]),
                        absetas[i] + 0.5 * (absetas[i + 1] - absetas[i]),
                        f"{zpos[i, j]:.2f}",
                        ha='center', va='center', color='black', fontsize=6)

        ax.set_xlabel('Jet_pt (GeV)')
        ax.set_ylabel('abs(Jet_eta)')
        ax.set_title(f"WP = {wp_map[wp]}, flavor = {flavor_map[flavor]}, AK4 b tagging efficiency")
        plt.colorbar(mesh, ax=ax)
        plt.savefig(f"btagging_plots/btagging_eff_2d_{year}_{dataset}_wp{wp}_favor{flavor}.png")

#print(eff)
