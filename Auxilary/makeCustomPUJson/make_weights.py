import ROOT
import numpy as np
import array
import matplotlib.pyplot as plt
f_data = ROOT.TFile.Open("all_data_pu.root", "READ")
h_data = f_data.Get("pileup")
N_all_data = h_data.Integral()

nbins = h_data.GetNbinsX()
bins = [h_data.GetXaxis().GetBinLowEdge(i) for i in range(1, nbins +1) ]
bins.append(h_data.GetXaxis().GetBinUpEdge(nbins))
bins_center = [(bins[i] + bins[i+1]) / 2 for i in range(nbins)]
#rdf = ROOT.RDataFrame("Events", "skimmed_2024__SignalMC_XHY4b__MX-900_MY-95.txt_n-2_i-4.root")
rdf = ROOT.RDataFrame("Events", "ttbar.root")
h_mc = rdf.Histo1D(("h", "h", nbins, array.array("d", bins)), "Pileup_nTrueInt", "genWeight").GetValue()

N_all_mc = h_mc.Integral()

nom = np.zeros(nbins)
up = np.zeros(nbins)
down = np.zeros(nbins)
for i in range(nbins):
    n_data = h_data.GetBinContent( i + 1 ) 
    n_mc = h_mc.GetBinContent( i + 1 ) 
    if n_mc != 0:
        nom[i] = (n_data / N_all_data) / (n_mc / N_all_mc)
        uncer = N_all_mc / N_all_data * np.sqrt( n_data/ (n_mc**2) + (n_data**2 * n_mc)/ (n_mc**4))
        up[i] = nom[i] + uncer
        down[i] = max(nom[i] - uncer, 0)
    else:
        nom[i] = 1.
        up[i] = 1.
        down[i] = 1.
print(nom)
print(up)
print(down)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim(0, 3)
ax.plot(bins_center, nom, color = "black")
ax.plot(bins_center, down, color = "blue")
ax.plot(bins_center, up, color = "red")
fig.savefig("weights.png")
with open("puweights_2024.txt", "w") as f:
    for i in range(nbins):
        f.write(f"{bins[i]} {bins[i+1]} {nom[i]} {up[i]} {down[i]}\n")

