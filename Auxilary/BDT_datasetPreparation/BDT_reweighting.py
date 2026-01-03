import ROOT
import os

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()

files = [f for f in os.listdir('./datasets')]
print(files)
for f in files:
    print(f)
    if f.startswith("RegSig_nom") and f.endswith(".root") and args.mode in f and "RegCon" not in f and "Data" not in f:
        if "SignalMC" in f:
            sample_id = 0
        elif "TTBar" in f:
            sample_id = 1
        elif "QCD" in f:
            sample_id = 2
        print("Processing: " + f)
        original_weight = "weight_All__nominal"
        #parts = f.partition(".root")
        #out_f = parts[0] + "_reweighted" + parts[1] + parts[2]
        out_f = "datasets/reweighted_" + f
        rdf_events = ROOT.RDataFrame("Events", "datasets/" + f)
        if rdf_events.Count().GetValue() < 10:
            continue
        rdf_runs = ROOT.RDataFrame("Runs", "datasets/" + f)
        total_weight = rdf_runs.Sum("genEventSumw").GetValue()
        rdf_events = rdf_events.Define("BDT_weight", f"{original_weight} / {total_weight}")
        rdf_events = rdf_events.Define("sample_ID", f"{sample_id}")
        rdf_events = rdf_events.Define("minPNet", f"std::min(PNet_H, PNet_Y)")
        rdf_events.Snapshot("Events", out_f)
        
