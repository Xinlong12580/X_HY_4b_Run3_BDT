import ROOT
from argparse import ArgumentParser
import os
#Reading input args

parser=ArgumentParser()
parser.add_argument('--input_file', type=str, dest='input_file',action='store', required=True)
parser.add_argument('--target_file', type=str, dest='target_file',action='store', required=True)
args = parser.parse_args()
if "1p1" in args.input_file:
    mode = "1p1"
elif "2p1" in args.input_file:
    mode = "2p1"

def Compatible_RDH(A, B ):
    nA = A.numEntries()
    nB = B.numEntries()
    if nA != nB:
        print("number of entries doesn't match")
        return 0
    obsA = A.get() 
    obsB = B.get() 
    diff_weight = 0
    for i in range(nA):
        A.get(i)
        B.get(i)

        coordsA = {var.GetName(): var.getVal() for var in obsA}
        coordsB = {var.GetName(): var.getVal() for var in obsB}

        weightA = A.weight()
        weightB = B.weight()
        #print(i, coordsA, coordsB, weightA, weightB)
        for axis in coordsA:
            if abs(coordsA[axis] - coordsB[axis]) > 1e-3:
                print("bin edge doesn't match")
                print(i, coordsA, coordsB, weightA, weightB)
                return 0
        if abs(weightA - weightB) > 1e-3:
            print("Warning: Different weights: ", i, coordsA, coordsB, weightA, weightB)
            diff_weight += 1
        #if diff_weight >= 2:
        #    print("more than one bin with different weights")
        #    return 0
    return 1







input_file = ROOT.TFile.Open(args.input_file, "READ")

target_file = ROOT.TFile.Open(args.target_file, "UPDATE")

w = target_file.Get("w")

passed = 0
for key in input_file.GetListOfKeys():
    hist = key.ReadObj()
    #hist.Print()
    
    MJY_var = w.var(f"M_JY_Region0_B_{mode}")
    MJJ_var = w.var(f"M_JJ_B_{mode}")
    #MJY_var.Print()    
    #MJJ_var.Print()    
    rdh = ROOT.RooDataHist(
        hist.GetName().replace("_up", "Up").replace("_down", "Down"),
        hist.GetTitle().replace("_up", "Up").replace("_down", "Down"),
        ROOT.RooArgList(MJY_var, MJJ_var),
        ROOT.RooFit.Import(hist)
    )
    
    if passed == 0:
        hist_name = hist.GetName()
        reference_name = hist_name[:hist_name.find("_MCstat")]
        reference = w.data(reference_name)
        print(reference_name)
        passed = Compatible_RDH(rdh, reference)
        if passed == 0:
            raise ValueError("Input TH2 not compatible with the RDH already in the workspace. Abort.")
    getattr(w, "import")(rdh)




w.Write()
input_file.Close()
target_file.Close()
