#Running division for mode 1p1
import ROOT
from TIMBER.Tools.Common import CompileCpp, OpenJSON
from XHY4b_Analyzer import *
from argparse import ArgumentParser
import os

#Reading input args
CompileCpp("cpp_modules/MVA_evaluator.cc")
CompileCpp("cpp_modules/DDT_map.cc")
parser=ArgumentParser()
parser.add_argument('-d', type=str, dest='dataset',action='store', required=True)
parser.add_argument('-y', type=str, dest='year',action='store', required=True)
parser.add_argument('-n', type=int, dest='n_files',action='store', required=True)
parser.add_argument('-i', type=int, dest='i_job',action='store', required=True)
args = parser.parse_args()
Veto_cuts = {"All1p1": "flag1p1", "All2p1" : "flag2p1", "Only1p1" : "flag1p1 && (! flag2p1)", "Only2p1": "flag2p1 && (! flag1p1)"}
#Veto_cuts = {"All1p1": "flag1p1", "Only1p1" : "flag1p1 && (! flag2p1)"}
#For each region, cut on the b score, then save the snapshot and cutflow and make 2D histograms
for veto_cut in Veto_cuts:

    #B tagging
    ana = XHY4b_Analyzer(args.dataset, args.year, args.n_files, args.i_job)

    #Specifying regions we want to save. each region is saved to one root file
    regions = ["SR1", "SB1"]

    file_basename=os.path.basename(args.dataset).replace(".txt", f"_n-{args.n_files}_i-{args.i_job}.root")

    #Checking what JME correction the file has, cause we want to do the nom correction differently
    JME_systs = ["nom", "JES__up", "JES__down", "JER__up", "JER__down"]
    JME_systs = ["nom", "JER__up", "JER__down"]
    jes_systs = ["Absolute", f"Absolute_{args.year}", "BBEC1", f"BBEC1_{args.year}", "EC2", f"EC2_{args.year}", "FlavorQCD", "HF", f"HF_{args.year}", f"RelativeBal", f"RelativeSample_{args.year}" ]
    for jes_syst in jes_systs:
        JME_systs.append(f"JES__{jes_syst}_up")
        JME_systs.append(f"JES__{jes_syst}_down")

    JMC_systs = ["nom", "JMS__up", "JMS__down", "JMR__up", "JMR__down"]
    for ele in JMC_systs:
        if ele in file_basename:
            JMC_syst = ele
            break

    if "1p1" in veto_cut:
        mode = "1p1"
        ana.analyzer.Define("Tagger_Y_decapitated", "val1p1_Tagger_Y_decapitated")
        ana.analyzer.Define("Tagger_H_decapitated", "val1p1_Tagger_H_decapitated")
        ana.analyzer.Define("MX", "val1p1_MX")
        ana.analyzer.Define("MY", "val1p1_MY")
        if "Data" not in args.dataset:
            for _syst in JME_systs:
                ana.analyzer.Define(f"MX_{_syst}", f"val1p1_MX_{_syst}")
                ana.analyzer.Define(f"MY_{_syst}", f"val1p1_MY_{_syst}")
        ana.analyzer.Define("Delta_Y", "val1p1_Delta_Y")
        ana.analyzer.Define("MassHiggsCandidate", "val1p1_MassHiggsCandidate")
        ana.analyzer.Define("MassHiggsCandidate_regressed", "val1p1_MassHiggsCandidate_regressed")
    
        ana.BDT_tagging_discrete_1p1()
    if "2p1" in veto_cut:
        mode = "2p1"
        ana.analyzer.Define("Tagger_b_Y0_decapitated", "val2p1_Tagger_b_Y0_decapitated")
        ana.analyzer.Define("Tagger_b_Y1_decapitated", "val2p1_Tagger_b_Y1_decapitated")
        ana.analyzer.Define("MassHiggsCandidate", "val2p1_MassHiggsCandidate")
        ana.analyzer.Define("MassHiggsCandidate_regressed", "val2p1_MassHiggsCandidate_regressed")
        ana.analyzer.Define("Tagger_H_decapitated", "val2p1_Tagger_H_decapitated")
        ana.analyzer.Define("MX", "val2p1_MX")
        ana.analyzer.Define("MY", "val2p1_MY")
        if "Data" not in args.dataset:
            for _syst in JME_systs:
                ana.analyzer.Define(f"MX_{_syst}", f"val2p1_MX_{_syst}")
                ana.analyzer.Define(f"MY_{_syst}", f"val2p1_MY_{_syst}")
        ana.BDT_tagging_discrete_2p1()
    ana.analyzer.Define("MX_TeV", "MX/1000")
    ana.analyzer.Define("MY_TeV", "MY/1000")
    if "Data" not in args.dataset:
        for _syst in JME_systs:
            ana.analyzer.Define(f"MX_TeV_{_syst}", f"MX_{_syst}/1000")
            ana.analyzer.Define(f"MY_TeV_{_syst}", f"MY_{_syst}/1000")
    ana.analyzer.Cut(veto_cut, Veto_cuts[veto_cut])
    veto_base_node = ana.analyzer.GetActiveNode()
    ana.output = veto_cut + "_division_" + file_basename
    f = ROOT.TFile.Open("Templates_" + ana.output, "RECREATE")
    #ana.snapshot(saveRunChain = True)
    for region in regions:
        ana.analyzer.SetActiveNode(veto_base_node)
        ana.divide(region)
        print(ana.output)
        ana.dumpTemplates_compound(region, f, JMC_syst, mode = mode, MX = "MX_TeV", MY = "MY_TeV", bin_scale = 1e-3)
        if "Data" in args.dataset: continue
        if JMC_syst != "nom": continue
        for _syst in JME_systs:
            if _syst == "nom": continue 
            ana.dumpTemplates_compound(region, f, _syst, mode = mode, MX = f"MX_TeV_{_syst}", MY = f"MY_TeV_{_syst}", bin_scale = 1e-3)
    f.Close()
    ana.save_cutflowInfo()


