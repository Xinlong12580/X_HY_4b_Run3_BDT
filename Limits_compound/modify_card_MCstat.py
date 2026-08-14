'''
TTBAR_PASS_SF rateParam SB* *TTBar* 1 [0.5,2]
'''
import ROOT

from argparse import ArgumentParser
import os

#Reading input args
parser=ArgumentParser()
parser.add_argument('--stat_file', type=str, dest='stat_file',action='store', required=True)
parser.add_argument('--card_file', type=str, dest='card_file',action='store', required=True)
args = parser.parse_args()

if "1p1" in args.stat_file:
    mode =  "1p1"
if "2p1" in args.stat_file:
    mode =  "2p1"

if "Signal" in args.stat_file:
    Reg = "SR"
if "Validation" in args.stat_file:
    Reg = "VR"
if "Control" in args.stat_file:
    Reg = "CR"
f = ROOT.TFile.Open(args.stat_file,"READ")



with open(args.card_file, "r") as f_card:
    lines = [line for line in f_card if ("MCstat" not in line)]


with open(args.card_file, "w") as f_card:
    f_card.writelines(lines)


for line in lines:
    if line.startswith("process") and "MC" in line:
        process_columns = line.split()[1:]
        print(process_columns)
    if line.startswith("bin") and "SR" in line:
        bin_columns = line.split()[1:]
        print(bin_columns)
count = 0
for key in f.GetListOfKeys():
    hist = key.ReadObj()
    hist_name  = hist.GetName()
    if ("down" in hist_name): continue
    syst_name = hist_name[hist_name.find("MCstat"):hist_name.find("_up")] 
    syst_line = syst_name + " shapes "
    for i in range(len(process_columns)):
        if "TTBar" in process_columns[i] and (("SR1" in bin_columns[i] and "SR1" in syst_name) or ("SB1" in bin_columns[i] and "SB1" in syst_name)):
            syst_line = syst_line + " 1.0 "
        else:
            syst_line = syst_line + " - "
    print(syst_line)
    count += 1
    with open(args.card_file, "a") as f_card:
        f_card.write(syst_line + "\n")
print("Total added systs:", count)
with open(args.card_file, "r") as f_card:
    lines = f_card.readlines()
    kmax = len([line for line in lines if ( ("shape" in line or "lnN" in line ) and (not line.startswith("shapes")) )]) 
    lines[2] = f"kmax {kmax}\n"
print(kmax)
 

with open(args.card_file, "w") as f_card:
    f_card.writelines(lines)
