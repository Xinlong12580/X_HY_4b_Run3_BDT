import ROOT
ROOT.gROOT.SetBatch(True)
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()
rdf = ROOT.RDataFrame("Events", f"datasets/BKGs_{args.mode}_ALL.root")
rdf = rdf.Filter("PNet_H > 0.3 && PNet_Y > 0.3")
hist = rdf.Histo2D((f"BKGs_{args.mode}", "BKGs_{args.mode}", 100, 0, 1000, 300, 0, 3000), "MY", "MX", "BDT_weight")

c = ROOT.TCanvas("c", "c")
hist.Draw("COLZ")
c.Print(f"All_BKGs_{args.mode}.png")
