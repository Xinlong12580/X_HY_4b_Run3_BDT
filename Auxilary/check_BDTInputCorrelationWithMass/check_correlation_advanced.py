import ROOT
import os
import sys
ROOT.gROOT.SetBatch(True)
DIR_TOP = os.environ["ANA_TOP"]
sys.path.append(DIR_TOP)
from XHY4b_Helper import *

data_files = []
template_files = []
with open(DIR_TOP + "/outputList/output_selection_1p1_BDT.txt", "r") as _f:
    lines = _f.readlines()
    for line in lines:
        if "Signal" in line and "Template" not in line and "2022EE" in line:
            data_files.append(line.strip())
            data_file_part = line.partition("nom")
            template_file = (data_file_part[0] + "Templates_" + data_file_part[1] + data_file_part[2]).strip()
            template_files.append(template_file)

signals = ["MX-600_MY-200", "MX-1000_MY-200", "MX-2000_MY-200", "MX-4000_MY-200"]
indices = []
for signal in signals:
    for index in range(len(data_files)):
        if signal in data_files[index]:
            indices.append(index)
            break
columns = ["PNet_H", "PNet_Y", "DeltaEta", "DeltaY", "MassHiggsCandidate"]
bins= {}
bins["MassHiggsCandidate"] = array.array("d", np.linspace(90, 160, 8) )

bins["PNet_H"] = array.array("d", np.linspace(0, 1, 101) )
bins["PNet_Y"] = array.array("d", np.linspace(0, 1, 101) )
bins["DeltaEta"] = array.array("d", np.linspace(0, 5, 101) )
bins["DeltaY"] = array.array("d", np.linspace(0, 5, 101) )

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kBlack, ROOT.kOrange, ROOT.kMagenta]
'''
for column in columns:
    for i in range(len(signals)):
        f = ROOT.TFile.Open(template_files[indices[i]])
        for key in f.GetListOfKeys():
            hist = key.ReadObj()
            hist_name = hist.GetName()
            if column in hist_name:
                c = ROOT.TCanvas("c", "c")
                hist.Scale(1 / hist.Integral())
                hist.Draw("HIST")
                c.Update()
                c.Print(f"advanced_{column}_{signals[i]}.png")
'''         

for column in columns:
    c = ROOT.TCanvas("c", "c")
    leg = ROOT.TLegend(0.65, 0.7, 0.88, 0.88)
    hs = []
    for i in range(len(signals)):
        print(data_files[indices[i]])
        rdf = ROOT.RDataFrame("Events", data_files[indices[i]])
        rdf = rdf.Filter("PNet_H > 0.1 && PNet_Y > 0.1")
        hist = rdf.Histo1D((f"{signal}_{column}", f"{signal}_{column}", len(bins[column]) - 1, bins[column]), column, "weight_All__nominal").GetValue()
        hs.append(hist.Clone())
        print(i, len(hs))
        hs[i].SetDirectory(0) 
        hs[i].Scale(1 / hs[i].Integral())
        hs[i].SetLineColor(colors[i])
        if i == 0:
            hs[i].Draw("HIST")
        else:
            hs[i].Draw("HIST SAME")
        leg.AddEntry(hs[i], signals[i])
    leg.Draw()
    c.Update()
    c.Print(f"advanced_{column}.png")
            
            
        
