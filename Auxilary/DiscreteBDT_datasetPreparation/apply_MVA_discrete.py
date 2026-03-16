import ROOT
from TIMBER.Tools.Common import CompileCpp
#from CompileCpp import CompileCpp
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
args = parser.parse_args()

CompileCpp("MVA_evaluator.cc")
#ROOT.gROOT.ProcessLine(".L MVA_evaluator.cc")
#ROOT.gSystem.CompileMacro("MVA_evaluator.cc", "k")
if args.mode == "1p1":
    ROOT.gInterpreter.Declare('MVA_evaluator evaluator(4, std::vector<std::string>({ "Delta_Y", "MassHiggsCandidate_regressed", "Tagger_H_discrete", "Tagger_Y_discrete"}), "dataset_' + args.mode + "_" + args.year +'_discrete/weights/TMVAClassification_BDTG_' + args.mode + "_" + args.year + '.weights.xml", 0, {} );')
elif args.mode == "2p1":
    ROOT.gInterpreter.Declare('MVA_evaluator evaluator(4, std::vector<std::string>({ "MassHiggsCandidate_regressed", "Tagger_H_discrete", "Tagger_b_Y0_discrete", "Tagger_b_Y1_discrete"}), "dataset_' + args.mode + "_" + args.year  +'_discrete/weights/TMVAClassification_BDTG_' + args.mode + "_" + args.year  + '.weights.xml", 0, {} );')
fs = os.listdir("datasets/")
for f in fs:
    
    if ( not f.startswith("reweighted") or "SignalMC" not in f or not args.mode in f or not (args.year + "_") in f or not "RegSig" in f) and f != f"BKGs_RegSig_{args.mode}_{args.year}_ALL.root":
        continue
    print("Procesing: ", f)
    input_f = "datasets/" + f
    #input_f = "root://cmseos.fnal.gov//store/user/xinlong//XHY4bRun3_selection_1p1_BDT/RegSig_nom_1p1_tagged_selected_SKIM_skimmed_2024__SignalMC_XHY4b__MX-900_MY-400_n-10000_i-0.root"

    rdf = ROOT.RDataFrame("Events", input_f)
    if args.mode == "1p1": 
        #rdf = rdf.Define("BDTG", "evaluator.eval(std::vector<std::variant<int, float>>( {Delta_Y, MassHiggsCandidate_regressed, Tagger_H_discrete, Tagger_Y_discrete}))")
        rdf = rdf.Define("BDTG", "evaluator.eval(std::vector<float>( {Delta_Y, MassHiggsCandidate_regressed, float(Tagger_H), float(Tagger_Y)}))")
    elif args.mode == "2p1":
        #rdf = rdf.Define("BDTG", "evaluator.eval(std::vector<float>({ MassHiggsCandidate, PNet_H, PNet_Y0, PNet_Y1 }))")
        rdf = rdf.Define("BDTG", "evaluator.eval(std::vector<std::variant<int, float>>({ MassHiggsCandidate_regressed, Tagger_H_discrete, Tagger_b_Y0_discrete, Tagger_b_Y1_discrete }))")
    rdf.Snapshot("Events", "datasets/BDT_discrete_" + f)
