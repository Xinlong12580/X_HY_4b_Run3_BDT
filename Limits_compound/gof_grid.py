import ROOT
import matplotlib.pyplot as plt
import numpy as np

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--fitdir', type=str, dest='fitdir',action='store', required=True)
parser.add_argument('--title', type=str, dest='title',action='store', required=True)
args = parser.parse_args()

import numpy as np
from scipy.optimize import curve_fit




with open("outputList/output_GOF_BDT.txt", "r") as _f:
    GOFs = _f.readlines()
f_string = args.fitdir.replace("/", "_").strip()
# Gaussian model: baseline + amplitude * exp(...)
def gaussian(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

years = ["2022", "2022EE", "2023", "2023BPix", "2024"]

obs_file = args.fitdir + "/higgsCombineSnapshot.GoodnessOfFit.mH125.root" 
toys = []
for toy_file in GOFs:
    #print(toy_file, f_string)
    if f_string not in toy_file:
        continue
    print(toy_file)
    rdf = ROOT.RDataFrame("limit", toy_file.strip())
    
    np_rdf = rdf.AsNumpy()
    print(np_rdf["limit"])
    _toys = np_rdf["limit"]
    _toys = [ _toys[i] for i in range(len(_toys)) if i%2 == 1 ]
    toys += _toys
fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1,1,1)
counts, bin_edges = np.histogram(toys, bins=np.linspace(min(toys), max(toys), 20))


# Compute bin centers
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# Poisson errors
errors = np.sqrt(counts)

ax.errorbar(bin_centers, counts, yerr=errors, fmt='o', capsize=3)

A0 = counts.max() - counts.min()
mu0 = bin_centers[np.argmax(counts)]
sigma0 = np.std(bin_centers)
p0 = [A0, mu0, sigma0]
fit_errors = np.where(errors == 0, 1, errors)

popt, pcov = curve_fit(
    gaussian,
    bin_centers,
    counts,
    p0=p0,
    sigma=fit_errors,
    absolute_sigma=True
)
A, mu, sigma = popt
x_fit = np.linspace(bin_centers.min(), bin_centers.max(), 1000)
y_fit = gaussian(x_fit, *popt)

f = ROOT.TFile.Open(obs_file, "READ")
tree = f.limit
for entry in tree:
    obs_limit = entry.limit
    break
print(obs_limit)


ax.plot(x_fit, y_fit, label=f'Gaussian fit\nμ={mu:.3g},sigma={abs(sigma):.3g}')


#p = sum([point > obs_limit for point in toys])/ len(toys)
tot=0
p=0
for i in range(len(x_fit) - 1):
    tot += (x_fit[i+1] - x_fit[i]) * (y_fit[i+1] + y_fit[i]) / 2
    if x_fit[i] > obs_limit:
        p += (x_fit[i+1] - x_fit[i]) * (y_fit[i+1] + y_fit[i]) / 2
p = p/tot
print(p)
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
ax.text(obs_limit+1, max(counts) * 0.9, f"p = {p:.4f}")
#plt.savefig(f"F_test.png")
ax.legend()
ax.set_title(f"Goodness Of Fit test, {args.title}")
fig.savefig(f"GOFs/{args.title}_grid.png")

