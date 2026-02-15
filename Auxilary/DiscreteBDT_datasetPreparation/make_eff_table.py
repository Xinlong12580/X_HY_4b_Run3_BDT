import ROOT
import os
import re
import numpy as np
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()

for f in os.listdir("datasets"):
    if not f.startswith("BDT") or "Signal" not in f or args.mode not in f:
        continue
    mx_match = re.search(r"MX-(\d+)", f)
    my_match = re.search(r"MY-(\d+)", f)
    MX = int(mx_match.group(1))
    MY = int(my_match.group(1))
    #if MY != 600 or MX != 1600:
    if MY < 2900:
        continue
    print("Processing: ", f, MX, MY)
    rdf = ROOT.RDataFrame("Events", "datasets/" + f)
    if args.mode == "1p1":
        classifiers = ["PNet_H", "PNet_Y", "minPNet", "BDTG"]
    elif args.mode == "2p1":
        classifiers = ["PNet_H", "PNet_Y0", "PNet_Y1", "minPNet", "minPNet_higherY", "BDTG"]
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
            #Nevents[classifier]["FN"].append(rdf.Filter(f"{classifier} < {score}").Sum("BDT_weight").GetValue())
    effs = {}
    for i in range(len(classifiers)):
        classifier = classifiers[i]
        #effs[classifier] = [x / (x + y) for x, y in  zip(Nevents[classifier]["TP"], Nevents[classifier]["FN"]) ]
        effs[classifier] = Nevents[classifier]["TP"]
    with open(f"eff_tables/MX-{MX}_MY-{MY}_{args.mode}.txt", "w") as sig_f:
        for j in range(len(scores)):
            if args.mode == "1p1":
                sig_f.write(f'{scores[j]} {effs["BDTG"][j]} {effs["minPNet"][j]} {effs["PNet_H"][j]} {effs["PNet_Y"][j]}\n')
            elif args.mode == "2p1":
                sig_f.write(f'{scores[j]} {effs["BDTG"][j]} {effs["minPNet"][j]} {effs["minPNet_higherY"][j]} {effs["PNet_H"][j]} {effs["PNet_Y0"][j]} {effs["PNet_Y1"][j]}\n')
 
