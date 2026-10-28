import ROOT
import numpy as np
plot_dir = "./"
ROOT.gROOT.SetBatch(True)
import ROOT
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
parser.add_argument('-r', type=float, dest='r',action='store', required=True)
parser.add_argument('--title', type=str, dest='title',action='store', required=True)
args = parser.parse_args()
with open("outputList/output_SI_BDT.txt", "r") as _f:
    SIs = _f.readlines()
f_string = args.f.replace("/", "_")

r_truth = args.r

truth_function = "exp"
fit_function = "poly"

name = "truth_%s_fit_%s" % (truth_function, fit_function)
hist_pull = ROOT.TH1F("pull_%s" % name, "Pull distribution: truth=%s, fit=%s" % (truth_function, fit_function), 100, -10, 10)
hist_pull.GetXaxis().SetTitle("Pull = (r_{truth}-r_{fit})/#sigma_{fit}")
hist_pull.GetYaxis().SetTitle("Entries")


N_neg  =0
N_pos = 0
for SI in SIs:
    SI=SI.strip()
    if f_string not in SI or "123456" in SI or f"r_{int(r_truth)}." not in SI or "MultiDimFit" not in SI:
        continue
    print(f_string)
    print(SI)
    # Open file with fits
    f = ROOT.TFile.Open(SI)
    t = f.Get("limit")

    N_toys = int(t.GetEntries() / 3) 

    sigma_values = np.array([])

    for i_toy in range(N_toys):
        # Best-fit value
        t.GetEntry(i_toy * 3)
        r_fit = getattr(t, "r")
                
        # -1 sigma value
        t.GetEntry(i_toy * 3 + 1)
        r_lo = getattr(t, "r")
        
        # +1 sigma value
        t.GetEntry(i_toy * 3 + 2)
        r_hi = getattr(t, "r")
        
        print(r_fit, r_lo, r_hi)
        diff = r_truth - r_fit

        if diff > 0: 
            N_pos +=1 
        else: N_neg+=1
        # Use uncertainty depending on where mu_truth is relative to mu_fit
        if diff > 0:
            if r_hi > 4.9: continue
            sigma = abs(r_hi - r_fit)

        else:
            if r_lo < -1.9: continue
            sigma = abs(r_lo - r_fit)

        if sigma != 0:
            sigma_values = np.append(sigma_values, sigma)
        else:
            sigma = sigma_values.mean()

        if sigma != 0:
            hist_pull.Fill(diff / sigma)
print(r_truth, N_pos, N_neg)
canv = ROOT.TCanvas()
hist_pull.Draw()

# Fit Gaussian to pull distribution
ROOT.gStyle.SetOptFit(111)
hist_pull.Fit("gaus")

canv.SaveAs(f"SIs/{args.title}_{args.r}.png")
