import ROOT
import os

#from TIMBER.Tools.Common import CompileCpp, OpenJSON
#CompileCpp("discretizeTaggers.C")
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
args = parser.parse_args()
files = [f for f in os.listdir('./datasets')]
#print(files)
for f in files:
    if f.startswith("Reg") and f.endswith(".root") and args.mode in f and (args.year + "_") in f:
        if "SignalMC" in f:
            sample_id = 0
        elif "TTBar" in f:
            sample_id = 1
        elif "QCD" in f:
            sample_id = 2
        elif "Data" in f:
            sample_id = -1
        print("Processing: " + f)
        original_weight = "weight_All__nominal"
        #parts = f.partition(".root")
        #out_f = parts[0] + "_reweighted" + parts[1] + parts[2]
        out_f = "datasets/reweighted_" + f
        rdf_events = ROOT.RDataFrame("Events", "datasets/" + f)
        if rdf_events.Count().GetValue() < 2:
            print(rdf_events.Count().GetValue())
            continue
        rdf_runs = ROOT.RDataFrame("Runs", "datasets/" + f)
        if "Data" not in f:
            total_weight = rdf_runs.Sum("genEventSumw").GetValue()
        else:
            total_weight = 1
        if args.mode == "1p1":
            rdf_events = rdf_events.Filter("MX > 200")
            rdf_events = rdf_events.Filter("MY > 40")
            rdf_events = rdf_events.Filter("Tagger_H > 0.1")
            rdf_events = rdf_events.Filter("Tagger_Y > 0.1")
        elif args.mode == "2p1":
            rdf_events = rdf_events.Filter("MX > 200")
            rdf_events = rdf_events.Filter("MY > 200")
            rdf_events = rdf_events.Filter("Tagger_H > 0.1")
            rdf_events = rdf_events.Filter("Tagger_b_Y0_discrete >= 1")
            rdf_events = rdf_events.Filter("Tagger_b_Y1_discrete >= 1")
        rdf_events = rdf_events.Define("BDT_weight", f"{original_weight} / {total_weight}")
        rdf_events = rdf_events.Define("sample_ID", f"{sample_id}")
        rdf_events.Snapshot("Events", out_f)
        
