import ROOT
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
parser.add_argument('--mx', type=str, dest='mx',action='store', required=True)
parser.add_argument('--my', type=str, dest='my',action='store', required=True)
parser.add_argument('--BDTG1', type=str, dest='BDTG1',action='store', required=True)
parser.add_argument('--BDTG2', type=str, dest='BDTG2',action='store', required=True)
args = parser.parse_args()

sig1_rdf = ROOT.RDataFrame("Events", f"datasets/{args.BDTG1}_reweighted_RegSig_nom_{args.mode}_tagged_selected_SKIM_skimmed_{args.year}__SignalMC_XHY4b__MX-{args.mx}_MY-{args.my}_{args.mode}_ALL.root") 
sig2_rdf =ROOT.RDataFrame("Events", f"datasets/{args.BDTG2}_reweighted_RegSig_nom_{args.mode}_tagged_selected_SKIM_skimmed_{args.year}__SignalMC_XHY4b__MX-{args.mx}_MY-{args.my}_{args.mode}_ALL.root")
bkg1_rdf = ROOT.RDataFrame("Events", f"datasets/{args.BDTG1}_BKGs_RegSig_{args.mode}_{args.year}_ALL.root")
bkg2_rdf = ROOT.RDataFrame("Events", f"datasets/{args.BDTG2}_BKGs_RegSig_{args.mode}_{args.year}_ALL.root" )
base_cut = "MX > 2000"
sig1_rdf = sig1_rdf.Filter(base_cut)
sig2_rdf = sig2_rdf.Filter(base_cut)
bkg1_rdf = bkg1_rdf.Filter(base_cut)
bkg2_rdf = bkg2_rdf.Filter(base_cut)

scores = [-1, 0, 1]
scores = np.linspace(-1, 1, 201) 

sig2bkgs1 = []
bkgEffs1 = []
sigEffs1 = []
sig2bkgs2 = []
bkgEffs2 = []
sigEffs2 = []
N_sig1_total = sig1_rdf.Sum("BDT_weight").GetValue()
N_bkg1_total = bkg1_rdf.Sum("BDT_weight").GetValue()
N_sig2_total = sig2_rdf.Sum("BDT_weight").GetValue()
N_bkg2_total = bkg2_rdf.Sum("BDT_weight").GetValue()
for score in scores:
    print(score)
    weight = "BDT_weight" 
    cut = f"BDTG > {score}"
    rdfN_sig1 = sig1_rdf.Filter(cut).Sum(weight)
    rdfN_bkg1 = bkg1_rdf.Filter(cut).Sum(weight)
    N_sig1 = rdfN_sig1.GetValue() 
    N_bkg1 = rdfN_bkg1.GetValue()
    sig2bkg1 = N_sig1 / (1 + np.sqrt(N_bkg1))
    sig2bkgs1.append(sig2bkg1)
    bkgEffs1.append(N_bkg1/N_bkg1_total if N_bkg1_total != 0 else float('nan'))
    sigEffs1.append(N_sig1/N_sig1_total if N_sig1_total != 0 else float('nan') )
    
    rdfN_sig2 = sig2_rdf.Filter(cut).Sum(weight)
    rdfN_bkg2 = bkg2_rdf.Filter(cut).Sum(weight)
    N_sig2 = rdfN_sig2.GetValue() 
    N_bkg2 = rdfN_bkg2.GetValue()
    sig2bkg2 = N_sig2 / (2 + np.sqrt(N_bkg2))
    sig2bkgs2.append(sig2bkg2)
    bkgEffs2.append(N_bkg2/N_bkg2_total if N_bkg2_total != 0 else float('nan'))
    sigEffs2.append(N_sig2/N_sig2_total if N_sig2_total != 0 else float('nan') )
print(sig2bkgs1)
print(sig2bkgs2)
print(sigEffs1)
print(sigEffs2)
print(bkgEffs1)
print(bkgEffs2)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(sigEffs1, bkgEffs1, label = args.BDTG1)
ax.plot(sigEffs2, bkgEffs2, label = args.BDTG2 )
ax.set_xlabel("sig_eff")
ax.set_ylabel("bkg_eff")
ax.set_title(f"ROC for mass point MX {args.mx}GeV, MY {args.my}GeV, {args.mode}, {args.year}")
ax.legend()
fig.savefig(f"plots/compareBDTGs/ROC_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}.png")

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(scores, sig2bkgs1, label = args.BDTG1)
ax.plot(scores, sig2bkgs2, label = args.BDTG2 )
ax.set_xlabel("score")
ax.set_ylabel("Punzi significance")
ax.set_title(f"Punzi significance for mass point MX {args.mx}GeV, MY {args.my}GeV, {args.mode}, {args.year}")
ax.legend()
fig.savefig(f"plots/compareBDTGs/PunziSig_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}.png")



