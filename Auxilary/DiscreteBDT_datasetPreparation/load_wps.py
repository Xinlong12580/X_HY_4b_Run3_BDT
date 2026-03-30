import ROOT
import json
import correctionlib._core as core
WPs = {"AK4":{}, "AK8":{}}
years = ["2022", "2022EE", "2023", "2023BPix", "2024"]

for year in years:
    WPs["AK8"][year] = [0, 0.95, 0.975, 0.99, 1]
    AK4_f = f"/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/{year[0:4]}_Summer{year[2:]}/btagging.json.gz";
    print(AK4_f)
    WPs["AK4"][year] = [0]
    wp_names = ["L", "M", "T", "XT", "XXT"]
    for wp_name in wp_names:
        cset = core.CorrectionSet.from_file(AK4_f)
        key = "particleNet_wp_values"
        if year == "2024":
            key = "UParTAK4_wp_values"
        corr = cset[key]
         
        value = corr.evaluate(wp_name)
        WPs["AK4"][year].append(value) 
        print(value) 
    WPs["AK4"][year].append(1) 

print(WPs)
with open("WPs.json", "w") as f:
    json.dump(WPs, f, indent = 4)
