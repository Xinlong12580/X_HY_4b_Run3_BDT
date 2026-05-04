'''
TTBAR_PASS_SF rateParam SB* *TTBar* 1 [0.5,2]
'''
import ROOT

from argparse import ArgumentParser
import os

#Reading input args
parser=ArgumentParser()
parser.add_argument('--eff_file', type=str, dest='eff_file',action='store', required=True)
parser.add_argument('--card_file', type=str, dest='card_file',action='store', required=True)
parser.add_argument('--fail_name', type=str, dest='fail_name',action='store', required=True)
parser.add_argument('--pass_name', type=str, dest='pass_name',action='store', required=True)
args = parser.parse_args()

if "1p1" in args.eff_file:
    mode =  "1p1"
if "2p1" in args.eff_file:
    mode =  "2p1"

if "Signal" in args.eff_file:
    Reg = "SR"
if "Validation" in args.eff_file:
    Reg = "VR"
if "Control" in args.eff_file:
    Reg = "CR"
f = ROOT.TFile.Open(args.eff_file,"READ")

TTBar_PASS = f.Get(f"Allyears__MC_TTBarJets__{Reg}_SR1_{mode}__nominal")
TTBar_FAIL = f.Get(f"Allyears__MC_TTBarJets__{Reg}_SB1_{mode}__nominal")
print(TTBar_PASS.Integral(), TTBar_FAIL.Integral())
eff = TTBar_PASS.Integral() / (TTBar_PASS.Integral() + TTBar_FAIL.Integral())
print(f"efficiency from {args.eff_file}", eff)
with open(args.card_file, "r") as f_card:
    lines = [line for line in f_card if (("TTBAR_PASS_SF" not in line) and ("TTBAR_FAIL_SF" not in line))]
with open(args.card_file, "w") as f_card:
    f_card.writelines(lines)

with open(args.card_file, "a") as f_card:
    f_card.write(f"TTBAR_PASS_SF_{args.pass_name} rateParam *SR* *TTBar* 1 [0.5,2]\n")
    f_card.write(f"TTBAR_FAIL_SF_{args.fail_name} rateParam *SB* *TTBar* (1-{eff:.4f}*@0/({1-eff:.4f})) TTBAR_PASS_SF_{args.pass_name}\n")    
    #print(f_card.readlines())
QCD_PASS = f.Get(f"Allyears__MC_QCDJets__{Reg}_SR1_{mode}__nominal")
QCD_FAIL = f.Get(f"Allyears__MC_QCDJets__{Reg}_SB1_{mode}__nominal")
print(QCD_PASS.Integral(), QCD_FAIL.Integral())
if "Control" in args.eff_file:
    JetMET_PASS = f.Get(f"Allyears__JetMET__{Reg}_SR1_{mode}__nominal")
    JetMET_FAIL = f.Get(f"Allyears__JetMET__{Reg}_SB1_{mode}__nominal")
    print(JetMET_PASS.Integral(), JetMET_FAIL.Integral())
#TTBar_PASS = f.Get("Allyears__SignalMC_MX-3000_MY-300__SR1_1p1__nominal")
#TTBar_FAIL = f.Get("Allyears__SignalMC_MX-3000_MY-300__SB1_1p1__nominal")
#eff = TTBar_PASS.Integral() / (TTBar_PASS.Integral() + TTBar_FAIL.Integral())
#print(eff)
