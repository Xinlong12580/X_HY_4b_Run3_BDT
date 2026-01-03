import ROOT
import numpy as np
import matplotlib.pyplot as plt
f_name = "TMVAC.root"

rdf = ROOT.RDataFrame("dataset/TestTree", f_name)
print(rdf.Count().GetValue())

signal_rdf = rdf.Filter("classID == 0")
bkg_rdf = rdf.Filter("classID == 1")

classifiers = ["PNet_H", "PNet_Y", "BDTG"]
event_types = {"TP", "TN", "FP", "FN"}
Nevents = {}
for classifier in classifiers:
    Nevents[classifier] = {}
    for event_type in event_types:
        Nevents[classifier][event_type] = []
    
#scores = np.linspace(-2, 2, 400) 
scores = np.linspace(-2, 2, 41) 

for score in scores:
    print(score)
    for classifier in classifiers:
        Nevents[classifier]["TP"].append(signal_rdf.Filter(f"{classifier} > {score}").Count().GetValue())
        Nevents[classifier]["TN"].append(bkg_rdf.Filter(f"{classifier} < {score}").Count().GetValue())
        Nevents[classifier]["FP"].append(bkg_rdf.Filter(f"{classifier} > {score}").Count().GetValue())
        Nevents[classifier]["FN"].append(signal_rdf.Filter(f"{classifier} < {score}").Count().GetValue())

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
fig.savefig("ROC.png")
