import ROOT
import numpy as np
plot_dir = "./"
ROOT.gROOT.SetBatch(True)
import ROOT
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser
import os
files = []
for f in os.listdir("SBparameters/"):
    if "full" in f: files.append("SBparameters/" + f)
print(files)
r_truth = 0

truth_function = "exp"
fit_function = "poly"

name = "truth_%s_fit_%s" % (truth_function, fit_function)
hist_pull = ROOT.TH1F("pull_%s" % name, "Pull distribution: truth=%s, fit=%s" % (truth_function, fit_function), 100, -10, 10)
hist_pull.GetXaxis().SetTitle("Pull = (r_{truth}-r_{fit})/#sigma_{fit}")
hist_pull.GetYaxis().SetTitle("Entries")


N_neg  =0
N_pos = 0
for SI in files:
        found = 0
        with open(SI, "r") as f:
            for line in f.readlines():
                if line.startswith("r "):
                    r_line = line.split()
                    r_fit = float(r_line[1])
                    sigma = float(r_line[2])
                    found = 1
                    break
        if found == 0: continue
        print(r_fit, sigma)
        diff = r_truth - r_fit

        if sigma != 0:
            hist_pull.Fill(diff / sigma)
print(r_truth, N_pos, N_neg)
canv = ROOT.TCanvas()
hist_pull.Draw()

# Fit Gaussian to pull distribution
ROOT.gStyle.SetOptFit(111)
hist_pull.Fit("gaus")

canv.SaveAs(f"SIs/test_local.png")
