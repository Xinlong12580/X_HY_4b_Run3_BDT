import ROOT
import numpy as np
import matplotlib.pyplot as plt

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()
f_name = f"TMVAC_{args.mode}.root"

rdf = ROOT.RDataFrame("dataset/TestTree", f_name)
print(rdf.Count().GetValue())

#signal_rdf = rdf.Filter("classID == 0")
#bkg_rdf = rdf.Filter("classID == 1")
signal_rdf = ROOT.RDataFrame("Events", "datasets/BDT_reweighted_Signal_nom_tagged_selected_SKIM_skimmed_2022EE__SignalMC_XHY4b__MX-1600_MY-200_1p1_ALL.root")
bkg_rdf = ROOT.RDataFrame("Events", "datasets/BDT_BKGs_1p1_ALL.root")


classifiers = ["PNet_H", "PNet_Y", "BDTG"]
classifiers = ["minPNet", "PNet_H", "PNet_Y", "BDTG"]
event_types = {"TP", "TN", "FP", "FN"}
Nevents = {}
for classifier in classifiers:
    Nevents[classifier] = {}
    for event_type in event_types:
        Nevents[classifier][event_type] = []
    
#scores = np.linspace(-2, 2, 400) 
scores = np.linspace(-1, 1, 101) 
scores = np.linspace(-1, 1, 21) 
scores = np.linspace(-1, 1, 11) 
scores = np.linspace(0.6, 1, 11) 
#scores = np.linspace(-1, 1, 2) 

for score in scores:
    print(score)
    for classifier in classifiers:
        #Nevents[classifier]["TP"].append(signal_rdf.Filter(f"{classifier} > {score}").Count().GetValue())
        #Nevents[classifier]["TN"].append(bkg_rdf.Filter(f"{classifier} < {score}").Count().GetValue())
        #Nevents[classifier]["FP"].append(bkg_rdf.Filter(f"{classifier} > {score}").Count().GetValue())
        #Nevents[classifier]["FN"].append(signal_rdf.Filter(f"{classifier} < {score}").Count().GetValue())
        Nevents[classifier]["TP"].append(signal_rdf.Filter(f"{classifier} > {score}").Sum("BDT_weight").GetValue())
        Nevents[classifier]["TN"].append(bkg_rdf.Filter(f"{classifier} < {score}").Sum("BDT_weight").GetValue())
        Nevents[classifier]["FP"].append(bkg_rdf.Filter(f"{classifier} > {score}").Sum("BDT_weight").GetValue())
        Nevents[classifier]["FN"].append(signal_rdf.Filter(f"{classifier} < {score}").Sum("BDT_weight").GetValue())
'''
fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1, 1, 1)
for classifier in classifiers:
    FPRs = [x / (x + y) for x, y in  zip(Nevents[classifier]["FP"], Nevents[classifier]["TN"]) ]
    TPRs = [x / (x + y) for x, y in  zip(Nevents[classifier]["TP"], Nevents[classifier]["FN"]) ]
    ax.plot(FPRs, TPRs, label = classifier)
ax.plot([0, 1], [0, 1], linestyle='--', color = "black")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title("ROC curve")
fig.legend(loc = 1)
fig.savefig("ROC_TP_TN.png")
'''


fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1, 1, 1)
for i in range(len(classifiers)):
    classifier = classifiers[i]
    effs = [x / (x + y) for x, y in  zip(Nevents[classifier]["TP"], Nevents[classifier]["FN"]) ]
    mistagging_rates = [x / (x + y) for x, y in  zip(Nevents[classifier]["FP"], Nevents[classifier]["TN"]) ]
    ax.plot(mistagging_rates, effs, label = classifier)
ax.plot([0, 1], [0, 1], linestyle='--', color = "black")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel("Mistagging rate")
ax.set_ylabel("Tagging efficiency")
ax.set_title(f"ROC curve {args.mode}")
fig.legend(loc = 1)
fig.savefig(f"ROC_{args.mode}.png")

fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1, 1, 1)
for i in range(len(classifiers)):
    classifier = classifiers[i]
    significances = [x / (1 + np.sqrt(y)) for x, y in  zip(Nevents[classifier]["TP"], Nevents[classifier]["FP"]) ]
    ax.plot(scores, significances, label = classifier)
ax.set_xlim(0, 1)
ax.set_xlabel("Score")
ax.set_ylabel("S/(1+sqrt(B))")
ax.set_title(f"Punzi Significance {args.mode}")
fig.legend(loc = 1)
fig.savefig(f"Punzi_Significance_{args.mode}.png")




effs = {}
mistagging_rates = {}
for i in range(len(classifiers)):
    classifier = classifiers[i]
    effs[classifier] = [x / (x + y) for x, y in  zip(Nevents[classifier]["TP"], Nevents[classifier]["FN"]) ]
    mistagging_rates[classifier] = [x / (x + y) for x, y in  zip(Nevents[classifier]["FP"], Nevents[classifier]["TN"]) ]
with open(f"eff_tables/BKG_mistagging_{args.mode}.txt", "w") as bkg_f:
    with open(f"eff_tables/MX-1600_MY-200_testTree_{args.mode}.txt", "w") as sig_f:
        for j in range(len(scores)):
            bkg_f.write(f'{scores[j]} {mistagging_rates["BDTG"][j]} {mistagging_rates["PNet_H"][j]} {mistagging_rates["PNet_Y"][j]}\n')
            sig_f.write(f'{scores[j]} {effs["BDTG"][j]} {effs["PNet_H"][j]} {effs["PNet_Y"][j]}\n')
        
