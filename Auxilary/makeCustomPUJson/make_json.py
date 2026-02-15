import json
import numpy as np
with open("example.json", "r") as f:
   corr_json = json.load(f)

#print(corr_json["corrections"][0])
corr =corr_json["corrections"][0]
corr["name"] = "manually_produced_2024_pileup_correction"
nom_corr = corr["data"]["content"][0]
up_corr = corr["data"]["content"][1]
down_corr = corr["data"]["content"][2]

data = np.loadtxt(f"puweights_2024.txt")
nom_val = data[:-1,2]
up_val = data[:-1,3]
down_val = data[:-1,4]
nom_corr["value"]["content"] = list(nom_val)
up_corr["value"]["content"] = list(up_val)
down_corr["value"]["content"] = list(down_val)
print(corr_json)
with open("puweights_2024.json", "w") as f:
    json.dump(corr_json, f, indent = 4)
