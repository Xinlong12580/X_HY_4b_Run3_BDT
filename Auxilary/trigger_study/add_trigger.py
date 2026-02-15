import ROOT
import numpy as np
import matplotlib.pyplot as plt
import array
import os
import sys
DIR_TOP = os.environ["ANA_TOP"]
sys.path.append(DIR_TOP)
from XHY4b_Helper import *
from XHY4b_Analyzer import *
from argparse import ArgumentParser
import os

#Reading input args
parser=ArgumentParser()
parser.add_argument('-y', type=str, dest='year',action='store', required=True)
parser.add_argument('-m', type=str, dest='mode',action='store', required=True)
parser.add_argument('-p', type=str, dest='process',action='store', required=True)
args = parser.parse_args()
year = args.year
mode = args.mode
process = args.process
triggers = ["HLT_AK8PFJet420_MassSD30", "HLT_AK8PFJet500", "HLT_PFJet500", "HLT_PFHT1050", "HLT_AK8DiPFJet250_250_MassSD50", "HLT_AK8PFHT800_TrimMass50"]
path ="../../outputList/"
files = [path + f for f in os.listdir(path) if mode in f and process in f and (year + "_") in f and (process + "0") not in f and os.path.isfile(os.path.join(path, f))]
print(files)
root_files = []
for f_name in files:
    with open(f_name, "r") as f:
        for root_file in f.readlines():
            root_files.append(root_file)
print(root_files)         
dataset = f"{process}_{year}_{mode}.txt"
with open(f"{process}_{year}_{mode}.txt", "w") as f:
    for root_file in root_files:
        f.write(root_file) 
ana = XHY4b_Analyzer(f"{process}_{year}_{mode}.txt", year, 10000000, 0)

ana.process = process
ana.subprocess = process
if "MC" in dataset:
    ana.isData = 0
else:
    ana.isData = 1
bins = [{"leadingFatJetPt":array.array("d", np.linspace(0, 3000, 301)), "MX": array.array("d", np.linspace(0, 5000, 501) ) }]

file_basename = os.path.basename(dataset).removesuffix(".txt")
ana.output = file_basename + f"_all.root"
#Saving the histograms to the "Templates" root file
f = ROOT.TFile("Templates_" + ana.output, "RECREATE")
'''
if "MC" in ana.dataset:
    ana.make_TH2(bins, ["weight_All__nominal"], f, "beforetrigger")
else:
    ana.make_TH2(bins, [], f, "beforetrigger")
'''
ana.make_TH2(bins, [], f, "beforetrigger")
ana.add_trigger(triggers)
'''
if "MC" in ana.dataset:
    print("MC")
    ana.make_TH2(bins, ["weight_All__nominal"], f, "aftertrigger")
else:
    print("DATA")
    ana.make_TH2(bins, [], f, "aftertrigger")
'''
ana.make_TH2(bins, [], f, "aftertrigger")
f.Close()
exit()















