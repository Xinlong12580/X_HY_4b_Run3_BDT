import ROOT
import numpy as np
ROOT.gROOT.SetBatch(True)
g = ROOT.TGraph2D()

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()
with open(f"best_scores_{args.mode}.txt", "r") as _f:
    lines = _f.readlines()
MXs = [float(line.split()[0]) for line in lines]
MYs = [float(line.split()[1]) for line in lines]
scores = [float(line.split()[2]) for line in lines]
for i in range(len(scores)):
    g.SetPoint(i, MXs[i], MYs[i], scores[i])

f2 = ROOT.TF2(
    "f2",
    #"( ([0]*x + [1]*y + [2]) / (1 + abs([0]*x + [1]*y + [2])))",
    #"( ([0]*x + [1]*y + [2] + [3]*y*y) / (1 + abs([0]*x + [1]*y + [2]+ [3]*y*y)))",
    #"1.99/(1+exp(-([0]*x+[1]*y+[2] + [3]*y*y))) - 1",
    #"1.99/(1+exp(- [5] /x * ([0]*x+[1]*y+[2] + [3]*y*y + [4]*x*x ))) - 1",
    "1.99/(1+exp(- [5] /x * ( [0] + [1]*x+[2]*y + [3]*x*x + [4]*y*y ))) - 1",
    #"( ([0] + [1]*y + [2]) / (1 + abs([0] + [1]*y + [2])))",
    200, 4000, 40, 3500
)
f2.SetParameters(10, 0, -0.01, 0, 0)
g.Fit(f2, "R")
c = ROOT.TCanvas("c", "c")
g.Draw("PCOL")
f2.Draw("SAME CONT3")
#f2.Draw("CONT3")
c.Update()
c.Print(f"fit_score_{args.mode}.png")

with open(f"DDT_map_para_{args.mode}.txt", "w") as _f: 
    for i in range(f2.GetNpar()):
        print(f2.GetParameter(i))
        _f.write(f"{f2.GetParameter(i)}\n")
    

with open(f"fitted_score_{args.mode}.txt", "w") as _f:
    for i in range(len(scores)):
        _f.write(f"{MXs[i]} {MYs[i]} {f2.Eval(MXs[i], MYs[i])} \n")
        
        
