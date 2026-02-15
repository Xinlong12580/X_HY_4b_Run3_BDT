import ROOT
import json
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-m', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()
mode = args.mode
f = ROOT.TFile.Open(f"TEffs_{mode}.root", "READ")
years = ["2022", "2022EE", "2023", "2023BPix"]
processes = ["JetMET", "TTto4Q"]
Effs = {}
for year in years:
    Effs[year] = {}
        
for key in f.GetListOfKeys():
    Eff = key.ReadObj()
    for year in years:
        for process in processes:
            if (year + "_") in str(key) and process in  str(key):
                Effs[year][process] = Eff
nbins_x = Effs["2022"]["JetMET"].GetTotalHistogram().GetNbinsX()
nbins_y = Effs["2022"]["JetMET"].GetTotalHistogram().GetNbinsY() 
nbins_teff = (nbins_x + 2) * (nbins_y + 2)
print(nbins_x, nbins_y, nbins_teff)

print(Effs)
SFs = {}
SF_ups = {}
SF_downs = {}
for year in years:
    SFs[year] = []
    SF_ups[year] = []
    SF_downs[year] = []
    for i in range(nbins_teff):
        eff_data = Effs[year]["JetMET"].GetEfficiency(i)
        eff_data_low = eff_data - Effs[year]["JetMET"].GetEfficiencyErrorLow(i)
        eff_data_up = eff_data + Effs[year]["JetMET"].GetEfficiencyErrorUp(i)
        print(eff_data, eff_data_low, eff_data_up)
        eff_ttto4q = Effs[year]["TTto4Q"].GetEfficiency(i)
        eff_ttto4q_low = eff_ttto4q - Effs[year]["TTto4Q"].GetEfficiencyErrorLow(i)
        eff_ttto4q_up = eff_ttto4q + Effs[year]["TTto4Q"].GetEfficiencyErrorUp(i)
        if (eff_data != 0) and (eff_ttto4q != 0):
            sf = eff_data / eff_ttto4q
            sf_up = eff_data_up / eff_ttto4q_low
            sf_down = eff_data_low / eff_ttto4q_up
        else:
            sf = 1.
            sf_up = 1.
            sf_down = 1.
        SFs[year].append(sf) 
        SF_ups[year].append(sf_up) 
        SF_downs[year].append(sf_down)
    #print(year) 
    #print(SFs[year])
    #print(SF_ups[year])
    #print(SF_downs[year])

h = Effs["2022"]["JetMET"].GetPassedHistogram()
bins_x = [h.GetXaxis().GetBinLowEdge(i) for i in range(1, nbins_x +1) ]
bins_y = [h.GetYaxis().GetBinLowEdge(i) for i in range(1, nbins_y+1) ]
bins_x.append(h.GetXaxis().GetBinUpEdge(nbins_x))
bins_y.append(h.GetYaxis().GetBinUpEdge(nbins_y))
SFs_dict = {}
for year in years:
    zpos = np.zeros((nbins_y, nbins_x)) 
    SFs_dict[year] = {}
    SFs_dict[year] = {}
    for i in range(1, nbins_x + 1):
        for j in range(1, nbins_y + 1):
            #print(i, j)
            pt_low =  h.GetXaxis().GetBinLowEdge(i) 
            pt_up =  h.GetXaxis().GetBinUpEdge(i)
            mx_low = h.GetYaxis().GetBinLowEdge(j) 
            mx_up = h.GetYaxis().GetBinUpEdge(j) 
            ibin = Effs["2022"]["JetMET"].GetGlobalBin(i, j)
            pt_string = f"{pt_low}_{pt_up}"
            mx_string = f"{mx_low}_{mx_up}" 
            SFs_dict[year].setdefault(pt_string, {})
            #if pt_string not in SFs_dict[year]["TTto4Q"]:
            #    SFs_dict[year]["TTto4Q"][pt_string] = {}
            SFs_dict[year][pt_string][mx_string] = {}
            SFs_dict[year][pt_string][mx_string]["nom"] = SFs[year][ibin]
            SFs_dict[year][pt_string][mx_string]["up"] = SF_ups[year][ibin]
            SFs_dict[year][pt_string][mx_string]["down"] = SF_downs[year][ibin]
            #print(pt_low, pt_up, mx_low, mx_up, SFs[year][ibin])
            zpos[j - 1][i - 1] = SFs[year][ibin]
    fig, ax = plt.subplots()
    print(len(bins_x), len(bins_y), zpos.shape)
    mesh = ax.pcolormesh(bins_x, bins_y, zpos, cmap='viridis', shading='auto')

    # Label each cell at its center
    for i in range(zpos.shape[0]):
        for j in range(zpos.shape[1]):
            ax.text(bins_x[j] + 0.5 * (bins_x[j + 1] - bins_x[j]),
                bins_y[i] + 0.5 * (bins_y[i + 1] - bins_y[i]),
                f"{zpos[i, j]:.2f}",
                ha='center', va='center', color='black', fontsize=6)

    ax.set_xlabel('leading FatJet Pt (GeV)')
    ax.set_ylabel('MX (GeV)')
    plt.colorbar(mesh, ax=ax)
    plt.savefig(f"trigger_SF_2d_{year}_{mode}.png")

with open(f"trigger_{mode}_SFs.json", "w") as f:
    json.dump(SFs_dict, f, indent=4)
'''
h = Effs["2022"]["JetMET"].GetPassedHistogram()
SFs_dict = {}
for year in years:
    SFs_dict[year] = {}
    SFs_dict[year]["TTto4Q"] = {}
    for i in range(1, 11):
        for j in range(1, 11):
            print(i, j)
            pt_low =  h.GetXaxis().GetBinLowEdge(i) 
            pt_up =  h.GetXaxis().GetBinUpEdge(i)
            mx_low = h.GetYaxis().GetBinLowEdge(j) 
            mx_up = h.GetYaxis().GetBinUpEdge(j) 
            ibin = Effs["2022"]["JetMET"].GetGlobalBin(i, j)
            pt_string = f"{pt_low}_{pt_up}"
            mx_string = f"{mx_low}_{mx_up}" 
            SFs_dict[year]["TTto4Q"].setdefault(pt_string, {})
            #if pt_string not in SFs_dict[year]["TTto4Q"]:
            #    SFs_dict[year]["TTto4Q"][pt_string] = {}
            SFs_dict[year]["TTto4Q"][pt_string][mx_string] = {}
            SFs_dict[year]["TTto4Q"][pt_string][mx_string]["nom"] = SFs[year][ibin]
            SFs_dict[year]["TTto4Q"][pt_string][mx_string]["up"] = SF_ups[year][ibin]
            SFs_dict[year]["TTto4Q"][pt_string][mx_string]["down"] = SF_downs[year][ibin]
            print(pt_low, pt_up, mx_low, mx_up, SFs[year][ibin])
with open("trigger_SFs.json", "w") as f:
    json.dump(SFs_dict, f, indent=4)
'''
