# Running skimming and golden json masking

import ROOT
from TIMBER.Tools.Common import CompileCpp, OpenJSON
from XHY4b_Analyzer import *
from argparse import ArgumentParser
import os

#Reading Args
parser=ArgumentParser()
parser.add_argument('-d', type=str, dest='dataset',action='store', required=True)
parser.add_argument('-y', type=str, dest='year',action='store', required=True)
parser.add_argument('-n', type=int, dest='n_files',action='store', required=True)
parser.add_argument('-i', type=int, dest='i_job',action='store', required=True)
parser.add_argument('-e', type=int, dest="n_events", action="store", default=-1)
parser.add_argument('-s', type=str, dest='JME_syst',action='store', required=True)
parser.add_argument('-r', type=str, dest='region',action='store', required=True)
args = parser.parse_args()

#dataset="raw_nano/files/2023_SignalMC_XHY4b_NMSSM_XtoYHto4B_MX-900_MY-95_TuneCP5_13p6TeV_madgraph-pythia8_Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v2_NANOAODSIM.txt"

CompileCpp("cpp_modules/skim_functions.cc")
CompileCpp("cpp_modules/goldenJson_mask.cc")

ana = XHY4b_Analyzer(args.dataset, args.year, args.n_files, args.i_job, args.n_events)

#Running skimming and masking
ana.skim()

ana.mask_goldenJson()
ana.cut_goldenJson()

#Saving snapshot and cutflow
file_basename=os.path.basename(args.dataset)
ana.output = "skimmed_" + file_basename + f"_n-{args.n_files}_i-{args.i_job}.root"
if "Data" in args.dataset:
    ana.output = "masked_skimmed_" + file_basename + f"_n-{args.n_files}_i-{args.i_job}.root"

ana.snapshot(saveRunChain = True)
ana.save_cutflowInfo()


skim_output = ana.output



CompileCpp("cpp_modules/deltaRMatching.cc")
CompileCpp("cpp_modules/helperFunctions.cc")
CompileCpp("cpp_modules/XHYgenMatching.cc")
CompileCpp("cpp_modules/ttbar_genMatching.cc")

CompileCpp("cpp_modules/selection_functions.cc")
CompileCpp("cpp_modules/TaggerDiscretizer.cc")

#Specifying columns to save
columns = ["val1p1.*", "val2p1.*", "flag1p1.*", "flag2p1.*", "weight.*"]

#Running selection
Reg = args.region
ana = XHY4b_Analyzer(skim_output, args.year, 1, 0)
ana.selection_combined_BDT(args.JME_syst, Reg, massType = "msoftdrop")
file_basename = os.path.basename(args.dataset).removesuffix(".root")
ana.output = "Reg" + Reg[0:3] + "_" + args.JME_syst + "_combined_tagged_selected_" + file_basename + f"_n-{args.n_files}_i-{args.i_job}.root"


if "MC" in args.dataset:
    ana.snapshot(columns + ["genWeight"], saveRunChain = True)
else:
    ana.snapshot(columns, saveRunChain = True)
ana.save_cutflowInfo()

                                   
