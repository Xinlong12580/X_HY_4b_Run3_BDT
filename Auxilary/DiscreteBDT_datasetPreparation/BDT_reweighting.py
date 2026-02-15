import ROOT
import os

from TIMBER.Tools.Common import CompileCpp, OpenJSON
CompileCpp("discretizeTaggers.C")
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()
years = ["2022", "2022EE", "2023", "2023BPix"]
files = [f for f in os.listdir('./datasets')]
#print(files)
for f in files:
    print(f)
    if f.startswith("Reg") and f.endswith(".root") and args.mode in f:
        if "SignalMC" in f:
            sample_id = 0
        elif "TTBar" in f:
            sample_id = 1
        elif "QCD" in f:
            sample_id = 2
        elif "Data" in f:
            sample_id = -1
        print("Processing: " + f)
        for _year in years:
            if _year + "_" in f:
                year = _year
                break
        original_weight = "weight_All__nominal"
        #parts = f.partition(".root")
        #out_f = parts[0] + "_reweighted" + parts[1] + parts[2]
        out_f = "datasets/reweighted_" + f
        rdf_events = ROOT.RDataFrame("Events", "datasets/" + f)
        if rdf_events.Count().GetValue() < 10:
            continue
        rdf_runs = ROOT.RDataFrame("Runs", "datasets/" + f)
        if "Data" not in f:
            total_weight = rdf_runs.Sum("genEventSumw").GetValue()
        else:
            total_weight = 1

        if args.mode == "1p1":
            rdf_events = rdf_events.Define("minPNet", f"std::min(PNet_H, PNet_Y)")
            rdf_events = rdf_events.Filter("minPNet > 0.3")
            rdf_events = rdf_events.Define("PNet_H_discrete", f'discretizeTaggers(PNet_H, "AK8", "{year}")')
            rdf_events = rdf_events.Define("PNet_Y_discrete", f'discretizeTaggers(PNet_Y, "AK8", "{year}")')
        elif args.mode == "2p1":
            rdf_events = rdf_events.Define("minPNet", f"std::min(PNet_H, PNet_Ymin)")
            rdf_events = rdf_events.Define("minPNet_higherY", f"std::min(PNet_H, PNet_Y)")
            rdf_events = rdf_events.Filter("PNet_Ymin > 0.04")
            rdf_events = rdf_events.Filter("PNet_H > 0.3")
            #rdf_events = rdf_events.Filter("minPNet > 0.04")
            #rdf_events = rdf_events.Filter("minPNet_higherY > 0.1")
            rdf_events = rdf_events.Filter("MassYCandidate > 200")
            rdf_events = rdf_events.Define("PNet_H_discrete", f'discretizeTaggers(PNet_H, "AK8", "{year}")')
            rdf_events = rdf_events.Define("PNet_Y_discrete", f'discretizeTaggers(PNet_Y, "AK4", "{year}")')
            rdf_events = rdf_events.Define("PNet_Y0_discrete", f'discretizeTaggers(PNet_Y0, "AK4", "{year}")')
            rdf_events = rdf_events.Define("PNet_Y1_discrete", f'discretizeTaggers(PNet_Y1, "AK4", "{year}")')
        #if (sample_id == -1000):
        #    rdf_events = rdf_events.Define("BDT_weight", f"2.55 * {original_weight} / {total_weight}")
        #else:
        #    rdf_events = rdf_events.Define("BDT_weight", f"{original_weight} / {total_weight}")
        rdf_events = rdf_events.Define("BDT_weight", f"{original_weight} / {total_weight}")
        rdf_events = rdf_events.Define("sample_ID", f"{sample_id}")
        rdf_events.Snapshot("Events", out_f)
        
