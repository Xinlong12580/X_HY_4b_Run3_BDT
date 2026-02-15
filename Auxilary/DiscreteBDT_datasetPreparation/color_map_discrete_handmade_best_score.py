import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()
# Load data from file
data = np.loadtxt(f"handmade_score_discrete_{args.mode}.txt")
#data = np.loadtxt("Y_matching_eff.txt")

# Separate into columns
MX_vals = data[:, 0]
MY_vals = data[:, 1]

# Create scatter plot with colormap
plt.figure(figsize=(10, 6))
#sc = plt.scatter(MX_vals, MY_vals, c=effs_vals, cmap="viridis", s=100, edgecolors='k', vmin=0.0, vmax=0.3)
#sc = plt.scatter(MX_vals, MY_vals, c=effs_vals, cmap="viridis", s=100, edgecolors='k', norm=LogNorm())
#sc = plt.scatter(MX_vals, MY_vals, c=data[:, 2], cmap="viridis", s=100, edgecolors='k')
sc = plt.scatter(MX_vals, MY_vals, c=data[:, 2], cmap="viridis", s=100, edgecolors='k', vmin = -1, vmax = 1)
#sc = plt.scatter(MX_vals, MY_vals, c=effs_vals[mode], cmap="viridis", s=100, edgecolors='k', vmin=0.0, vmax=1)
#sc = plt.scatter(MX_vals, MY_vals, c=effs_vals[mode], cmap="hot_r", s=100, edgecolors='k', vmin=0.0, vmax=1)

# Add colorbar
cbar = plt.colorbar(sc)
cbar.set_label("Efficiency")

# Axis labels and title
plt.xlabel("MX")
plt.ylabel("MY")
plt.xlim(10, 4100)
plt.ylim(10, 3600)
plt.title(f"best_BDT_score_{args.mode}")
#plt.title("Y Matching Efficiency Map (MX vs. MY)")
plt.grid(True)
#plt.yscale("log")
plt.tight_layout()

# Save plot
plt.savefig(f"linear_handmade_BDT_score_discrete_{args.mode}.png", dpi=300)
plt.xscale("log")
plt.yscale("log")
plt.savefig(f"log_best_handmade_score_discrete_{args.mode}.png", dpi=300)

#plt.savefig("Y_eff_map.png", dpi=300)
