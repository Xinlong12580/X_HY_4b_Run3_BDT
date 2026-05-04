import os
import matplotlib.pyplot as plt
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--fname', type=str, dest='fname',action='store', required=True)
args = parser.parse_args()
with open(args.fname, "r") as f:
    lines = f.readlines()
systs = []
values = []
errors = []
for line in lines:
    syst = line.split()[0]
    if "In" in syst or "QCD_" in syst or "PASS" in syst or "n_exp" in syst or "r" == syst or "M_" in syst:
        continue 
    value = float(line.split()[1])
    error = float(line.split()[2])
    print(line)
    systs.append(syst)
    values.append(value)
    errors.append(error)
x = range(len(systs))  # numeric positions
fig = plt.figure()
ax = fig.add_subplot(111)
ax.errorbar(x, values, yerr=errors, fmt='o', capsize=5, color = "red")

ax.plot([0,100], [0,0], color = "black")
ax.plot([0,100], [-1,-1], color = "black", linestyle = "--")
ax.plot([0,100], [1,1], color = "black", linestyle = "--")
ax.set_xticks(x)
ax.set_xticklabels(systs, rotation=45, ha='right')
ax.set_xlim(-1, len(systs) + 1)
ax.set_ylim(-2, 2)
ax.set_ylabel("Value")
ax.set_title("Systs")
fig.tight_layout()

fig.savefig("parameters/plots/" + os.path.basename(args.fname).replace(".txt", ".png"))
