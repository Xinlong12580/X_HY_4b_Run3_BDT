import glob
import re
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
parser.add_argument('--mx', type=str, dest='mx',action='store', required=True)
parser.add_argument('--my', type=str, dest='my',action='store', required=True)
parser.add_argument('--method', type=int, dest="method",action='store', required=True)
args = parser.parse_args()
files = glob.glob("*.log")

print(files)
massXs = []
massYs = []
best_scores = []
best_sig2bkgs = []
best_sigEffs = []
best_bkgEffs = []
best_QCDEffs = []
best_QCDPtoFs = []
best_TTBarEffs = []
for _file in files:
    if f"MX{args.mx}_MY{args.my}" not in _file or "condor" in _file or "FAILED" in _file or args.mode not in _file or (args.year + "__") not in _file or "discrete" not in _file:
        continue
    print(_file)
    mx_match = re.search(r"MX-(\d+)", _file)
    my_match = re.search(r"MY-(\d+)", _file)

    MX = int(mx_match.group(1))
    MY = int(my_match.group(1))
    massXs.append(MX)
    massYs.append(MY)
    with open(_file, "r") as f:
        lines = f.readlines()
        for i in range(1, 20):
            if "best_score" in lines[-i]:
                best_scores.append(lines[-i].strip().partition(" ")[-1])
            if "best_sig2bkg" in lines[-i]:
                best_sig2bkgs.append(lines[-i].strip().partition(" ")[-1])
            if "best_sigEff" in lines[-i]:
                best_sigEffs.append(lines[-i].strip().partition(" ")[-1])
            if "best_bkgEff" in lines[-i]:
                best_bkgEffs.append(lines[-i].strip().partition(" ")[-1])
            if "best_QCDEff" in lines[-i]:
                best_QCDEffs.append(lines[-i].strip().partition(" ")[-1])
            if "best_QCDPtoF" in lines[-i]:
                best_QCDPtoFs.append(lines[-i].strip().partition(" ")[-1])
            if "best_TTBarEff" in lines[-i]:
                best_TTBarEffs.append(lines[-i].strip().partition(" ")[-1])

with open (f"best_scores_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}_{args.method}.txt", "w") as f:
    f.write("{massXs[i]} {massYs[i]} {best_scores[i]} {best_sig2bkgs[i]} {best_sigEffs[i]} {best_bkgEffs[i]} {best_QCDEffs[i]} {best_QCDPtoFs[i]} {best_TTBar_Effs[i]}\n") 
    for i in range(len(massXs)):
        #print(f"{massXs[i]} {massYs[i]} {best_scores[i]} {best_sig2bkgs[i]} {best_sigEffs[i]} {best_bkgEffs[i]} {best_QCDEffs[i]} {best_QCDPtoFs[i]} {best_TTBarEffs[i]}\n")
        f.write(f"{massXs[i]} {massYs[i]} {best_scores[i]} {best_sig2bkgs[i]} {best_sigEffs[i]} {best_bkgEffs[i]} {best_QCDEffs[i]} {best_QCDPtoFs[i]} {best_TTBarEffs[i]}\n") 

with open (f"BDT_threshold_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}.txt", "w") as f:
    for i in range(len(massXs)):
        f.write(f"{massXs[i]} {massYs[i]} {best_scores[i]}\n") 
