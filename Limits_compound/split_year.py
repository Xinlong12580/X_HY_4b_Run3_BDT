import json
import copy

input_file = "XYH_2p1_Allyears.json"
output_file = "XYH_2p1_Splityears.json"

with open(input_file, "r") as f:
    input_json = json.load(f)

output_json = copy.deepcopy(input_json)
processes = {}
for process in output_json["PROCESSES"]:
    if "Allyears" in process: processes[process]= copy.deepcopy(output_json["PROCESSES"][process]) 

years=["2022", "2022EE", "2023", "2023BPix", "2024"]

for process in processes:
    for year in years:
        new_process = process.replace("Allyears", year)
        systs  = []
        for syst in processes[process]["SYSTEMATICS"]:
            if (not syst.startswith("Y20") ) or (year + "_") in syst:
                systs.append(syst)
            
        output_json["PROCESSES"][new_process] = copy.deepcopy(output_json["PROCESSES"][process])
        output_json["PROCESSES"][new_process]["SYSTEMATICS"] = systs.copy()

for process in processes:
    del output_json["PROCESSES"][process]

for region in output_json["REGIONS"]:
    process_list = output_json["REGIONS"][region]["PROCESSES"].copy()
    new_process_list = []
    for process in process_list:
        if "Allyears" in process:
            for year in years:
                new_process_list.append(process.replace("Allyears", year))
        else:
            new_process_list.append(process)
    output_json["REGIONS"][region]["PROCESSES"] = new_process_list.copy()
        
        
    

with open(output_file, "w") as f:
    json.dump(output_json, f, indent = 4)
    



