import ROOT
import os
import numpy as np
import array
import json
from XHY4b_Helper import * 
from argparse import ArgumentParser
import os

parser=ArgumentParser()

parser.add_argument('--mode', type=str, action='store', required=False)
parser.add_argument('--type', type=str, action='store', required=False)

parser.add_argument('--mx', type=str, action='store', required=False)
parser.add_argument('--my', type=str, action='store', required=False)
parser.add_argument('--Reg', type=str, action='store', required=False)
args = parser.parse_args()
if "1p1" in args.mode:
    hist_mode = "1p1"
elif "2p1" in args.mode:
    hist_mode = "2p1"
with open("raw_nano/Luminosity.json") as f:
    lumi_json = json.load(f)

with open("raw_nano/Xsections_background.json") as f:
    Xsec_json = json.load(f)

with open("raw_nano/Datasets_signal.json") as f:
    signal_json=json.load(f)
#----------------------------- set bins, variable columns and other configs---------------------------------------------------------------------
with open(f"outputList/output_division_{args.mode}_BDT.txt") as f:
    lines = f.readlines()
    if args.Reg == "Control":
        template_files =[ line.strip() for line in lines if "Templates" in line and "log" not in line and args.mode in line and "RegCon" in line]
    elif args.Reg == "Signal":
        template_files =[ line.strip() for line in lines if "Templates" in line and "log" not in line and args.mode in line and "RegSig" in line]
systs = ["JES__up", "JES__down", "JER__up", "JER__down", "PileUp_Corr_up", "PileUp_Corr_down", "TriggerSF_up", "TriggerSF_down", "Pdfweight_up", "Pdfweight_down", "nominal"]
if args.type == "signal":
    processes = {"SignalMC_XHY4b": [f"MX-{args.mx}_MY-{args.my}"]}

elif args.type == "bkg":
    processes = { "MC_TTBarJets": ["*"], "MC_WZJets": ["Wto2Q-3Jets_HT-200to400", "Wto2Q-3Jets_HT-400to600", "Wto2Q-3Jets_HT-600to800", "Wto2Q-3Jets_HT-800", "Zto2Q-4Jets_HT-200to400", "Zto2Q-4Jets_HT-400to600", "Zto2Q-4Jets_HT-600to800", "Zto2Q-4Jets_HT-800"]}
elif args.type == "all":
    processes = { "MC_TTBarJets": ["*"], "MC_WZJets": ["Wto2Q-3Jets_HT-200to400", "Wto2Q-3Jets_HT-400to600", "Wto2Q-3Jets_HT-600to800", "Wto2Q-3Jets_HT-800", "Zto2Q-4Jets_HT-200to400", "Zto2Q-4Jets_HT-400to600", "Zto2Q-4Jets_HT-600to800", "Zto2Q-4Jets_HT-800"], "SignalMC_XHY4b": [f"MX-{args.mx}_MY-{args.my}"]}
for process in processes:
    if processes[process] == ["*"]:
        processes[process] = []
        if "SignalMC" in process:
            for mass in signal_json["2022"]["SignalMC_XHY4b"]:
                processes[process].append(mass)
        elif "MC" in process:
            for subprocess in Xsec_json[process]:
                processes[process].append(subprocess) 
print(processes)
#exit()
#print(VB1_files) 
#processes = ["JetMET", "MC_TTBarJets", "MC_WZJets", "SignalMC_XHY4b" ]

regions = ["SR1", "SR2", "SB1", "SB2", "VS1", "VS2", "VS3", "VS4", "VB1", "VB2"]
years = ["2022", "2022EE", "2023", "2023BPix"]
MJY_bins = array.array("d", np.linspace(0, 5000, 501) )
MJJ_bins = array.array("d", np.linspace(0, 5000, 501) )
hist_base = ROOT.TH2D(f"MJJvsMJY", f"MJJ vs MJY", len(MJY_bins) - 1, MJY_bins, len(MJJ_bins) - 1, MJJ_bins)
hists = {}
for year in years:
    hists[year] = {}
    if args.type == "bkg" or args.type == "all":
        hists[year]["JetMET"] = {}
        for region in regions:
            hists[year]["JetMET"][region] = {}
            for syst in systs:
                if syst == "nominal" or "Pdfweight" in syst:
                    hists[year]["JetMET"][region][syst] = hist_base.Clone(f"{year}__JetMET__{region}_{hist_mode}__{syst}")
                else:
                    hists[year]["JetMET"][region][syst] = hist_base.Clone(f"{year}__JetMET__{region}_{hist_mode}__Y{year}_{syst}")
    if "SignalMC_XHY4b" in processes:
        for subprocess in processes["SignalMC_XHY4b"]:
            hists[year][f"SignalMC_XHY4b_{subprocess}"] = {}        
            for region in regions:
                hists[year][f"SignalMC_XHY4b_{subprocess}"][region] = {}
                for syst in systs:
                    if syst == "nominal" or "Pdfweight" in syst:
                        hists[year][f"SignalMC_XHY4b_{subprocess}"][region][syst] = hist_base.Clone(f"{year}__SignalMC_XHY4b_{subprocess}__{region}_{hist_mode}__{syst}")
                    else:
                        hists[year][f"SignalMC_XHY4b_{subprocess}"][region][syst] = hist_base.Clone(f"{year}__SignalMC_XHY4b_{subprocess}__{region}_{hist_mode}__Y{year}_{syst}")
        
    for process in processes:
        if "SignalMC" in process:
            continue
        hists[year][process] = {}        
        for region in regions:
            hists[year][process][region] = {}
            for syst in systs:
                if syst == "nominal" or "Pdfweight" in syst:
                    hists[year][process][region][syst] = hist_base.Clone(f"{year}__{process}__{region}_{hist_mode}__{syst}")
                else:
                    hists[year][process][region][syst] = hist_base.Clone(f"{year}__{process}__{region}_{hist_mode}__Y{year}_{syst}")
#print(hists)
#print(VB1_files)
if args.type == "bkg" or args.type == "all":
    processes["JetMET"] = {}
for f_name in template_files:
    for year in years:
        if (year + "__") in f_name:
            for process in processes:
                if process in f_name:
                    good = 0
                    if "MC" in process:
                        for subprocess in processes[process]:
                            if subprocess in f_name:
                                good = 1
                                break
                    else:
                        good = 1
                    if good == 0:
                        continue
                    print(f_name)
                    f = ROOT.TFile.Open(f_name, "READ")
                    for key in f.GetListOfKeys():
                        hist = key.ReadObj()
                        if isinstance(hist, ROOT.TH2):  
                            hist_name = hist.GetName()
                            print(hist_name) 
                            loaded = 0
                            for region in regions:
                                if region in hist_name:
                                    for syst in systs:
                                        if hist_name.endswith(syst):
                                            print(f"{year}_{process}_{region}_{syst}")
                                            if "MC" in process:
                                                for subprocess in processes[process]:
                                                    
                                                    if subprocess  + "_" in f_name:
                                                        if "SignalMC" in process:
                                                            hist.Scale(1/1000)
                                                            hists[year][f"{process}_{subprocess}"][region][syst].Add(hist)
                                                        else:
                                                            hists[year][process][region][syst].Add(hist)
                                                        loaded = 1
                                                        break
                                                    
                                            else:
                                                hists[year][process][region][syst].Add(hist)
                                                loaded = 1
                                    print(f"HIST LOADING STATUS:  {loaded}")
                        del hist
                    f.Close()
                    del f

hists_allyears = {}
for process in hists[years[0]]:
    hists_allyears[process] = {}        
    for region in regions:
        hists_allyears[process][region] = {}
        for syst in systs:
            if syst == "nominal" or "Pdfweight" in syst:
                hists_allyears[process][region][syst] = hist_base.Clone(f"Allyears__{process}__{region}_{hist_mode}__{syst}")
            else:
                for year in years:
                    syst_byyear = f"Y{year}_{syst}"
                    hists_allyears[process][region][syst_byyear] = hist_base.Clone(f"Allyears__{process}__{region}_{hist_mode}__{syst_byyear}")
            #hists_allyears[process][region][syst] = hist_base.Clone(f"Allyears_{process}_{region}_{syst}")
        for syst_byyear in hists_allyears[process][region]:
            year_syst = syst_byyear.partition("_")[0][1:]
            root_syst = syst_byyear[(len(year_syst) + 2):]
            print(syst_byyear, year_syst, root_syst)
            for year in years:
                if syst_byyear == "nominal" or "Pdfweight" in syst_byyear:
                    hists_allyears[process][region][syst_byyear].Add(hists[year][process][region][syst_byyear])
                else:
                    if year == year_syst:
                        hists_allyears[process][region][syst_byyear].Add(hists[year][process][region][root_syst])
                    else:
                        hists_allyears[process][region][syst_byyear].Add(hists[year][process][region]["nominal"])



if args.type == "bkg":
    f = ROOT.TFile.Open(f"Templates/Templates_{args.mode}_{args.Reg}_bkg.root", "RECREATE")
elif args.type == "signal":
    f = ROOT.TFile.Open(f"Templates/Templates_{args.mode}_{args.Reg}_SignalMC_XHY4b_MX-{args.mx}_MY-{args.my}.root", "RECREATE")
if args.type == "all":
    f = ROOT.TFile.Open(f"Templates/Templates_{args.mode}_{args.Reg}_all.root", "RECREATE")
f.cd()

for year in years:
    for process in hists[year]:
        for region in regions:
            for syst in systs:
                hists[year][process][region][syst].Write()

for process in hists_allyears:
    for region in hists_allyears[process]:
        for syst in hists_allyears[process][region]:
            hists_allyears[process][region][syst].Write()

f.Close()


   


    
