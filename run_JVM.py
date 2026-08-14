# Running selection for mode 1p1
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
parser.add_argument('-s', type=str, dest='JME_syst',action='store', required=True)
parser.add_argument('-r', type=str, dest='region',action='store', required=True)
args = parser.parse_args()

#cpp modules from Matej
CompileCpp("cpp_modules/deltaRMatching.cc")
CompileCpp("cpp_modules/helperFunctions.cc")
CompileCpp("cpp_modules/XHYgenMatching.cc")
CompileCpp("cpp_modules/ttbar_genMatching.cc")

CompileCpp("cpp_modules/selection_functions.cc")
CompileCpp("cpp_modules/TaggerDiscretizer.cc")

#Specifying columns to save
columns = ["n.*", "Jet_eta", "Jet_phi"]

Reg = args.region
ana = XHY4b_Analyzer(args.dataset, args.year, args.n_files, args.i_job, nEvents = -1)
ana.check_JVM(args.JME_syst, Reg, massType = "msoftdrop")

file_basename = os.path.basename(args.dataset).removesuffix(".txt")
ana.output = "Reg" + Reg[0:3] + "_" + args.JME_syst + "_1p1_tagged_selected_" + file_basename + f"_n-{args.n_files}_i-{args.i_job}.root"

if "MC" in args.dataset:
    ana.snapshot(columns + ["genWeight"], saveRunChain = True)
else:
    ana.snapshot(columns, saveRunChain = True)
ana.save_cutflowInfo()
