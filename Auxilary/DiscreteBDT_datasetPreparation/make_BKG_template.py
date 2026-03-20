import ROOT
ROOT.gROOT.SetBatch(True)
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--year', type=str, dest='year',action='store', required=True)
args = parser.parse_args()
rdf = ROOT.RDataFrame("Events", f"datasets/BKGs_RegSig_{args.mode}_{args.year}_ALL.root")
hist = rdf.Histo2D((f"BKGs_{args.mode}_{args.year}", f"BKGs_{args.mode}_{args.year}", 50, 0, 5000, 30, 0, 3000), "MX", "MY", "BDT_weight")
hist.SetMinimum(0.1)
#hist.SetMaximum(10)

hist.SetTitle(f"Background, {args.mode}, {args.year}")
hist.GetXaxis().SetTitle("M_{X}/GeV")
hist.GetYaxis().SetTitle("M_{Y}/GeV")
c = ROOT.TCanvas("c", "c")
hist.Draw("COLZ")
c.Print(f"All_BKGs_{args.mode}_{args.year}.png")
