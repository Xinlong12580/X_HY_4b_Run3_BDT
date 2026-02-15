import ROOT
import re
import numpy as np
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
parser.add_argument('-b', type=str, dest='b',action='store', default="datasets/BKGs_1p1_ALL.root")
args = parser.parse_args()

BKG_file = args.b
mx_match = re.search(r"MX-(\d+)", args.f)
my_match = re.search(r"MY-(\d+)", args.f)

MX = int(mx_match.group(1))
MY = int(my_match.group(1))
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
    #winsize_mx = max(MX * 0.4, 100)
    #winsize_my = max(MY * 0.4, 100)
    #winsize_mx = 200
    #winsize_my = 50


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
print(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}")
print(f"MX > {MX - winsize_mx} && MX < {MX + winsize_mx} && MY > {MY - winsize_my} && MY < {MY + winsize_my}")
print(sig_rdf.Sum("BDT_weight").GetValue())
print(bkg_rdf.Sum("BDT_weight").GetValue(),  bkg_rdf.Count().GetValue())

scores = np.linspace(-1, 1, 201) 

#N_total_sig = sig_rdf.Sum("BDT_weight").GetValue()
#N_total_bkg = bkg_rdf.Sum("BDT_weight").GetValue()
sig2bkgs = []
for score in scores:
    N_sig = sig_rdf.Filter(f"BDTG > {score}").Sum("BDT_weight").GetValue()
    N_bkg = bkg_rdf.Filter(f"BDTG > {score}").Sum("BDT_weight").GetValue()
    sig2bkg = N_sig / (1 + np.sqrt(N_bkg))
    #sig2bkg = N_sig / np.sqrt(N_bkg)
    sig2bkgs.append(sig2bkg)
ind = sig2bkgs.index(max(sig2bkgs))
best_score = scores[ind]

print(sig2bkgs)
print(best_score)
