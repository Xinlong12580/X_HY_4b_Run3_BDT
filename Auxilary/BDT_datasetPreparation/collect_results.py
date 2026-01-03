import glob
import re
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()
files = glob.glob("*.log")

print(files)
massXs = []
massYs = []
best_scores = []
for _file in files:
    if "condor" in _file or "FAILED" in _file or args.mode not in _file:
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
        best_scores.append(lines[-1].strip())
with open (f"best_scores_{args.mode}.txt", "w") as f:
    for i in range(len(massXs)):
        f.write(f"{massXs[i]} {massYs[i]} {best_scores[i]} \n") 
