import ROOT

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
args = parser.parse_args()
f = ROOT.TFile.Open("TMVAC_{args.mode}_{args.year}_discrete.root", "READ")
h = f.Get("dataset_{args.mode}_{args.year}_discrete/Method_BDT/BDTG/MVA_BDTG_rejBvsS")
#h = f.Get("dataset_2p1/Method_BDT/BDTG/MVA_BDTG_trainingRejBvsS")
#print(h.Integral()/ h.GetEntries())
AUC = 0.
print(h.GetNbinsX())
for i in range(h.GetNbinsX()):
    area = (h.GetXaxis().GetBinUpEdge(i + 1) - h.GetXaxis().GetBinLowEdge(i + 1)) * h.GetBinContent(i+1)
    AUC += area
print(AUC) 
