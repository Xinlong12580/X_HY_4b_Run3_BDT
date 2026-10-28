import ROOT
from argparse import ArgumentParser
from XHY4b_Helper import *
import array
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f', action='store', required=True)
parser.add_argument('--mx', type=str, dest='mx', action='store', required=True)
parser.add_argument('--my', type=str, dest='my', action='store', required=True)
parser.add_argument('--year', type=str, dest='year', action='store', required=True)
parser.add_argument('--recreate',  action='store_true')
args = parser.parse_args()
if "1p1" in args.f:
    mode = "1p1"
elif "2p1" in args.f:
    mode = "2p1"
if "Signal" in args.f:
    Reg = "SR"
if "Validation" in args.f:
    Reg = "VR"
if "Control" in args.f:
    Reg = "CR"
if mode == "1p1":
    MJY_bins = array.array("d", [0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.3, 0.4, 0.5, 1.0])
    MJJ_bins = array.array("d", [0.8, 0.9, 1.0,  1.2, 1.4, 1.7, 2.0, 2.5, 3.0, 5.0] )
elif mode == "2p1":
    #MJY_bins = array.array("d", [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0])
    #MJJ_bins = array.array("d", [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.7, 2.0, 2.5, 3.0, 4.0, 5.0] )
    MJY_bins = array.array("d", [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 2.0, 2.5, 3.0, 4.0])
    MJJ_bins = array.array("d", [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 2.0, 2.5, 3.0, 5.0] )


f = ROOT.TFile.Open(args.f, "READ")

print("REBINNING###############################################################")
open_method = "RECREATE" if args.recreate else "UPDATE"
f_out = ROOT.TFile.Open(args.f.replace(".root", "_rebinned.root"), open_method)
for key in f.GetListOfKeys():
    if not key.GetName().startswith(args.year + "__"): continue
    if not ("TTBar" in key.GetName() or "SignalMC" in key.GetName() or ("JetMET" in key.GetName() and "nominal" in key.GetName() ) ):
        continue
    hist = key.ReadObj()
    print("rebinning ", hist.GetName())
    if "TTBar" in key.GetName() and (key.GetName().startswith("2024_") or key.GetName().startswith("Allyears_")): 
        hist = rebin_TH2(hist,  MJY_bins, MJJ_bins, "rebinned_" + hist.GetName(), forceOutputPositive = True, outputFloor = 2)
    else:
        hist = rebin_TH2(hist,  MJY_bins, MJJ_bins, "rebinned_" + hist.GetName(), forceOutputPositive = True, outputFloor = 0)
    hist.SetDirectory(f_out)
    hist.Write()


f.Close()
f_out.Close()
