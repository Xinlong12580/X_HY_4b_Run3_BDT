import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
parser.add_argument('--mx', type=str, dest='mx',action='store', required=True)
parser.add_argument('--my', type=str, dest='my',action='store', required=True)
parser.add_argument('--method', type=int, dest='method',action='store', required=True)
args = parser.parse_args()
# Load data from file
#data = np.loadtxt("Y_matching_eff.txt")
if args.method == 0:
    data = np.loadtxt(f"best_scores_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}_0.txt", skiprows = 1)
    save_dir= "plots/best_scores/"
    title_string = "from local optimization"
elif args.method == 1:
    data = np.loadtxt(f"best_scores_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}_1.txt", skiprows = 1)
    save_dir= "plots/good_P2Fs/"
    title_string = "from adjusting QCD P/F"
# Separate into columns
MX_vals = data[:, 0]
MY_vals = data[:, 1]

# Create scatter plot with colormap
plt.figure(figsize=(10, 6))
#sc = plt.scatter(MX_vals, MY_vals, c=effs_vals, cmap="viridis", s=100, edgecolors='k', vmin=0.0, vmax=0.3)
#sc = plt.scatter(MX_vals, MY_vals, c=effs_vals, cmap="viridis", s=100, edgecolors='k', norm=LogNorm())
#sc = plt.scatter(MX_vals, MY_vals, c=data[:, 2], cmap="viridis", s=100, edgecolors='k')
sc = plt.scatter(MX_vals, MY_vals, c=data[:, 2], cmap="viridis", s=100, edgecolors='k', vmin=-1, vmax=1)
#sc = plt.scatter(MX_vals, MY_vals, c=effs_vals[mode], cmap="viridis", s=100, edgecolors='k', vmin=0.0, vmax=1)
#sc = plt.scatter(MX_vals, MY_vals, c=effs_vals[mode], cmap="hot_r", s=100, edgecolors='k', vminvmax=1=0.0, vmax=1)

# Add colorbar
cbar = plt.colorbar(sc)

# Axis labels and title
plt.xlabel(r"$M_X/GeV$")
plt.ylabel(r"$M_Y/GeV$")
plt.title(r"$BDTG_{threshold}(M_X, M_Y)$ " + f"{title_string}, \n Training set: MX{args.mx}_MY{args.my}GeV, {args.mode}, {args.year}")
#plt.title("Y Matching Efficiency Map (MX vs. MY)")
plt.grid(True)
#plt.yscale("log")
plt.tight_layout()

# Save plot
plt.savefig(f"{save_dir}/linear_best_BDT_score_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}.png", dpi=300)
plt.xscale("log")
plt.yscale("log")
plt.savefig(f"{save_dir}/log_best_BDT_score_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}.png", dpi=300)

#plt.savefig("Y_eff_map.png", dpi=300)
labels = ["BDT_Scores", "Punzi_Significance", "Signal_Efficiency", "Background_Efficiency", "QCD_Efficiency", "QCD_Pass_to_Fail_ratio", "TTBar_Efficiency"]

for i in range(len(labels)): 

    # Create scatter plot with colormap
    plt.figure(figsize=(10, 6))
    #sc = plt.scatter(MX_vals, MY_vals, c=data[:, 2 + i], norm=LogNorm(), cmap="viridis", s=100, edgecolors='k', vmax=0.01)
    sc = plt.scatter(MX_vals, MY_vals, c=data[:, 2 + i], cmap="viridis", s=100, edgecolors='k')

    cbar = plt.colorbar(sc)

    plt.xlabel(r"$M_X/GeV$")
    plt.ylabel(r"$M_Y/GeV$")
    plt.title(f"{labels[i]} {title_string},\n " + f"Training Set: MX{args.mx}_MY{args.my}GeV {args.mode}, {args.year}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/linear_{labels[i]}_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}.png", dpi=300)
    plt.xscale("log")
    plt.yscale("log")
    plt.savefig(f"{save_dir}/log_{labels[i]}_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}.png", dpi=300)

MYs = []
for MY in data[:, 1]:
    if MY not in MYs:
        MYs.append(MY)
for MY in MYs:
    MXs_raw = [ data[ind, 0] for ind in range(len(data[:,0])) if data[ind, 1] == MY and data[ind, 0] > 700 ]
    for i in range(len(labels)):
        # Create scatter plot with colormap
        plt.figure(figsize=(10, 6))
        #sc = plt.scatter(MX_vals, MY_vals, c=data[:, 2 + i], norm=LogNorm(), cmap="viridis", s=100, edgecolors='k', vmax=0.01)
        vals_raw = [ data[ind, i + 2] for ind in range(len(data[:,0])) if data[ind, 1] == MY and data[ind, 0] > 700 ]
        _pass = 0
        for val in vals_raw:
            if val > 0:
                _pass = 1
                break
        if _pass == 0: continue 
        MXs, vals = zip(*sorted(zip(MXs_raw, vals_raw)))
        plt.plot(MXs,vals )

        plt.xlabel(r"$M_X/GeV$")
        plt.ylabel(r"{labels[i]}")
        plt.title(f"{labels[i]} {title_string}, MY = {MY}; " + f"{args.mode}, {args.year}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{save_dir}/linear_SliceMY{MY}_{labels[i]}_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}.png", dpi=300)
        plt.xscale("log")
        plt.yscale("log")
        plt.savefig(f"{save_dir}/log_SliceMY{MY}_{labels[i]}_discrete_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}.png", dpi=300) 
