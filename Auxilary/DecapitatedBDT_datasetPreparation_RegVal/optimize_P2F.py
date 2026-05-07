import ROOT
import psutil
import re
import os
import numpy as np
from argparse import ArgumentParser
import math
parser=ArgumentParser()
parser.add_argument('--MX', type=float, dest='MX',action='store', required=True)
parser.add_argument('--MY', type=float, dest='MY',action='store', default="datasets/BKGs_1p1_ALL.root")
parser.add_argument('-b', type=str, dest='b',action='store', default="datasets/BKGs_1p1_ALL.root")
parser.add_argument('--expr', type=str, dest='expr',action='store', default="(1.75e-6 * exp(0.0017 * x) + 4.48e-4) ")
args = parser.parse_args()

BKG_file = args.b

MX = args.MX
MY = args.MY

window_ratio = 0.25
min_count = 40000
bkg_rdf = ROOT.RDataFrame("Events", BKG_file)
bkg_rdf = bkg_rdf.Filter("event_Idx%2 == 1")

for i in range(1, 40):
    winsize_mx = i * 100
    winsize_my = winsize_mx * window_ratio
    if (bkg_rdf.Filter(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}").Count().GetValue() > min_count):        break

winsize_mx_base = winsize_mx - 100
for i in range(0, 10):
    winsize_mx = winsize_mx_base  + i * 10
    winsize_my = winsize_mx * window_ratio
    if (bkg_rdf.Filter(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}").Count().GetValue() > min_count):        break
print("WinSize: ", winsize_mx, winsize_my)
    


bkg_rdf = bkg_rdf.Filter(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}")
TTBar_rdf = bkg_rdf.Filter("sample_ID == 1")
QCD_rdf = bkg_rdf.Filter("sample_ID == 2")
print(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}")
print(bkg_rdf.Sum("BDT_weight").GetValue(),  bkg_rdf.Count().GetValue())

scores = np.linspace(0.5, 1, 501) 

QCDPtoFs = []
QCDPtoFs_events = []
N_bkg_total = bkg_rdf.Sum("BDT_weight").GetValue() 
N_TTBar_total = TTBar_rdf.Sum("BDT_weight").GetValue() 
N_QCD_total = QCD_rdf.Sum("BDT_weight").GetValue()
N_QCD_total_events = QCD_rdf.Count().GetValue()
print("N_QCD_total", N_QCD_total)
for score in scores:
    #N_bkg = bkg_rdf.Filter(f"BDTG > {score}").Sum("BDT_weight").GetValue() * lumi_total / lumi
    #N_TTBar = TTBar_rdf.Filter(f"BDTG > {score}").Sum("BDT_weight").GetValue() * lumi_total / lumi
    #N_QCD = QCD_rdf.Filter(f"BDTG > {score}").Sum("BDT_weight").GetValue() * lumi_total / lumi

    ###############There is memory leak here for some reason. Doing it in the verbose way below saves same memory and speed up the running for some reason 
    weight = "BDT_weight" 
    cut = f"BDTG > {score}"
    rdfN_QCD = QCD_rdf.Filter(cut).Sum(weight)
    N_QCD = rdfN_QCD.GetValue() 
    rdfN_QCD_events = QCD_rdf.Filter(cut).Count()
    N_QCD_events = rdfN_QCD_events.GetValue() 
    import gc; gc.collect()
    QCDPtoFs.append(N_QCD/(N_QCD_total - N_QCD) if (N_QCD_total - N_QCD) != 0 else float('nan') )
    QCDPtoFs_events.append(N_QCD_events/(N_QCD_total_events - N_QCD_events) if (N_QCD_total_events - N_QCD_events) != 0 else float('nan') )
    process = psutil.Process(os.getpid())
    print(f"Memory usage: {process.memory_info().rss / 1024**2:.2f} MB")
    
##################################################################################################
ind_up = 0
f2 = ROOT.TF2("f2", args.expr, 0, 5000, 0, 5000)
thres_P2F = f2.Eval(MX, MY)
for i in range(len(QCDPtoFs)):
    if QCDPtoFs[i] <= thres_P2F:
        ind_up = i
        break
ind = ind_up
ind_down = max(ind_up - 1, 0)
distance_up = thres_P2F - QCDPtoFs[ind_up]  
distance_down = thres_P2F - QCDPtoFs[ind_down]  
distance = distance_down - distance_up
print("Goal: ", thres_P2F, "ind_up: ",  ind_up, "P2F_up: ", QCDPtoFs[ind_up], "ind_down: ",  ind_down, "P2F_down: ", QCDPtoFs[ind_down], "distances: ", distance_up, distance_down, "scores: ", scores[ind_up], scores[ind_down])
if distance == 0 or math.isnan(distance):
    best_score = scores[ind]
    QCDPtoF = QCDPtoFs[ind]
else: 
    best_score = (scores[ind_up] * distance_down - scores[ind_down] * distance_up) / distance
    QCDPtoF = (QCDPtoFs[ind_up] * distance_down - QCDPtoFs[ind_down] * distance_up) / distance
##################################################################################################
print("QCDPtoFs", QCDPtoFs)
print("Events_ratio", QCDPtoFs_events)

print("best_score", best_score)
print("best_sig2bkg", "nan")
print("best_sigEff", "nan")
print("best_bkgEff", "nan")
print("best_TTBarEff", "nan")
print("best_QCDEff", "nan")
print("best_QCDPtoF", QCDPtoF)
