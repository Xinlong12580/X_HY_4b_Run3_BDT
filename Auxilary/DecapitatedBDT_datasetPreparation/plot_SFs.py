import json
import matplotlib.pyplot as plt
years = ["2022", "2022EE", "2023", "2023BPix", "2024"]
years = ["2022", "2022EE", "2023", "2023BPix"]
WPs = [0.95, 0.975, 0.99]
for year in years:
    with open(f"../../raw_nano/Xbbtagging_SFs/{year}_AK8_Xbbtagging_SF.txt", "r") as f:
        wp_json  = json.load(f)
    SFs = []
    print(wp_json)
    SFs_up = []
    SFs_down = []
    for i in range(3):
        SFs.append(wp_json[f"{i+1}"]["1"]["0_450.0"]["0_2.5"]["nom"])
        SFs_up.append(wp_json[f"{i+1}"]["1"]["0_450.0"]["0_2.5"]["up_uncert"])
        SFs_down.append(wp_json[f"{i+1}"]["1"]["0_450.0"]["0_2.5"]["down_uncert"])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.errorbar(WPs, SFs, yerr=[SFs_down, SFs_up], fmt='o', capsize=5) 
    ax.set_title(f"XbbSFs_{year}")
    ax.set_xlabel("Xbb score")
    ax.set_xlabel("SF")
    ax.set_xlim(0.1, 1)
    ax.set_ylim(0.4, 1.6)
    ax.plot([0, 1], [1, 1])
    fig.savefig(f"linear_XbbSF_{year}.png")
    ax.set_xscale("log")
    fig.savefig(f"log_XbbSF_{year}.png")
    print(SFs)
