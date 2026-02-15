import numpy as np
import matplotlib.pyplot as plt

# Load data from file
data = np.loadtxt(f"eff_compound.txt")

# Separate into columns
MX_vals = data[:, 0]
MY_vals = data[:, 1]
eff_vals = {}
eff_vals["1"] = data[:, 2]
eff_vals["2"] = data[:, 3]
eff_vals["1not2"] = data[:, 4]
eff_vals["2not1"] = data[:, 5]
eff_vals["1and2"] = data[:, 6]
titles = {}
titles["1"] = "1+1"
titles["2"] = "2+1"
titles["1not2"] = "1+1 && !(2+1)"
titles["2not1"] = "2+1 && !(1+1)"
titles["1and2"] = "1+1 && 2+1"
for channel in eff_vals:
    print(channel)
    # Create scatter plot with colormap
    plt.figure(figsize=(10, 6))
    #sc = plt.scatter(MX_vals, MY_vals, c=eff_vals, cmap="hot", s=100, edgecolors='k', vmin=0.0, vmax=0.08)
    sc = plt.scatter(MX_vals, MY_vals, c=eff_vals[channel], cmap="viridis", s=100, edgecolors='k', vmin=0.0, vmax=0.2)

    # Add colorbar
    cbar = plt.colorbar(sc)
    cbar.set_label("Efficiency")

    # Axis labels and title
    plt.xlabel("MX")
    plt.ylabel("MY")
    plt.title(f"Reconstruction efficiency {titles[channel]}")
    plt.grid(True)
    plt.tight_layout()
    # Save plot
    plt.savefig(f"compound_linear_gen_eff_map_{channel}.png", dpi=300)
    plt.yscale("log")
    plt.xscale("log")
    plt.savefig(f"compound_log_gen_eff_map_{channel}.png", dpi=300)
