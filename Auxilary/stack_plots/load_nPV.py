import numpy as np
import matplotlib.pyplot as plt
import mplhep
from hist import Hist
import ROOT
import array
import json
import pickle
import os
import sys
DIR_TOP = os.environ["ANA_TOP"]
sys.path.append(DIR_TOP)
from XHY4b_Helper import *
#-----------------------------------loading files for the templates --------------------------------------------
with open(DIR_TOP + "outputList/output_selection_2p1_BDT.txt") as f:
    lines = f.readlines()
    data_files =[ line.strip() for line in lines]
data_files = [data_file for data_file in data_files if ((not ("Templates" in data_file)) and "nom" in data_file and "RegSig" in data_file)]
data_files = [ "datasets/" + _f for _f in os.listdir("datasets") ]
print(data_files)
with open(DIR_TOP + "raw_nano/Luminosity.json") as f:
    lumi_json = json.load(f)

with open(DIR_TOP + "raw_nano/Xsections_background.json") as f:
    Xsec_json = json.load(f)

with open(DIR_TOP + "raw_nano/Datasets_signal_v15.json") as f:
    signal_json=json.load(f)
#----------------------------- set bins, variable columns and other configs---------------------------------------------------------------------
years = [ "2024"]
bins = {}
bin_centers = {}
bins["PV_npvs"] = array.array("d", np.linspace(0, 200, 201) )

MC_weight = "weight_All__nominal"

processes = {"MC_QCDJets": ["*"], "MC_TTBarJets": ["*"]}
for process in processes:
    if "*" in processes[process]:
        processes[process] = []
        for subprocess in Xsec_json[process]:
            processes[process].append(subprocess)
print(processes)
#BKG_fileWeight, BKG_totalWeight = load_weight(data_files, years, processes, signal_json, Xsec_json)
#with open("tmp.pkl", "wb") as f:
#    pickle.dump(BKG_totalWeight, f)
with open("tmp.pkl", "rb") as f:
    BKG_totalWeight = pickle.load(f)
hists_noPU = {}
hists_PU = {}
for process in processes:
    hists_noPU[process] = ROOT.TH1D(f"nPV_{process}_noPU", f"nPV_{process}_noPU", len(bins["PV_npvs"]) - 1, bins["PV_npvs"])
    hists_PU[process] = ROOT.TH1D(f"nPV_{process}_PU", f"nPV_{process}_PU", len(bins["PV_npvs"]) - 1, bins["PV_npvs"])
hist_data = ROOT.TH1D(f"nPV_Data_Data_1", f"nPV_Data_Data_1", len(bins["PV_npvs"]) - 1, bins["PV_npvs"])
for data_file in data_files:
    if "JetMET" in data_file:
        print(data_file)
        rdf = ROOT.RDataFrame("Events", data_file) 
        good_string = data_file.replace("/", "_").replace(".", "_").replace(":", "_")
        hist = rdf.Histo1D((good_string, good_string, len(bins["PV_npvs"]) - 1, bins["PV_npvs"]), "PV_npvs").GetValue() 
        hist_data.Add(hist)
        continue
    _process = ""
    _subprocess = ""
    for process in processes:
        if process in data_file:
            _process = process
            for subprocess in processes[process]:
                if subprocess in data_file:
                    _subprocess = subprocess
                    break
            break
    if _process == "" or _subprocess == "": continue
    print(data_file)
    good_string = data_file.replace("/", "_").replace(".", "_").replace(":", "_")
    rdf = ROOT.RDataFrame("Events", data_file)
    rdf = rdf.Define("withPU_weight", f' weight_All__nominal / {BKG_totalWeight["2024"][_process][_subprocess]} ')
    rdf = rdf.Define("withoutPU_weight", f'genWeight * {lumi_json["2024"]} * {Xsec_json[_process][_subprocess]} / {BKG_totalWeight["2024"][_process][_subprocess]} ')
    hist_noPU = rdf.Histo1D((good_string, good_string, len(bins["PV_npvs"]) - 1, bins["PV_npvs"]), "PV_npvs", "withoutPU_weight").GetValue()
    hist_PU = rdf.Histo1D((good_string, good_string, len(bins["PV_npvs"]) - 1, bins["PV_npvs"]), "PV_npvs", "withPU_weight").GetValue()
    hists_noPU[_process].Add(hist_noPU)
    hists_PU[_process].Add(hist_PU)

hists={"data": hist_data, "noPU": hists_noPU, "PU": hists_PU}
save_name = "pkls/nPV_2p1_TH.pkl"
with open(save_name, "wb") as f:
    pickle.dump(hists, f)

