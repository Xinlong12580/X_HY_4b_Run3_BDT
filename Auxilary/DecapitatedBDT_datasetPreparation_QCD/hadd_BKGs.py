import ROOT
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
args = parser.parse_args()
try_files =  [ "datasets/" + f for f in os.listdir("datasets/") if (f.startswith("reweighted") and ("QCD" in f or "TTBar" in f) and (args.year + "__") in f and args.mode in f) ]
print("hadding files: ")
sumN = 0
files = []
for f in try_files:
    print(f)
    root_f = ROOT.TFile.Open(f, "READ")
    sumN += root_f.Get("Events").GetEntries()
    if root_f.Get("Events").GetEntries() >= 1:
        files.append(f)
print(sumN)
rdf = ROOT.RDataFrame("Events",files)
print(rdf.Count().GetValue())
columns = ["BDT_weight", "Delta_Y", "Delta_Eta", "Tagger_H", "Tagger_Y", "Tagger_H_discrete", "Tagger_Y_discrete", "Tagger_H_decapitated", "Tagger_H_decapitated", "sample_ID", "year_ID", "MassHiggsCandidate.*" ]
columns = "BDT_weight|Delta_.*|Tagger_.*|sample_ID|year_ID|MassHiggsCandidate.*|MX|MY|idx.*|Mass.*|event_Idx"
rdf.Snapshot("Events", f"datasets/BKGs_RegSig_{args.mode}_{args.year}_ALL.root", columns)
