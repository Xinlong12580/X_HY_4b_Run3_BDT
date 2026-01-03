import ROOT
from TIMBER.Tools.Common import CompileCpp, OpenJSON
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()

CompileCpp("MVA_evaluator.cc")
'''
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
args = parser.parse_args()

#cpp modules from Matej
f = "datasets/" + args.f

rdf = ROOT.RDataFrame("Events", f)
ROOT.gInterpreter.Declare('MVA_evaluator evaluator(4, std::vector<std::string>({ "DeltaY", "MassHiggsCandidate", "PNet_H", "PNet_Y"}), "dataset/weights/TMVAClassification_BDTG.weights.xml", 2, std::vector<std::string>({"BDT_weight", "sample_ID"}) );')

rdf = rdf.Define("BDTG", "evaluator.eval(std::vector<float>({ DeltaY, MassHiggsCandidate, PNet_H, PNet_Y}))")

rdf.Snapshot("Events", "datasets/BDT_" + args.f)
'''
ROOT.gInterpreter.Declare('MVA_evaluator evaluator(4, std::vector<std::string>({ "DeltaY", "MassHiggsCandidate", "PNet_H", "PNet_Y"}), "dataset_' + args.mode +'/weights/TMVAClassification_BDTG.weights.xml", 3, std::vector<std::string>({"BDT_weight", "minPNet", "sample_ID"}) );')

fs = os.listdir("datasets/")
for f in fs:
    
    if ( not f.startswith("reweighted") or "SignalMC" not in f or not args.mode in f) and f != f"BKGs_{args.mode}_ALL.root":
        continue
    print("Procesing: ", f)
    input_f = "datasets/" + f

    rdf = ROOT.RDataFrame("Events", input_f)
    
    rdf = rdf.Define("BDTG", "evaluator.eval(std::vector<float>({ DeltaY, MassHiggsCandidate, PNet_H, PNet_Y}))")

    rdf.Snapshot("Events", "datasets/BDT_" + f)
