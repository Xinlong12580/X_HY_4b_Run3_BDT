import ROOT
import matplotlib.pyplot as plt
import numpy as np
f_name = "Loose_MX-3500_MY-800_workspace/SignalMC_XHY4b_1x1_area/higgsCombiner_10.FitDiagnostics.mH125.123456.root" 
nom_r = 10
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
        print(index, r, deltar)
        rs.append(r)
        deltars.append(deltar)
        sigs.append((r - nom_r) / deltar)
        index += 1

fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1, 1, 1)
counts, bin_edges = np.histogram(sigs, bins=np.linspace(-5, 5, 21))

# Compute bin centers
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# Poisson errors
errors = np.sqrt(counts)

ax.errorbar(bin_centers, counts, yerr=errors, fmt='o', capsize=3)

fig.savefig(f"signal_injection_r_{nom_r}.png")

