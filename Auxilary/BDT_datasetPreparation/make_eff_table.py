import ROOT
import os
import re
import numpy as np

for f in os.listdir("datasets"):
    if not f.startswith("BDT") or "Signal" not in f:
        continue
    mx_match = re.search(r"MX-(\d+)", f)
    my_match = re.search(r"MY-(\d+)", f)
    MX = int(mx_match.group(1))
    MY = int(my_match.group(1))
    print("Processing: ", f, MX, MY)
    rdf = ROOT.RDataFrame("Events", "datasets/" + f)

    classifiers = ["PNet_H", "PNet_Y", "BDTG"]
    event_types = {"TP", "FN"}
    Nevents = {}
    for classifier in classifiers:
        Nevents[classifier] = {}
        for event_type in event_types:
            Nevents[classifier][event_type] = []
    
    scores = np.linspace(-1, 1, 21) 

    for score in scores:
        print(score)
        for classifier in classifiers:
            Nevents[classifier]["TP"].append(rdf.Filter(f"{classifier} > {score}").Sum("BDT_weight").GetValue())
            Nevents[classifier]["FN"].append(rdf.Filter(f"{classifier} < {score}").Sum("BDT_weight").GetValue())
    effs = {}
    for i in range(len(classifiers)):
        classifier = classifiers[i]
        effs[classifier] = [x / (x + y) for x, y in  zip(Nevents[classifier]["TP"], Nevents[classifier]["FN"]) ]
    with open(f"eff_tables/MX-{MX}_MY-{MY}_testTree.txt", "w") as sig_f:
        for j in range(len(scores)):
            sig_f.write(f'{scores[j]} {effs["BDTG"][j]} {effs["PNet_H"][j]} {effs["PNet_Y"][j]}\n')
        
 
