import ROOT

f = ROOT.TFile.Open("TMVAC_2p1_discrete.root", "READ")
h = f.Get("dataset_2p1_discrete/Method_BDT/BDTG/MVA_BDTG_rejBvsS")
#h = f.Get("dataset_2p1/Method_BDT/BDTG/MVA_BDTG_trainingRejBvsS")
#print(h.Integral()/ h.GetEntries())
AUC = 0.
print(h.GetNbinsX())
for i in range(h.GetNbinsX()):
    area = (h.GetXaxis().GetBinUpEdge(i + 1) - h.GetXaxis().GetBinLowEdge(i + 1)) * h.GetBinContent(i+1)
    AUC += area
print(AUC) 
