import ROOT
import psutil
import re
import os
import numpy as np
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
parser.add_argument('-b', type=str, dest='b',action='store', default="datasets/BKGs_1p1_ALL.root")
parser.add_argument('--method', type=int, dest='method',action='store', default=1) #0: optimize punzi significance #1: set continuousefficiency
parser.add_argument('--expr', type=str, dest='expr',action='store', default="( ( x < 2000 ) * 0.0005 + ( x >= 2000 ) * ( ( x - 2000 ) / (4000 - 2000) * ( 0.006 - 0.0005 ) + 0.0005 ) ) * ( y > 0 )")
args = parser.parse_args()
lumi_dict = {
    "2022": 7980.454151,
    "2022EE": 26671.609707000002,
    "2023": 18062.659110999995,
    "2023BPix": 9693.130053000003,
    "2024": 109987.998903 
}
lumi_total = 0
lumi = 0
years = ["2022", "2022EE", "2023", "2023BPix", "2024"]
for year in years:
    lumi_total += lumi_dict[year]
    if (year + "_") in args.f:
        lumi += lumi_dict[year]
BKG_file = args.b
mx_match = re.search(r"MX-(\d+)", args.f)
my_match = re.search(r"MY-(\d+)", args.f)

MX = int(mx_match.group(1))
MY = int(my_match.group(1))
'''
if "1p1" in args.f:
    winsize_mx = 500
    winsize_my = 100
elif "2p1" in args.f:
    xbins = [300, 400, 500, 600, 700, 800,900,1000, 1200, 1500, 2000,3000,4000, 5000] 
    ybins = [200,  300, 400, 500, 600, 700, 800, 900,1000, 1200, 1500, 2000, 3000, 4000, 5000]
    if MY <= 200:
        winsize_mx = 200
        winsize_my = 100
    else:
        for i in range(len(xbins)):
            if xbins[i] >= MX:
                winsize_mx = 0.5 * (xbins[i] - xbins[i-1])
                break
        for i in range(len(ybins)):
            if ybins[i] >= MY:
                winsize_my = 0.5 * (ybins[i] - ybins[i-1])
                break
    #winsize_mx = max(MX * 0.2, 100)
    #winsize_my = max(MY * 0.2, 100)
    #winsize_mx = 200
    #winsize_my = 50
'''
if args.method == 0:
    winsize_mx = min(max(MX * 0.1, 50), 200)
    winsize_my = min(max(MY * 0.1, 50), 200)
elif args.method == 1:
    winsize_mx = max(MX * 0.2, 50)
    winsize_my = max(MY * 0.2, 50)

sig_rdf = ROOT.RDataFrame("Events", args.f)
bkg_rdf = ROOT.RDataFrame("Events", BKG_file)

print(sig_rdf.Mean("MX").GetValue())
print(sig_rdf.StdDev("MX").GetValue())
#sig_rdf = sig_rdf.Filter(f"PNet_H > 0.3 && PNet_Ymin > 0.3 && PNet_Y > 0.3")
#bkg_rdf = bkg_rdf.Filter(f"PNet_H > 0.3 && PNet_Ymin > 0.3 && PNet_Y > 0.3")
print(sig_rdf.Mean("MY").GetValue())
print(sig_rdf.StdDev("MY").GetValue())
print(sig_rdf.Sum("BDT_weight").GetValue())
print(bkg_rdf.Sum("BDT_weight").GetValue(), bkg_rdf.Count().GetValue())
sig_rdf = sig_rdf.Filter(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}")
bkg_rdf = bkg_rdf.Filter(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}")
TTBar_rdf = bkg_rdf.Filter("sample_ID == 1")
QCD_rdf = bkg_rdf.Filter("sample_ID == 2")
print(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}")
print(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}")
print(sig_rdf.Sum("BDT_weight").GetValue())
print(bkg_rdf.Sum("BDT_weight").GetValue(),  bkg_rdf.Count().GetValue())

scores = np.linspace(0, 1, 201) 

#N_total_sig = sig_rdf.Sum("BDT_weight").GetValue()
#N_total_bkg = bkg_rdf.Sum("BDT_weight").GetValue()
sig2bkgs = []
bkgEffs = []
sigEffs = []
QCDEffs = []
TTBarEffs = []
QCDPtoFs = []
N_sig_total = sig_rdf.Sum("BDT_weight").GetValue() * lumi_total / lumi 
N_bkg_total = bkg_rdf.Sum("BDT_weight").GetValue() * lumi_total / lumi
N_TTBar_total = TTBar_rdf.Sum("BDT_weight").GetValue() * lumi_total / lumi
N_QCD_total = QCD_rdf.Sum("BDT_weight").GetValue() * lumi_total / lumi
for score in scores:
    #N_sig = sig_rdf.Filter(f"BDTG > {score}").Sum("BDT_weight").GetValue() * lumi_total / lumi
    #N_bkg = bkg_rdf.Filter(f"BDTG > {score}").Sum("BDT_weight").GetValue() * lumi_total / lumi
    #N_TTBar = TTBar_rdf.Filter(f"BDTG > {score}").Sum("BDT_weight").GetValue() * lumi_total / lumi
    #N_QCD = QCD_rdf.Filter(f"BDTG > {score}").Sum("BDT_weight").GetValue() * lumi_total / lumi

    ###############There is memory leak here for some reason. Doing it in the verbose way below saves same memory and speed up the running for some reason 
    weight = "BDT_weight" 
    cut = f"BDTG > {score}"
    rdfN_sig = sig_rdf.Filter(cut).Sum(weight)
    rdfN_bkg = bkg_rdf.Filter(cut).Sum(weight)
    rdfN_TTBar = TTBar_rdf.Filter(cut).Sum(weight)
    rdfN_QCD = QCD_rdf.Filter(cut).Sum(weight)
    N_sig = rdfN_sig.GetValue() * lumi_total / lumi
    N_bkg = rdfN_bkg.GetValue() * lumi_total / lumi
    N_TTBar = rdfN_TTBar.GetValue() * lumi_total / lumi
    N_QCD = rdfN_QCD.GetValue() * lumi_total / lumi
    #del rdfN_sig
    #del rdfN_bkg
    #del rdfN_TTBar
    #del rdfN_QCD 
    import gc; gc.collect()
    sig2bkg = N_sig / (1 + np.sqrt(N_bkg))
    sig2bkgs.append(sig2bkg)
    bkgEffs.append(N_bkg/N_bkg_total if N_bkg_total != 0 else float('nan'))
    TTBarEffs.append(N_TTBar/N_TTBar_total if N_TTBar_total != 0 else float('nan') )
    QCDEffs.append(N_QCD/N_QCD_total if N_QCD_total != 0 else float('nan') )
    QCDPtoFs.append(N_QCD/(N_QCD_total - N_QCD) if (N_QCD_total - N_QCD) != 0 else float('nan') )
    sigEffs.append(N_sig/N_sig_total if N_sig_total != 0 else float('nan') )
    process = psutil.Process(os.getpid())
    print(f"Memory usage: {process.memory_info().rss / 1024**2:.2f} MB")
    
##################################################################################################
ind = 0
if args.method == 0:
    ind = sig2bkgs.index(max(sig2bkgs))
elif args.method == 1: 
    f2 = ROOT.TF2("f2", args.expr, 0, 5000, 0, 5000)
    thres_P2F = f2.Eval(MX, MY)
    for i in range(len(QCDPtoFs)):
        if QCDPtoFs[i] <= thres_P2F:
            ind = i
            break
##################################################################################################
best_score = scores[ind]
sigEff = sigEffs[ind]
bkgEff = bkgEffs[ind]
QCDEff = QCDEffs[ind]
TTBarEff = TTBarEffs[ind]
sig2bkg = sig2bkgs[ind]
QCDPtoF = QCDPtoFs[ind]
print(ind)
print("sigEffs", sigEffs)
print("bkgEffs", bkgEffs)
print("TTBarEffs", TTBarEffs)
print("QCDEffs", QCDEffs)
print("QCDPtoFs", QCDPtoFs)
print("sig2bkgs", sig2bkgs)

print("best_score", best_score)
print("best_sig2bkg", sig2bkg)
print("best_sigEff", sigEff)
print("best_bkgEff", bkgEff)
print("best_TTBarEff", TTBarEff)
print("best_QCDEff", QCDEff)
print("best_QCDPtoF", QCDPtoF)
