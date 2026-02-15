from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()

out_f = f"best_scores_discrete_{args.mode}_smooth.txt"

with open(f"best_scores_discrete_{args.mode}.txt", "r") as _f:
    lines = _f.readlines()
MXs = [float(line.split()[0]) for line in lines]
MYs = [float(line.split()[1]) for line in lines]
scores = [float(line.split()[2]) for line in lines]
if args.mode == "2p1":
    MXs_new = [MXs[i] for i in range(len(scores)) if MXs[i] > MYs[i] + 100 and MYs[i] >= 200]
    MYs_new = [MYs[i] for i in range(len(scores)) if MXs[i] > MYs[i] + 100 and MYs[i] >= 200]
    scores_new = [scores[i] for i in range(len(scores)) if MXs[i] > MYs[i] + 100 and MYs[i] >= 200]
    #MXs_new = [MXs[i] for i in range(len(scores)) if scores[i] > 0.75]
    #MYs_new = [MYs[i] for i in range(len(scores)) if scores[i] > 0.75]
    #scores_new = [scores[i] for i in range(len(scores)) if scores[i] > 0.75]
    MXs = MXs_new
    MYs = MYs_new
    scores = scores_new
scores_smooth = []
for i in range(len(scores)):
    MX = MXs[i]
    MY = MYs[i]
    score0 = scores[i]
    inds_left = [j for j in range(len(scores)) if MYs[j] == MY and MXs[j] < MX]
    inds_right = [j for j in range(len(scores)) if MYs[j] == MY and MXs[j] > MX]
    inds_up = [j for j in range(len(scores)) if MXs[j] == MX and MYs[j] > MY]
    inds_down = [j for j in range(len(scores)) if MXs[j] == MX and MYs[j] < MY]
    if len(inds_left) > 0:
        Ms = [MXs[j] for j in inds_left]
        ind_left = inds_left[Ms.index(max(Ms))]
    else:
        ind_left = i
    if len(inds_right) > 0:
        Ms = [MXs[j] for j in inds_right]
        ind_right = inds_right[Ms.index(min(Ms))]
    else:
        ind_right = i
    if len(inds_down) > 0:
        Ms = [MYs[j] for j in inds_down]
        ind_down = inds_down[Ms.index(max(Ms))]
    else:
        ind_down = i
    if len(inds_up) > 0:
        Ms = [MYs[j] for j in inds_up]
        ind_up = inds_up[Ms.index(min(Ms))]
    else:
        ind_up = i
    if (MX == 1600.0):
        print(MX, MY, MXs[ind_left], MXs[ind_right], MYs[ind_up], MYs[ind_down])
        print(scores[i], scores[ind_left], scores[ind_right], scores[ind_up], scores[ind_down])
    scores_smooth.append((scores[i] + scores[ind_left] + scores[ind_right] + scores[ind_up] + scores[ind_down]) / 5) 


with open(f"best_scores_discrete_{args.mode}_smooth.txt", "w") as _f:
    for i in range(len(scores)):
        _f.write(f"{MXs[i]} {MYs[i]} {scores_smooth[i]} \n")
    
