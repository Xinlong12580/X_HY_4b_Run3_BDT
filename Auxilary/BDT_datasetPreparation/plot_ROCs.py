import matplotlib.pyplot as plt
import os
import re
BKGs = {"score":[], "BDTG":[], "PNet_H":[], "PNet_Y":[]}
with open("eff_tables/BKG_mistagging.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        effs = line.strip().split(" ")
        BKGs["score"].append(float(effs[0]))
        BKGs["BDTG"].append(float(effs[1]))
        BKGs["PNet_H"].append(float(effs[2]))
        BKGs["PNet_Y"].append(float(effs[3]))
    
print(BKGs)

for f in os.listdir("eff_tables/"):
    if "BKG" in f:
        continue
    mx_match = re.search(r"MX-(\d+)", f)
    my_match = re.search(r"MY-(\d+)", f)

    MX = int(mx_match.group(1))
    MY = int(my_match.group(1))
    sigs = {"score":[], "BDTG":[], "PNet_H":[], "PNet_Y":[]}
    with open("eff_tables/" + f, "r") as f:
        lines = f.readlines()
        for line in lines:
            effs = line.strip().split(" ")
            sigs["score"].append(float(effs[0]))
            sigs["BDTG"].append(float(effs[1]))
            sigs["PNet_H"].append(float(effs[2]))
            sigs["PNet_Y"].append(float(effs[3]))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for classifier in sigs:
        if classifier == "score":
            continue
        ax.plot(BKGs[classifier], sigs[classifier], label = classifier)
    ax.plot([0, 1], [0, 1], linestyle='--', color = "black")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Mistagging rate")
    ax.set_ylabel("Tagging efficiency")
    ax.set_title(f"ROC curve, MX = {MX}, MY = {MY}")
    fig.legend(loc = 1)
    fig.savefig(f"plots/MX-{MX}_MY-{MY}.png")
