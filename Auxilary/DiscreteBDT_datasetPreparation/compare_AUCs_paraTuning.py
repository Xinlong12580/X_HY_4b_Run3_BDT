import ROOT
import matplotlib.pyplot
import pickle
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
args = parser.parse_args()
f = ROOT.TFile.Open(f"TMVAC_optimization_{args.mode}_{args.year}_discrete.root", "READ")
BDT_dir = f.Get(f"dataset_optimization_{args.mode}_{args.year}_discrete/Method_BDT")
AUCs = {}
ROCs = {}
for key in BDT_dir.GetListOfKeys():
    obj = key.ReadObj()
    if obj.InheritsFrom("TDirectory"):
        print("config: " , obj.GetName())
        config_name = obj.GetName()
        paras = config_name.split("_")
        para_names = ["Method", "NTree", "MinNodeSize", "Shrinkage", "BaggedSampleFraction", "nCuts", "MaxDepth"]
        print_str = ""
        for i in range(len(paras)):
            print_str += (para_names[i] + ": " + paras[i] + ", ")
        print(print_str)
        subsubdir = BDT_dir.Get(f"{config_name}") 
        h = BDT_dir.Get(f"{config_name}/MVA_{config_name}_rejBvsS") 
        #print(h.Integral()/ h.GetEntries())
        AUC = 0.
        print(h.GetNbinsX())
        for i in range(h.GetNbinsX()):
            area = (h.GetXaxis().GetBinUpEdge(i + 1) - h.GetXaxis().GetBinLowEdge(i + 1)) * h.GetBinContent(i+1)
            AUC += area
        print(AUC) 
        AUCs[config_name] = AUC
        xs = [(h.GetXaxis().GetBinUpEdge(i + 1) + h.GetXaxis().GetBinLowEdge(i + 1))/ 2 for i in range(h.GetNbinsX())]
        ys = [h.GetBinContent(i+1) for i in range(h.GetNbinsX())]
        ROCs[config_name] = {}
        ROCs[config_name]["X"] = xs
        ROCs[config_name]["Y"] = ys
print(AUCs)
with open(f"AUCs_{args.mode}_{args.year}.txt", "w") as _f:
    for config_name in AUCs:
        _f.write(f"{config_name} {AUCs[config_name]}\n")
with open(f"ROCs_{args.mode}_{args.year}.pkl", "wb") as _f:
        pickle.dump(ROCs, _f)
        pickle.dump(AUCs, _f)
