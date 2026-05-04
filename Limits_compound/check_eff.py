'''
TTBAR_PASS_SF rateParam SB* *TTBar* 1 [0.5,2]
'''
import ROOT

from argparse import ArgumentParser
import os

#Reading input args
parser=ArgumentParser()
parser.add_argument('--eff_file', type=str, dest='eff_file',action='store', required=True)
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

    #print(f_card.readlines())
QCD_PASS = f.Get(f"Allyears__MC_QCDJets__{Reg}_SR1_{mode}__nominal")
QCD_FAIL = f.Get(f"Allyears__MC_QCDJets__{Reg}_SB1_{mode}__nominal")
print(QCD_PASS.Integral(), QCD_FAIL.Integral())
print(QCD_PASS.Integral()/ QCD_FAIL.Integral())
if "Sig" not in args.eff_file:
    JetMET_PASS = f.Get(f"Allyears__JetMET__{Reg}_SR1_{mode}__nominal")
    JetMET_FAIL = f.Get(f"Allyears__JetMET__{Reg}_SB1_{mode}__nominal")
    print(JetMET_PASS.Integral(), JetMET_FAIL.Integral())
    print(JetMET_PASS.Integral()/ JetMET_FAIL.Integral())
#TTBar_PASS = f.Get("Allyears__SignalMC_MX-3000_MY-300__SR1_1p1__nominal")
#TTBar_FAIL = f.Get("Allyears__SignalMC_MX-3000_MY-300__SB1_1p1__nominal")
#eff = TTBar_PASS.Integral() / (TTBar_PASS.Integral() + TTBar_FAIL.Integral())
#print(eff)
