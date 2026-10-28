import json

mode = "2p1"
config_file = f"XYH_{mode}_old.json"
with open( config_file, "r") as f:
    config = json.load(f)
years = ["2022", "2022EE", "2023", "2023BPix", "2024"]
systs = ["JES__Absolute", "JES__BBEC1", "JES__EC2",  "JES__FlavorQCD", "JES__HF", "JES__RelativeBal" ]
for year in years:
    systs += [f"Y{year}_JES__Absolute_{year}", f"Y{year}_JES__BBEC1_{year}", f"Y{year}_JES__EC2_{year}", f"Y{year}_JES__HF_{year}", f"Y{year}_JES__RelativeSample_{year}"]
    systs += [f"Y{year}_JMS_", f"Y{year}_JMR_"]
for process in config["PROCESSES"]:
    if "data" in process: continue

    old_jeses = []
    for syst in config["PROCESSES"][process]["SYSTEMATICS"]:
        if "JES" in syst: old_jeses.append(syst)
    print(old_jeses)
    for old_jes in old_jeses:
        config["PROCESSES"][process]["SYSTEMATICS"].remove(old_jes)        

    for syst in systs:
        if syst not in config["PROCESSES"][process]["SYSTEMATICS"]:
            config["PROCESSES"][process]["SYSTEMATICS"].append(syst)




    
for syst in systs:
    if syst in config["SYSTEMATICS"]: continue  
    config["SYSTEMATICS"][syst] = {"UP": "PATH_LOCAL/FILE:HIST_UP","DOWN": "PATH_LOCAL/FILE:HIST_DOWN","SIGMA": 1.0}
for old_jes in old_jeses:
    if old_jes in config["SYSTEMATICS"]: del config["SYSTEMATICS"][old_jes]



for process in config["PROCESSES"]:
    if "data" in process: continue

    old_lumies = []
    for syst in config["PROCESSES"][process]["SYSTEMATICS"]:
        if "lumi" in syst: old_lumies.append(syst)
    for old_lumi in old_lumies:
        config["PROCESSES"][process]["SYSTEMATICS"].remove(old_lumi)
    config["PROCESSES"][process]["SYSTEMATICS"].append("lumi")

config["SYSTEMATICS"]["lumi"] = {"VAL":1.013, "CODE": 0}
for old_lumi in old_lumies:
    if old_lumi in config["SYSTEMATICS"]: del config["SYSTEMATICS"][old_lumi]

with open (f"XYH_{mode}.json", "w") as f:
    json.dump(config, f, indent = 4)
