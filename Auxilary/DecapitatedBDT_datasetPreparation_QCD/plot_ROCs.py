import matplotlib.pyplot as plt
import os
import re
import numpy as np
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()
if args.mode == "1p1":
    classifiers = ["BDTG", "minPNet", "PNet_H", "PNet_Y"]
    BKGs = {"score":[], "BDTG":[], "" "PNet_H":[], "PNet_Y":[]}
elif args.mode == "2p1":
    classifiers = ["BDTG", "minPNet", "minPNet_higherY", "PNet_H", "PNet_Y0", "Pnet_Y1"]
    BKGs = {"score":[], "BDTG":[], "PNet_H":[], "PNet_Y":[]}
BKGs = {}
BKGs["scores"] = []
for classifier in classifiers:
    BKGs[classifier] = []

with open(f"eff_tables/BKG_mistagging_{args.mode}.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        effs = line.strip().split(" ")
        BKGs["scores"].append(float(effs[0]))
        for i in range(len(classifiers)):
            BKGs[classifiers[i]].append(float(effs[i+1]))
    
print(BKGs)

for f in os.listdir("eff_tables/"):
    if "BKG" in f or args.mode not in f:
        continue
    mx_match = re.search(r"MX-(\d+)", f)
    my_match = re.search(r"MY-(\d+)", f)

    MX = int(mx_match.group(1))
    MY = int(my_match.group(1))
    sigs = {}
    sigs["scores"] = []
    for classifier in classifiers:
        sigs[classifier] = []
    with open("eff_tables/" + f, "r") as f:
        lines = f.readlines()
        for line in lines:
            effs = line.strip().split(" ")
            sigs["scores"].append(float(effs[0]))
            for i in range(len(classifiers)):
                sigs[classifiers[i]].append(float(effs[i+1]))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for classifier in sigs:
        if classifier == "scores":
            continue
        ax.plot(BKGs[classifier], sigs[classifier], label = classifier)
    ax.plot([0, 1], [0, 1], linestyle='--', color = "black")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Mistagging rate")
    ax.set_ylabel("Tagging efficiency")
    ax.set_title(f"ROC curve, MX = {MX}, MY = {MY}")
    fig.legend(loc = 1)
    fig.savefig(f"plots/ROC_MX-{MX}_MY-{MY}_{args.mode}.png")

    fig = plt.figure(figsize = (10, 6))
    ax = fig.add_subplot(1, 1, 1)
    scores = sigs["scores"]
    for i in range(len(classifiers)):
        classifier = classifiers[i]
        if (MX == 1600 and MY == 500):
            print(sigs[classifier], BKGs[classifier])
        significances = [x / (1 + np.sqrt(y)) for x, y in  zip(sigs[classifier], BKGs[classifier]) ]
        ax.plot(scores, significances, label = classifier)
    ax.set_xlim(-1, 1)
    ax.set_xlabel("Score")
    ax.set_ylabel("S/(1+sqrt(B))")
    ax.set_title(f"Punzi Significance {args.mode}")
    fig.legend(loc = 1)
    fig.savefig(f"plots/Punzi_Significance_MX-{MX}_MY-{MY}_{args.mode}.png")


