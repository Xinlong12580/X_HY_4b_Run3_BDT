import ROOT
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
parser.add_argument('--mx', type=str, dest='mx',action='store', required=True)
parser.add_argument('--my', type=str, dest='my',action='store', required=True)
parser.add_argument('--fname', type=str, dest='fname',action='store', default = "all")
args = parser.parse_args()

ROOT.gROOT.ProcessLine(".L MVA_evaluator.cc+")
if args.mode == "1p1":

    #ROOT.gInterpreter.Declare('MVA_evaluator evaluator(4, std::vector<std::string>({ "Delta_Y", "MassHiggsCandidate", "Tagger_H_discrete", "Tagger_Y_discrete"}), "dataset_' + args.mode + "_" + args.year +'_discrete/weights/TMVAClassification_BDTG_' + args.mode + "_" + args.year + '.weights.xml", 0, {} );')
    ROOT.gInterpreter.Declare('MVA_evaluator evaluator(4, std::vector<std::string>({ "Delta_Y", "MassHiggsCandidate", "Tagger_H_decapitated", "Tagger_Y_decapitated"}), "dataset_MX' + args.mx + "_MY" + args.my + "_"  + args.mode + "_" + args.year +'_discrete/weights/TMVAClassification_BDTG_' + args.mode + "_" + args.year + '.weights.xml", 0, {} );')
elif args.mode == "2p1":
    #ROOT.gInterpreter.Declare('MVA_evaluator evaluator(4, std::vector<std::string>({ "MassHiggsCandidate", "Tagger_H_discrete", "Tagger_b_Y0_discrete", "Tagger_b_Y1_discrete"}), "dataset_' + args.mode + "_" + args.year  +'_discrete/weights/TMVAClassification_BDTG_' + args.mode + "_" + args.year  + '.weights.xml", 0, {} );')
    ROOT.gInterpreter.Declare('MVA_evaluator evaluator(4, std::vector<std::string>({ "MassHiggsCandidate", "Tagger_H_decapitated", "Tagger_b_Y0_decapitated", "Tagger_b_Y1_decapitated"}), "dataset_MX' + args.mx + "_MY" + args.my + "_" + args.mode + "_" + args.year  +'_discrete/weights/TMVAClassification_BDTG_' + args.mode + "_" + args.year  + '.weights.xml", 0, {} );')
fs = os.listdir("datasets/")
for f in fs:
    
    if ( not f.startswith("reweighted") or "SignalMC" not in f or not args.mode in f or not (args.year + "__") in f or not "RegSig" in f) and f != f"BKGs_RegSig_{args.mode}_{args.year}_ALL.root":
        continue
    if (args.fname != "all" and f != args.fname):
        continue
    #if f != f"BKGs_RegSig_{args.mode}_{args.year}_ALL.root":
    #   continue
    print("Procesing: ", f)
    input_f = "datasets/" + f
    rdf = ROOT.RDataFrame("Events", input_f)
    try:
        if args.mode == "1p1": 
            rdf = rdf.Define("BDTG", "evaluator.eval(std::vector<float>( {Delta_Y, MassHiggsCandidate, float(Tagger_H_decapitated), float(Tagger_Y_decapitated)}))")
        elif args.mode == "2p1":
            #rdf = rdf.Define("BDTG", "evaluator.eval(std::vector<float>({ MassHiggsCandidate, PNet_H, PNet_Y0, PNet_Y1 }))")
            rdf = rdf.Define("BDTG", "evaluator.eval(std::vector<float>({ MassHiggsCandidate, float(Tagger_H_decapitated), float(Tagger_b_Y0_decapitated), float(Tagger_b_Y1_decapitated) }))")
        rdf.Snapshot("Events", f"datasets/BDT_discrete_MX{args.mx}_MY{args.my}_" + f)
    except:
        print("Warning: FAILED")
