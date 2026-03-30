import ROOT
import numpy as np
ROOT.gROOT.SetBatch(True)
g = ROOT.TGraph2D()

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--smooth', action='store_true')
args = parser.parse_args()
if args.smooth:
    with open(f"best_scores_discrete_{args.mode}_smooth.txt", "r") as _f:
        lines = _f.readlines()
else:
    with open(f"best_scores_discrete_{args.mode}.txt", "r") as _f:
        lines = _f.readlines()
MXs = [float(line.split()[0]) for line in lines]
MYs = [float(line.split()[1]) for line in lines]
scores = [float(line.split()[2]) for line in lines]
if args.mode == "2p1":
    MXs_new = [MXs[i] for i in range(len(scores)) if MXs[i] > MYs[i] + 300 and MXs[i] > 300]
    MYs_new = [MYs[i] for i in range(len(scores)) if MXs[i] > MYs[i] + 300 and MXs[i] > 300]
    scores_new = [scores[i] for i in range(len(scores)) if MXs[i] > MYs[i] + 300 and MXs[i] > 300]
    #MXs_new = [MXs[i] for i in range(len(scores)) if scores[i] > 0.75]
    #MYs_new = [MYs[i] for i in range(len(scores)) if scores[i] > 0.75]
    #scores_new = [scores[i] for i in range(len(scores)) if scores[i] > 0.75]
    MXs = MXs_new
    MYs = MYs_new
    scores = scores_new
for i in range(len(scores)):
    g.SetPoint(i, MXs[i], MYs[i], scores[i])
if args.mode == "1p1":
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
if args.mode == "2p1":
    f2 = ROOT.TF2(
        "f2",
        #"1.73/(1+exp( [4] * (sqrt( (x - [0]) * (x - [0]) / [1] / [1]  + (y - [2]) * (y - [2]) / [3] / [3]) - [5] ) ) ) - 0.88",
        #"1.85/(1+exp( [4] * (sqrt( (x - [0]) * (x - [0]) / [1] / [1]  + (y - [2]) * (y - [2]) / [3] / [3]) - 1 ) ) ) - 0.88",
        #"1.75/(1+exp( [4] * ( (x - [0]) * (x - [0]) / [1] / [1]  + (y - [2]) * (y - [2]) / [3] / [3] - 1 ) ) ) - 0.88",
        #"1.87/(1+exp(- [5] /x * ( [0] + [1]*x+[2]*y + [3]*x*x + [4]*y*y ))) - 0.88",
        #"1.45/(1+exp(- [5] /x * ( [0] + [1]*x+[2]*y + [3]*x*x + [4]*y*y ))) - 0.5",
        "1.5/(1+exp(- [5] /x * ( [0] + [1]*x+[2]*y + [3]*x*x + [4]*y*y ))) - 0",
        #"( ([0]*x + [1]*y + [2] + [3]*y*y) / (1 + abs([0]*x + [1]*y + [2]+ [3]*y*y)))",
        #"1.99/(1+exp(-([0]*x+[1]*y+[2] + [3]*y*y))) - 1",
        #"1.99/(1+exp(- [5] /x * ([0]*x+[1]*y+[2] + [3]*y*y + [4]*x*x ))) - 1",
        #"0.14/(1+exp(- [5] /x * ( [0] + [1]*x+[2]*y + [3]*x*x + [4]*y*y ))) + 0.78",
        #"6.3/(1+exp(- [5]  * ( [0] + [1]*x+[2]*y + [3]*x*x + [4]*y*y ))) + 0.3",
        #"1.8/(1+exp(- [5] /x  * ( 240000 + [1]*x+[2]*y + [3]*x*x + [4]*y*y ))) - 1",
        #"0.82 * exp(-([0] + [1]*x+[2]*y + [3]*x*x + [4]*y*y)) - 1",
        #"1.8/(1+exp( [4] * (sqrt( (x - [0]) * (x - [0]) / [1] / [1]  + (y - [2]) * (y - [2]) / [3] / [3]) - [5] ) ) ) - 1",
        #"min([0] + [1] * x + [2] * y +[3] *x*x +[4] *y*y + [5] *x*y, 0.9)",
        #"max(0.8, [4] * exp(-( (x - [0]) * (x - [0]) / [1] / [1]  + (y - [2]) * (y - [2]) / [3] / [3]) ) - 1)",
        #"exp(-( (x - [0]) * (x - [0]) / [1] / [1]  + (y - [2]) * (y - [2]) / [3] / [3]) * ( (x - [0]) * (x - [0]) / [1] / [1]  + (y - [2]) * (y - [2]) / [3] / [3]) ) - 1",
        #"0.33/(1+exp(- [5] /log(x) * ( [0] + [1]*log(x)+[2]*log(y) + [3]*log(x)*log(x) + [4]*log(y)*log(y) ))) + 0.6 ",
        #"0.27/(1+exp(- [5]/ log(x)  * ( [0] + [1]*log(x)+[2]*log(y) + [3]*log(x)*log(x) + [4]*log(y)*log(y) ))) + 0.65 ",
        #"0.27/(1+exp(- [5] / log(x)  * ( [0] + [1]*log(x)+[2]*log(y) + [3]*log(x)*log(x) + [4]*log(y)*log(y) ))) + 0.65 ",
        #"0.17/(1+exp(- [2] * ( 1 + [0]*x+[1]*y  ))) + 0.75 ",
        #"1.99/(1+exp(- [5] /x * ( [0] + [1]*x+[2]*y  ))) - 1",
        #"1.99/(1+exp(-  ( [0] + [1]*x+[2]*y  ))) - 1",
        #" [0] + [1]*x+[2]*y ",
        #"( ([0] + [1]*y + [2]) / (1 + abs([0] + [1]*y + [2])))",
        200, 4000, 210, 3500
    )
f2.SetParameters(10, -0.001, -0.001, 0, 0)
#f2.SetParameters(1000, 500, 200, 200, 1, 11)
#f2.SetParameters(1500, 500, 0, 500, 0.01 , 1)
#f2.SetParameters(1, -0.00120, -0.00200, 0, 0, 0)
#f2.SetParameters( -0.0004, -0.0004, 10 )
g.Fit(f2, "R")
c = ROOT.TCanvas("c", "c")
g.Draw("PCOL")
f2.Draw("SAME CONT3")
#f2.Draw("CONT3")
c.Update()
c.Print(f"fit_score_discrete_{args.mode}.png")

with open(f"DDT_map_para_discrete_{args.mode}.txt", "w") as _f: 
    for i in range(f2.GetNpar()):
        print(f2.GetParameter(i))
        _f.write(f"{f2.GetParameter(i)}\n")
    

with open(f"fitted_score_discrete_{args.mode}.txt", "w") as _f:
    for i in range(len(scores)):
        _f.write(f"{MXs[i]} {MYs[i]} {f2.Eval(MXs[i], MYs[i])} \n")
        
        
