import numpy as np
import matplotlib.pyplot as plt
import mplhep
from hist import Hist
import ROOT
import array
import json
import pickle
import os
import sys
DIR_TOP = os.environ["ANA_TOP"]
sys.path.append(DIR_TOP)
from XHY4b_Helper import *
with open("pkls/nPV_2p1_TH.pkl", "rb") as f:
    hists = pickle.load(f)
with open(DIR_TOP + "raw_nano/color_scheme.json", "r") as f:
    color_json = json.load(f)
with open(DIR_TOP + "raw_nano/Luminosity.json") as f:
    lumi_json = json.load(f)
h_data = hists["data"]
#----------------------------- set bins, variable columns and other configs---------------------------------------------------------------------

save_dir = "plots/plots_nPV"
#-------------------------------------rebinning -----------------------------------------

data_binned = [h_data.GetBinContent(i) for i in range(1, h_data.GetNbinsX() + 1)]
data_binned_error = [h_data.GetBinError(i) for i in range(1, h_data.GetNbinsX() + 1)]
bin_centers = [(h_data.GetXaxis().GetBinUpEdge(i) + h_data.GetXaxis().GetBinLowEdge(i) )/2 for i in range(1, h_data.GetNbinsX() + 1) ]
print(data_binned)
for pu in ["PU", "noPU"]:
    labels = []
    colors = []
    hs = []
    N_data = h_data.Integral()
    N_MC = 0
    processes = ["MC_QCDJets", "MC_TTBarJets"]
    year = "2024"
    for process in hists[pu]:
        colors.append(color_json[process])
        labels.append(process)
        N_MC += hists[pu][process].Integral()
    scale_factor = N_data/N_MC
    for process in hists[pu]:
        hists[pu][process].Scale(scale_factor)
        hs.append(hists[pu][process])
    #fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={"height_ratios": [3, 1]}, sharex=True)
    fig = plt.figure(figsize=(15, 12))
    ax1 = fig.add_subplot(111)
    ax1.errorbar(bin_centers, data_binned, yerr=data_binned_error, fmt='o', color='black', label='Data')
    mplhep.histplot(
        hs,
        label = labels,
        color = colors,
        stack = True,
        histtype = "fill",
        ax = ax1,
    )
    mplhep.histplot(
        hs,
        stack = True,  # Note: keep stack=True so contours align with total stacks
        histtype = "step",
        color = "black",
        ax = ax1,
        linewidth = 1.2,
    )
    mplhep.cms.label("Preliminary", data = False, rlabel = f"{((lumi_json['2024'])/1000):.2f}"  + r"$fb^{-1}$, "+ year + "(13.6 TeV)", ax = ax1)
    ax1.set_ylabel("Event Counts")
    xlabel = f"PV_npvs, with PU correction" if pu == "PU" else f"PV_npvs, without PU correction"
    ax1.set_xlabel(xlabel)
    ax1.legend()

    fig.tight_layout()
    ax1.set_yscale("linear")
    ax1.set_ylim(auto = True)
    fig.savefig(f"{save_dir}/linear_PV_npvs_{pu}.png")
    ax1.set_yscale("log")
    ax1.set_ylim(1,10000000)
    fig.savefig(f"{save_dir}/log_PV_npvs_{pu}.png")


