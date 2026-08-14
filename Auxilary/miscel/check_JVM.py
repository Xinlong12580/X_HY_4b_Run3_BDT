import ROOT
import matplotlib.pyplot as plt
import numpy as np
years = ["2022", "2022EE", "2023", "2023BPix", "2024"]
year = "2023BPix"
fname_before = f"skimmed_{year}__MC_QCDJets__QCD-4Jets_HT-1000to1200.txt_n-10_i-0.root"
fname_after = f"RegSig_nom_1p1_tagged_selected_skimmed_{year}__MC_QCDJets__QCD-4Jets_HT-1000to1200.txt_n-10_i-0.root_n-1_i-0.root"
fname_before = f"skimmed_2024__MC_QCDJets__QCD-4Jets_HT-1000to1200.txt_n-1_i-0.root"
fname_after = f"RegSig_nom_1p1_tagged_selected_skimmed_2024__MC_QCDJets__QCD-4Jets_HT-1000to1200.txt_n-1_i-0.root_n-1_i-0.root"

for _year in years:
    if _year + "_" in fname_before:
        year = _year
        break
f_before = ROOT.TFile.Open(fname_before, "READ")
f_after =  ROOT.TFile.Open(fname_after, "READ")

events_before = f_before.Get("Events")
events_after = f_after.Get("Events")

etas_before = []
phis_before = []
etas_after = []
phis_after = []

for entry in events_before:
    for eta in entry.Jet_eta:
        etas_before.append(eta)
    for phi in entry.Jet_phi:
        phis_before.append(phi)

for entry in events_after:
    for eta in entry.Jet_eta:
        etas_after.append(eta)
    for phi in entry.Jet_phi:
        phis_after.append(phi)

fig = plt.figure()
ax = fig.add_subplot(111)
#ax.hist2d(etas_before, phis_before, bins = [400, 400])

H, xedges, yedges = np.histogram2d(etas_before, phis_before, bins=[400, 400])
H = np.ma.masked_where(H == 0, H)
mesh = ax.pcolormesh(xedges, yedges, H.T)
fig.colorbar(mesh, ax = ax, label="Counts")

ax.set_xlabel("eta")
ax.set_ylabel("phi")
ax.set_title(f"eta-phi map before applying JVM of year {year}")
fig.savefig(f"before_JVM_{year}.png")

fig = plt.figure()
ax = fig.add_subplot(111)
#ax.hist2d(etas_after, phis_after, bins = [400, 400])
H, xedges, yedges = np.histogram2d(etas_after, phis_after, bins= [400, 400])
H = np.ma.masked_where(H == 0, H)
mesh = ax.pcolormesh(xedges, yedges, H.T)
fig.colorbar(mesh, ax = ax, label="Counts")

ax.set_xlabel("eta")
ax.set_ylabel("phi")
ax.set_title(f"eta-phi map after applying JVM of year {year}")
fig.savefig(f"after_JVM_{year}.png")
