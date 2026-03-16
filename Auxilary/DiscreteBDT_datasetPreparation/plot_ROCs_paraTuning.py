import matplotlib.pyplot as plt
import pickle

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
args = parser.parse_args()

with open(f"ROCs_{args.mode}_{args.year}.pkl", "rb") as f:
    ROCs = pickle.load(f)
    AUCs = pickle.load(f)
fig = plt.figure(figsize= (15, 6))

gs = fig.add_gridspec(1, 2, width_ratios=[1,1])

ax = fig.add_subplot(gs[0])      
ax_leg = fig.add_subplot(gs[1]) 

handles = []
max_AUC = 0
max_config = ""
max_leg = ""
count = 0
for config_name in ROCs:
    paras = config_name.split("_")
    para_names = ["Method", "NTree", "MinNodeSize", "Shrinkage", "BaggedSampleFraction", "nCuts", "MaxDepth"]
    leg_str = ""
    for i in range(len(paras)):
        if i == 0:
            continue
        if i == 5:
            leg_str += "\n"
        #print(paras[i])
        #if paras[i].isdigit() and "." in paras[i]:
        if "." in paras[i]:
            leg_str += (para_names[i] + "=" + f"{float(paras[i]):.2f}" + " ")
        else:
            leg_str += (para_names[i] + "=" + paras[i] + " ")
    if AUCs[config_name] > max_AUC:
        max_AUC = AUCs[config_name]
        max_config = config_name
        max_leg = leg_str
    if count % 10 == 0:
        print(count)
        handle, = ax.plot(ROCs[config_name]["X"], ROCs[config_name]["Y"], label = f"{leg_str}, AUC={AUCs[config_name]:.3f}")
        handles.append(handle)
    count += 1

handle, = ax.plot(ROCs[max_config]["X"], ROCs[max_config]["Y"], label = f"{max_leg}, AUC={AUCs[max_config]:.3f}")
handles.append(handle)
ax_leg.axis("off")
ax_leg.legend(handles=handles)
ax.set_title(f"ROCs for parameter tuning, {args.mode} channel, year {args.year}")
ax.set_xlabel("Signal Efficiency")
ax.set_ylabel("Background Rejection Rate")
#ax.legend()
fig.savefig(f"ROCs_{args.mode}_{args.year}.png")
print(max_AUC, max_config)
with open(f"max_config_{args.mode}_{args.year}.txt", "w") as f:
    f.write(f"{max_config}\n")
