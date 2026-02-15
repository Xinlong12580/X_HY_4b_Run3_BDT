import matplotlib.pyplot as plt
import ROOT
import os
import mplhep as hep
import json
from argparse import ArgumentParser
from matplotlib.ticker import MaxNLocator

parser=ArgumentParser()

plt.style.use(hep.style.CMS)
#modes = ["1p1_BDT", "1p1", "2p1_BDT", "2p1"]
modes = ["2p1","2p1_BDT_noDDT", "2p1_BDT"]
#modes = ["2p1", "2p1_BDT_noDDT", "2p1_BDT_v0", "2p1_BDT_v1"]
modes = ["1p1", "1p1_BDT_DDT", "2p1", "2p1_BDT_noDDT", "2p1_BDT_v0"]
modes = ["1p1", "1p1_BDT_continuous", "1p1_BDT"]
modes = ["2p1", "2p1_BDT_noDDT_continuous", "2p1_BDT", "2p1_BDT_v0", "2p1_BDT_noDDT"]
modes = ["2p1", "2p1_BDT", "2p1_BDT_hv0", "2p1_BDT_v1", "2p1_BDT_noDDT"]
#modes = ["1p1", "1p1_BDT", "1p1_BDT_DDT"]
colors = ["cyan", "red", "blue", "green", "magenta", "purple"]
#colors = [ "blue", "green", "red", "purple"]
linestyles = [(0, (7, 2)), (0, (5, 2)), (0, (2, 2)), (0, (1, 2))]
linestyles = [(0, (7, 2)), (0, (5, 2)), (0, (2, 2)), (0, (1, 2))]
linestyles = ["-", "-", "-", "-", "-", "-", "-"]
markersize = 10
linewidth = 2
markers = ["o", "s", "^", "D", "o", "o", "o"]
alpha = 0.7
save_dir = f"plots/plots_limits_All" 
collecting = 1
if collecting == 1:
    All_Limits = {}
    for mode in modes:
        with open(f"outputList/output_limits_{mode}.txt", "r") as f:
            files = [file.strip() for file in f.readlines() if "AsymptoticLimits" in file]
        #print(files)
        Limits = {"YSlice": {}, "XSlice": {}}
        for file in files:
            f = ROOT.TFile.Open(file)
            tree = f.limit
            limit = []
            if tree.GetEntries() < 5:
                continue
            for entry in tree:
                print("Bad File: " + file)
                limit.append(tree.limit)
            if limit[2] > 1000:
                continue
            M_i_ind = file.find("123456_") + 7
            M_f_ind = file.find("_region")
            M_str = file[M_i_ind: M_f_ind]
            MX = int(M_str.partition("_")[0])
            MY = int(M_str.partition("_")[2])
            if MY not in Limits["YSlice"]:
                Limits["YSlice"][MY] = {}
            if MX not in Limits["XSlice"]:
                Limits["XSlice"][MX] = {}
            Limits["YSlice"][MY][MX] = limit
            Limits["XSlice"][MX][MY] = limit
        All_Limits[mode] = Limits
    print(All_Limits)


    with open("limits_database/All_Limits.txt", "w") as f:
            json.dump(All_Limits, f, indent = 4)



with open("limits_database/All_Limits.txt", "rb") as f:
        All_Limits = json.load(f)
with open ("limits_database/Limits_run2_expected.txt", "rb") as f:
        run2_Limits = json.load(f)

for MY in All_Limits[modes[0]]["YSlice"]:
    fig = plt.figure(figsize = (10, 8)) 
    ax = fig.add_subplot(1, 1, 1)
    #for mode in modes:
    for i in range(len(modes)):
        mode = modes[i]
        MXs = []
        Medians = []
        if MY in All_Limits[mode]["YSlice"]:
            for MX in All_Limits[mode]["YSlice"][MY]:
                MXs.append(int(MX))
            MXs.sort()    
            for MX in MXs:
                Medians.append(All_Limits[mode]["YSlice"][MY][str(MX)][2])
            print(MXs)
            print(Medians)

            ax.plot(MXs, Medians, marker = markers[i], color = colors[i], linestyle = linestyles[i], alpha = alpha, label = mode, linewidth = linewidth, markersize = markersize, markerfacecolor='none')
    if MY in run2_Limits["YSlice"]:
        MXs = []
        Obses = []
        for MX in run2_Limits["YSlice"][MY]:
            MXs.append(int(MX))
        MXs.sort()    
        for MX in MXs:
            Obses.append(run2_Limits["YSlice"][MY][str(MX)][2])
        print(f"Run2 MY = {MY}: ", MXs)
        print(Obses)

        ax.plot(MXs, Obses, marker='X', color = "grey", label = "run2 expected", alpha = 0.5, markersize = markersize)

    ax.xaxis.set_major_locator(MaxNLocator(20))
    ax.yaxis.set_major_locator(MaxNLocator(20))
    ax.set_title(f"XHY4b_All_limit_MY: {MY} GeV")
    ax.set_xlabel("MX(GeV)")
    ax.set_ylabel("cross section x branching ratio(fb)")
    ax.set_ylim(0.1, 1000)
    ax.legend(loc = 1)
    ax.tick_params(axis='x', labelsize=12)
    fig.savefig(f"{save_dir}/linear_limits_All_MY_{MY}.png")
    ax.set_yscale("log")
    fig.savefig(f"{save_dir}/log_limits_All_MY_{MY}.png")
    plt.close(fig)


for MX in All_Limits[modes[0]]["XSlice"]:
    fig = plt.figure(figsize = (10, 8)) 
    ax = fig.add_subplot(1, 1, 1)
    #for mode in modes:
    for i in range(len(modes)):
        mode = modes[i]
        MYs = []
        Medians = []
        if MX in All_Limits[mode]["XSlice"]:
            for MY in All_Limits[mode]["XSlice"][MX]:
                MYs.append(int(MY))
            MYs.sort()    
            for MY in MYs:
                Medians.append(All_Limits[mode]["XSlice"][MX][str(MY)][2])
        print(MYs)
        print(Medians)

        ax.plot(MYs, Medians, marker = markers[i], color = colors[i], linestyle = linestyles[i], alpha = alpha, label = mode, linewidth = linewidth,  markersize = markersize, markerfacecolor='none' )
    if MX in run2_Limits["XSlice"]:
        MYs = []
        Obses = []
        for MY in run2_Limits["XSlice"][MX]:
            MYs.append(int(MY))
        MYs.sort()    
        for MY in MYs:
            Obses.append(run2_Limits["XSlice"][MX][str(MY)][2])

        ax.plot(MYs, Obses, marker='X', color = "grey", alpha = 0.5, label = "run2 expected",  markersize = markersize)

    ax.set_title(f"XHY4b_All_limit_MX: {MX} GeV")
    ax.set_xlabel("MY(GeV)")
    ax.set_ylabel("cross section x branching ratio(fb)")
    ax.set_ylim(0.1, 1000)
    ax.legend(loc = 1)
    ax.tick_params(axis='x', labelsize=12)
    fig.savefig(f"{save_dir}/linear_limits_All_MX_{MX}.png")
    ax.set_yscale("log")
    fig.savefig(f"{save_dir}/log_limits_All_MX_{MX}.png")
    plt.close(fig)




