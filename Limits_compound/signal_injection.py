import ROOT
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
parser.add_argument('-r', type=float, dest='r',action='store', required=True)
parser.add_argument('--title', type=str, dest='title',action='store', required=True)
args = parser.parse_args()
f_name = args.f 
#f_name = "Loose_MX-3500_MY-800_workspace/SignalMC_XHY4b_1x1_area/higgsCombiner_10.FitDiagnostics.mH125.123456.root" 
nom_r = args.r
f = ROOT.TFile.Open(f_name, "READ")
limit = f.limit
index = 2
rs = []
deltars = []
sigs = []
for entry in limit:
    if entry.iToy != index:
        r = entry.limit
        deltar = entry.limitErr
    else:
        if deltar > 0:
            print(index, r, deltar)
            rs.append(r)
            deltars.append(deltar)
            sigs.append((r - nom_r) / deltar)
            index += 1

fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1, 1, 1)
counts, bin_edges = np.histogram(sigs, bins=np.linspace(-2, 2, 21))

# Compute bin centers
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# Poisson errors
errors = np.sqrt(counts)

ax.errorbar(bin_centers, counts, yerr=errors, fmt='o', capsize=3)
ax.set_title(f"signal injection, $r_0$={nom_r}, {args.title}")
ax.set_xlabel(r"$(r-r_0)/(\delta r)$")
fig.savefig(f"SIs/signal_injection_r_{nom_r}_{args.title}.png")

