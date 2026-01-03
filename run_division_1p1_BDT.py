#Running division for mode 1p1
import ROOT
from TIMBER.Tools.Common import CompileCpp, OpenJSON
from XHY4b_Analyzer import *
from argparse import ArgumentParser
import os

#Reading input args
parser=ArgumentParser()
parser.add_argument('-d', type=str, dest='dataset',action='store', required=True)
parser.add_argument('-y', type=str, dest='year',action='store', required=True)
parser.add_argument('-n', type=int, dest='n_files',action='store', required=True)
parser.add_argument('-i', type=int, dest='i_job',action='store', required=True)
args = parser.parse_args()
CompileCpp("cpp_modules/MVA_evaluator.cc")
CompileCpp("cpp_modules/DDT_map.cc")
#B tagging
ana = XHY4b_Analyzer(args.dataset, args.year, args.n_files, args.i_job)
ana.BDT_tagging_1p1()

#Specifying regions we want to save. each region is saved to one root file
regions = ["SR1", "SB1"]

file_basename=os.path.basename(args.dataset).replace(".txt", f"_n-{args.n_files}_i-{args.i_job}.root")

#Checking what JME correction the file has, cause we want to do the nom correction differently
JME_systs = ["nom", "JES__up", "JES__down", "JER__up", "JER__down"]
for ele in JME_systs:
    if ele in file_basename:
        JME_syst = ele
        break

#For each region, cut on the b score, then save the snapshot and cutflow and make 2D histograms
base_node = ana.analyzer.GetActiveNode()
ana.output = "division_1p1_" + file_basename
f = ROOT.TFile.Open("Templates_" + ana.output, "RECREATE")
ana.snapshot(saveRunChain = True)
for region in regions:
    ana.analyzer.SetActiveNode(base_node)
    ana.divide(region)
    #ana.output = region + "_" + file_basename
    print(ana.output)
    #ana.snapshot(saveRunChain = True)
    #ana.save_cutflowInfo()
    ana.dumpTemplates_normalized(region, f, JME_syst) 
f.Close()
ana.save_cutflowInfo()

