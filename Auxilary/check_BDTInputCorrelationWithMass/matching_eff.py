import ROOT
import re
import os
import sys
DIR_TOP = os.environ["ANA_TOP"]
sys.path.append(DIR_TOP)
from XHY4b_Helper import *
mode = "1p1"
# Input txt file containing ROOT paths
input_txt_path = DIR_TOP + f"outputList/output_selection_{mode}_BDT.txt"
#input_txt_path = DIR_TOP + f"outputList/output_mass_debug_{mode}.txt"

# Output efficiency file
output_file = f"{mode}_matching_eff.txt"

# Open output file for writing
with open(output_file, "w") as out:
    # Open and read input file line by line
    with open(input_txt_path, "r") as filelist:
        for line in filelist:
            eos_path = line.strip()
            # Filter to only process ROOT files with required format
            if re.search(rf"nom.*2022EE__.*Signal", eos_path):
                if "Templates" in eos_path:
                    continue
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
                    print(file_path)
                    rdf = ROOT.RDataFrame("Events", file_path)
                    N_total = rdf.Count().GetValue()
                    N_both_matched = rdf.Sum("both_matched").GetValue()
                    eff = N_both_matched /  N_total
                    print(f"{MX} {MY} {eff:.6f}\n")
                    out.write(f"{MX} {MY} {eff:.6f}\n")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

