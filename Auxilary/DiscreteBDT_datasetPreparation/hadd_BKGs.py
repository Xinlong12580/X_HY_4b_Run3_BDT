import ROOT
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
args = parser.parse_args()
files =  [ "datasets/" + f for f in os.listdir("datasets/") if (f.startswith("reweighted") and ("QCD" in f or "TTBar" in f) and (args.year + "__") in f and args.mode in f) ]
rdf = ROOT.RDataFrame("Events",files)
print("hadding files: ")
sumN = 0
for f in files:
    print(f)
    root_f = ROOT.TFile.Open(f, "READ")
    sumN += root_f.Get("Events").GetEntries()
print(sumN)
print(rdf.Count().GetValue())
columns = ["BDT_weight", "Delta_Y", "Delta_Eta", "Tagger_H", "Tagger_Y", "Tagger_H_discrete", "Tagger_Y_discrete", "Tagger_H_decapitated", "Tagger_H_decapitated", "sample_ID", "year_ID", "MassHiggsCandidate.*" ]
columns = "BDT_weight|Delta_.*|Tagger_.*|sample_ID|year_ID|MassHiggsCandidate.*|MX|MY"
rdf.Snapshot("Events", f"datasets/BKGs_RegSig_{args.mode}_{args.year}_ALL.root", columns)
