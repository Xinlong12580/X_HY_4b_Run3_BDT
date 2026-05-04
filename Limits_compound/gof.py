import ROOT
import matplotlib.pyplot as plt
import numpy as np

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--fitdir', type=str, dest='fitdir',action='store', required=True)
parser.add_argument('--title', type=str, dest='title',action='store', required=True)
args = parser.parse_args()

years = ["2022", "2022EE", "2023", "2023BPix", "2024"]

toy_file = args.fitdir + "/higgsCombineSnapshot.GoodnessOfFit.mH125.123456.root" 
obs_file = args.fitdir + "/higgsCombineSnapshot.GoodnessOfFit.mH125.root" 

rdf = ROOT.RDataFrame("limit", toy_file)

np_rdf = rdf.AsNumpy()
print(np_rdf["limit"])
toys = np_rdf["limit"]
fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1,1,1)
counts, bin_edges = np.histogram(toys, bins=np.linspace(150, max(toys), 33))

# Compute bin centers
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# Poisson errors
errors = np.sqrt(counts)

ax.errorbar(bin_centers, counts, yerr=errors, fmt='o', capsize=3)

f = ROOT.TFile.Open(obs_file, "READ")
tree = f.limit
for entry in tree:
    obs_limit = entry.limit
    break
print(obs_limit)
ax.annotate(
    '',                                # no text
    xy=(obs_limit, 0.0),                     # arrow end
    xytext=(obs_limit, max(counts) / 2),                 # arrow start
    arrowprops=dict(
        arrowstyle='->', 
        color='blue',
        linewidth=2
    )
)
p = sum([point > obs_limit for point in toys])/ len(toys)
print(p)
ax.text(30, max(counts) * 0.9, f"p = {p:.4f}")
#plt.savefig(f"F_test.png")
ax.set_title(f"Goodness Of Fit test, {args.title}")
fig.savefig(f"GOFs/{args.title}.png")

