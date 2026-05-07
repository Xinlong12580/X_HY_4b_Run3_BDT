import ROOT
import os
import json
ROOT.gInterpreter.Declare('''float mass_shift(float mass, float input_down, float input_up, float target_down, float target_up){ return (target_up - target_down)/(input_up - input_down) * (mass - input_down) + target_down;}''')
#from TIMBER.Tools.Common import CompileCpp, OpenJSON
#CompileCpp("discretizeTaggers.C")
from argparse import ArgumentParser
parser=ArgumentParser()
ROOT.gROOT.ProcessLine(".L simpleDiscretizer.cc+")
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
args = parser.parse_args()
files = [f for f in os.listdir('./datasets')]

#print(files)
with open("WPs.json", "r") as f:
    WPs = json.load(f)
AK4_WPs = "{"
for WP in WPs["AK4"][args.year]:
    AK4_WPs += f"{WP},"
AK4_WPs = AK4_WPs[:-1] + "}"
print(AK4_WPs)
AK8_WPs = "{"
for WP in WPs["AK8"][args.year]:
    AK8_WPs += f"{WP},"
AK8_WPs = AK8_WPs[:-1] + "}"
print(AK8_WPs)
ROOT.gInterpreter.Declare(f'TaggerDiscretizer AK4_discretizer = TaggerDiscretizer("Jet",  "", "", {AK4_WPs});')
ROOT.gInterpreter.Declare(f'TaggerDiscretizer AK8_discretizer = TaggerDiscretizer("FatJet",  "", "", {AK8_WPs});')
year_IDs = {"2022": 1, "2022EE": 2, "2023": 3, "2023BPix": 4, "2024": 5} 
for f in files:
    if f.startswith("Reg") and f.endswith(".root") and args.mode in f and (args.year + "__") in f:
        if "SignalMC" in f:
            sample_id = 0
        elif "TTBar" in f:
            sample_id = 1
        elif "QCD" in f:
            sample_id = 2
        elif "Data" in f:
            sample_id = -1
        print("Processing: " + f)
        original_weight = f"weight_{args.mode}__nominal"
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
            rdf_events = rdf_events.Filter("flag1p1")
            rdf_events = rdf_events.Define("MX", "val1p1_MX")
            rdf_events = rdf_events.Define("MassHiggsCandidate", "mass_shift(val1p1_MassHiggsCandidate, 60, 100, 100, 150 )")
            rdf_events = rdf_events.Define("MY", "val1p1_MY")
            rdf_events = rdf_events.Define("Delta_Y", "val1p1_Delta_Y")
            rdf_events = rdf_events.Define("Tagger_H", "val1p1_Tagger_H")
            rdf_events = rdf_events.Define("Tagger_Y", "val1p1_Tagger_Y")
            rdf_events = rdf_events.Define("Tagger_H_decapitated", "val1p1_Tagger_H_decapitated")
            rdf_events = rdf_events.Define("Tagger_Y_decapitated", "val1p1_Tagger_Y_decapitated")
            rdf_events = rdf_events.Filter("MX > 200")
            rdf_events = rdf_events.Filter("MY > 40")
            rdf_events = rdf_events.Filter("Tagger_H > 0.1")
            rdf_events = rdf_events.Filter("Tagger_Y > 0.1")
            #rdf_events = rdf_events.Define("Tagger_H_decapitated", "AK8_discretizer.decapitate(Tagger_H)") ##IF this columen already exists; comment out this line
            #rdf_events = rdf_events.Define("Tagger_Y_decapitated", "AK8_discretizer.decapitate(Tagger_Y)") ##IF this columen already exists; comment out this line
        elif args.mode == "2p1":
            rdf_events = rdf_events.Filter("flag2p1")
            rdf_events = rdf_events.Define("MX", "val2p1_MX")
            rdf_events = rdf_events.Define("MY", "val2p1_MY")
            rdf_events = rdf_events.Define("MassHiggsCandidate", "mass_shift(val2p1_MassHiggsCandidate, 60, 100, 100, 150 )")
            rdf_events = rdf_events.Define("Tagger_H", "val2p1_Tagger_H")
            rdf_events = rdf_events.Define("Tagger_b_Y0", "val2p1_Tagger_b_Y0")
            rdf_events = rdf_events.Define("Tagger_b_Y1", "val2p1_Tagger_b_Y1")
            rdf_events = rdf_events.Define("Tagger_H_discrete", "val2p1_Tagger_H_discrete")
            rdf_events = rdf_events.Define("Tagger_b_Y0_discrete", "val2p1_Tagger_b_Y0_discrete")
            rdf_events = rdf_events.Define("Tagger_b_Y1_discrete", "val2p1_Tagger_b_Y1_discrete")
            rdf_events = rdf_events.Define("Tagger_H_decapitated", "val2p1_Tagger_H_decapitated")
            rdf_events = rdf_events.Define("Tagger_b_Y0_decapitated", "val2p1_Tagger_b_Y0_decapitated")
            rdf_events = rdf_events.Define("Tagger_b_Y1_decapitated", "val2p1_Tagger_b_Y1_decapitated")
            rdf_events = rdf_events.Filter("MX > 200")
            rdf_events = rdf_events.Filter("MY > 200")
            rdf_events = rdf_events.Filter("Tagger_H > 0.1")
            rdf_events = rdf_events.Filter("Tagger_b_Y0_discrete >= 1")
            rdf_events = rdf_events.Filter("Tagger_b_Y1_discrete >= 1")
            #rdf_events = rdf_events.Define("Tagger_H_decapitated", "AK8_discretizer.decapitate(Tagger_H)") ##IF this columen already exists; comment out this line
            #rdf_events = rdf_events.Define("Tagger_b_Y0_decapitated", "AK4_discretizer.decapitate(Tagger_b_Y0)") ##IF this columen already exists; comment out this line
            #rdf_events = rdf_events.Define("Tagger_b_Y1_decapitated", "AK4_discretizer.decapitate(Tagger_b_Y1)") ##IF this columen already exists; comment out this line
        rdf_events = rdf_events.Define("BDT_weight", f"{original_weight} / {total_weight}")
        rdf_events = rdf_events.Define("sample_ID", f"{sample_id}")
        rdf_events = rdf_events.Define("year_ID", f"{year_IDs[args.year]}")
        rdf_events = rdf_events.Define("event_Idx", f"rdfentry_")
        rdf_events.Snapshot("Events", out_f)
        
