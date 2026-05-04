import ROOT
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f', action='store', required=True)
args = parser.parse_args()
    
f = ROOT.TFile.Open(args.f, "UPDATE")
for key in f.GetListOfKeys():
    h = key.ReadObj()
    if "2024__" in h.GetName() and "TTBar" in h.GetName() and "SB1" in h.GetName():
    #if "Allyears" in h.GetName() and "TTBar" in h.GetName() and "SB1" in h.GetName():
        print(h.GetName(), h.Integral()) 
