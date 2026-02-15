import os
from TwoDAlphabet.ftest import FstatCalc
from scipy.stats import f as f_dist
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser
######################loading info #########################################################
def getNBins(f_name):
    f = ROOT.TFile.Open(f_name, "READ")
    w = f.Get("w")
    data = w.data("data_obs_SB1_Region0")
    return data.numEntries()


parser=ArgumentParser()

parser.add_argument('--tf1', type=str, action='store', required=False)
parser.add_argument('--tf2', type=str, action='store', required=False)
args = parser.parse_args()
tfs = [args.tf1, args.tf2]
#tfs = ["1x1", "2x1"]

print("CHECK")
work_dir = "./Control_MX-3000_MY-600_workspace/"
subdirs = []
dirs = os.listdir(work_dir)
for tf in tfs:
    for subdir in dirs:
        if "Signal" in subdir and tf in subdir:
            subdirs.append(work_dir + subdir + "/")
            break

fs = []
ps = []
ns = []
for subdir in subdirs:
    files = os.listdir(subdir)
    for f in files:
        if "GoodnessOfFit" in f and ".root" in f:
            fs.append(subdir + f)
        elif f == "card.txt":
            p = 0
            n = 0
            with open(subdir + f, "r") as _f:
                for _ in _f.readlines():
                    if "QCD" in _ and "bin" in _:
                        n += 1
                    elif "QCD" in _ and "Rc" in _:
                        p += 1
            ps.append(p)
            #ns.append(n)
            ns.append(getNBins(subdir + f))
print(fs, ps, ns)
if ns[0] == ns[1]:
    n = ns[0]
######################### calculating F and plotting ###################################
F_obs =  FstatCalc(fs[0], fs[1], ps[0], ps[1], n)
F_obs = F_obs[0]
p_value = f_dist.sf(F_obs, ps[1] - ps[0], n - ps[1])
print(F_obs, p_value)
F_dist = f_dist(ps[1] - ps[0], n - ps[1] )

xs = np.linspace(0, 10, 1000)
ys = [F_dist.pdf(x) for x in xs]

fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(xs, ys, color = "red")
ax.set_title(f"{tfs[0]} tested against {tfs[1]}")
ax.set_xlabel(r'$ F = \frac{-2log(\lambda_1 / \lambda_2)/(p_2 - p_1)}{-2log(\lambda_2)/(n - p_2)} $')
ax.text(9, 0.9, f"n = {n}")
ax.text(9, 0.8, f"p1 = {ps[0]}, p2 = {ps[1]}")
ax.text(9, 0.7, f"F_obs = {F_obs:.4f}")
ax.text(9, 0.6, f"p value = {p_value:.4f}")
ax.annotate(
    '',                                # no text
    xy=(F_obs, 0.0),                     # arrow end
    xytext=(F_obs, 0.5),                 # arrow start
    arrowprops=dict(
        arrowstyle='->', 
        color='blue',
        linewidth=2
    )
)
fig.savefig(f"F_test_{tfs[0]}_{tfs[1]}.png")
#plt.savefig(f"F_test.png")






