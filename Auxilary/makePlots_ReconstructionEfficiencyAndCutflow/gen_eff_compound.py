import ROOT
import re
import os
import sys
DIR_TOP = os.environ["ANA_TOP"]
sys.path.append(DIR_TOP)
from XHY4b_Helper import *

# Input txt file containing ROOT paths
input_txt_path = DIR_TOP + "/outputList/output_selection_compound.txt"

# Output efficiency file
output_file = "eff_compound.txt"

# Open output file for writing
with open(output_file, "w") as out:
    # Open and read input file line by line
    with open(input_txt_path, "r") as filelist:
        for line in filelist:
            eos_path = line.strip()
            #print("Found file: " + eos_path)
            # Filter to only process ROOT files with required format
            if re.search(r"nom.*2022EE__.*Signal", eos_path):
                print("Reading file: " + eos_path)
                # Extract MX and MY from filename
                mx_match = re.search(r"MX-(\d+)", eos_path)
                my_match = re.search(r"MY-(\d+)", eos_path)
                if not (mx_match and my_match):
                    print(f"Could not extract MX or MY from: {eos_path}")
                    continue

                MX = int(mx_match.group(1))
                MY = int(my_match.group(1))

                # Correct file path handling
                if eos_path.startswith("root://"):
                    file_path = eos_path
                else:
                    file_path = "root://cmsxrootd.fnal.gov" + eos_path

                try:
                    # Open ROOT file
                    f = ROOT.TFile.Open(file_path)
                    if not f or f.IsZombie():
                        print(f"Failed to open file: {file_path}")
                        continue

                    # Get Cutflow tree
                    cutflow = f.Get("Cutflow")
                    if not cutflow:
                        print(f"Cutflow tree not found in: {file_path}")
                        continue

                    # Load first entry
                    cutflow.GetEntry(0)

                    # Extract variables
                    region_1 = getattr(cutflow, "Region_SR_1p1", None)
                    region_2 = getattr(cutflow, "Region_SR_2p1", None)
                    region_1not2 = getattr(cutflow, "Region_SR_1p1_and_not_Region_SR_2p1", None)
                    region_2not1 = getattr(cutflow, "Region_SR_2p1_and_not_Region_SR_1p1", None)
                    region_1and2 = getattr(cutflow, "Region_SR_1p1_and_Region_SR_2p1", None)
                    before_skim = getattr(cutflow, "BeforeSkim", None)

                    # Check values exist and compute efficiency
                    if before_skim and before_skim != 0:
                        eff_1 = region_1 / before_skim
                        eff_2 = region_2 / before_skim
                        eff_1not2 = region_1not2 / before_skim
                        eff_2not1 = region_2not1 / before_skim
                        eff_1and2 = region_1and2 / before_skim
                        print(f"MX = {MX}, MY = {MY}, Efficiency = {eff_1:.6f} {eff_2:.6f} {eff_1not2:.6f} {eff_2not1:.6f} {eff_1and2:.6f}")
                        out.write(f"{MX} {MY} {eff_1:.6f} {eff_2:.6f} {eff_1not2:.6f} {eff_2not1:.6f} {eff_1and2:.6f}\n")
                    else:
                        print(f"Invalid values in: {file_path}")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

