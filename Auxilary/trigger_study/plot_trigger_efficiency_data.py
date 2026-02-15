import ROOT
import numpy as np
import matplotlib.pyplot as plt
import array
import os
import sys
DIR_TOP = os.environ["ANA_TOP"]
sys.path.append(DIR_TOP)
from XHY4b_Helper import *
from XHY4b_Analyzer import *
from argparse import ArgumentParser
import os
ROOT.gROOT.SetBatch(True)
#Reading input args
parser=ArgumentParser()
parser.add_argument('-y', type=str, dest='year',action='store', required=True)
parser.add_argument('-m', type=str, dest='mode',action='store', required=True)
parser.add_argument('-p', type=str, dest='process',action='store', required=True)
args = parser.parse_args()
year = args.year
mode = args.mode
process = args.process
f_name = f"Templates_{process}_{year}_{mode}_all.root"
h_process = process
if process == "Data" or process == "JetMET":
    h_process = "Data_Data"
f = ROOT.TFile.Open(f_name, "READ")
for key in f.GetListOfKeys():
    hist = key.ReadObj()
    if isinstance(hist, ROOT.TH2) and "before" in str(key): 
        h_before = hist
    if isinstance(hist, ROOT.TH2) and "after" in str(key): 
        h_after = hist
#h_before = rebin_TH2(h_before, array.array("d", np.linspace(0, 3000, 11)), array.array("d", np.linspace(0, 5000, 11)))
#h_after = rebin_TH2(h_after, array.array("d", np.linspace(0, 3000, 11)), array.array("d", np.linspace(0, 5000, 11)))
h_before = rebin_TH2(h_before, array.array("d", np.linspace(200, 1000, 17)), array.array("d", np.linspace(0, 5000, 21)))
h_after = rebin_TH2(h_after, array.array("d", np.linspace(200, 1000, 17)), array.array("d", np.linspace(0, 5000, 21)))
h = h_after.Clone("Efficiency")
h.Divide(h_before)
nbins_x = h.GetNbinsX()
nbins_y = h.GetNbinsY()
zpos = np.array([[h.GetBinContent(ix+1, iy+1) for ix in range(nbins_x)] for iy in range(nbins_y)])
bins_x = [h.GetXaxis().GetBinLowEdge(i) for i in range(1, nbins_x +1) ]
bins_y = [h.GetYaxis().GetBinLowEdge(i) for i in range(1, nbins_y+1) ]
xpos, ypos = np.meshgrid(bins_x, bins_y)
fig = plt.figure(figsize=(8, 6))


print(xpos, xpos.shape)
print(ypos, ypos.shape)
print(zpos, zpos.shape, max(zpos.flatten()))
ax = fig.add_subplot(111, projection='3d')
x = xpos.flatten()
y = ypos.flatten()
z = np.zeros_like(x)
dx = bins_x[1] - bins_x[0]
dy = bins_y[1] - bins_y[0]
dz = zpos.flatten()


# Draw bars
ax.bar3d(x, y, z, dx, dy, dz, color='white', shade=False, edgecolor='black')

# Label axes
ax.set_xlabel('leading FatJet Pt (GeV)')
ax.set_ylabel('MX (GeV)')
ax.set_zlabel('Efficiency')

plt.savefig(f"trigger_eff_{process}_{year}_{mode}.png")








fig, ax = plt.subplots()
bins_x.append(h.GetXaxis().GetBinUpEdge(nbins_x))
bins_y.append(h.GetYaxis().GetBinUpEdge(nbins_y))
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
plt.savefig(f"trigger_eff_2d_{process}_{year}_{mode}.png")

c = ROOT.TCanvas("c", "c")
c.cd()
if (ROOT.TEfficiency.CheckConsistency(h_after, h_before)):
    print("Compatible Histogram")
else:
    print("Incompatible Histogram")

TEff = ROOT.TEfficiency(h_after, h_before)
print(TEff.GetDimension(), TEff.GetGlobalBin(1,1))
#for i in range(132):
#    print(TEff.GetEfficiency(i))
ht = TEff.GetPassedHistogram()
ht.Draw()
c.Print(f"test_{process}_{year}_{mode}.png")
f = ROOT.TFile.Open(f"TEffs_{mode}.root", "UPDATE")
f.cd()
TEff.Write()
f.Close()
