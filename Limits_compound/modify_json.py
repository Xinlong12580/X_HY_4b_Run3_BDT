import ROOT

import json
from argparse import ArgumentParser

parser=ArgumentParser()

parser.add_argument('--json', type=str, action='store', required=True)
parser.add_argument('--stat', type=str, action='store', required=True)
args = parser.parse_args()

with open(args.json, "r") as f:
    config = json.load(f)

stat = ROOT.TFile.Open(args.stat, "r")
TTBar_syst = config["PROCESSES"]["Allyears__MC_TTBarJets"]["SYSTEMATICS"]
systs = config["SYSTEMATICS"]

for key in stat.GetListOfKeys():
    name = key.GetName()
    if "MCstat" not in name or "up" not in name:
        continue
    syst = name[name.find("MCstat"): name.find("_up")] 
    print("Adding ", syst)
    if syst not in TTBar_syst:
        TTBar_syst.append(syst) 
    systs[syst] = {"UP": "PATH_LOCAL/FILE:HIST_UP","DOWN": "PATH_LOCAL/FILE:HIST_DOWN","SIGMA": 1.0}
print("Final json:", args.json)
print(config)

with open(args.json, "w") as f:
    json.dump(config,f, indent = 4)
