import ROOT
ROOT.gROOT.SetBatch(True)
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()
rdf = ROOT.RDataFrame("Events", f"datasets/BKGs_{args.mode}_ALL.root")
rdf = rdf.Filter("minPNet > 0.3")
hist = rdf.Histo2D((f"BKGs_{args.mode}", f"BKGs_{args.mode}", 100, 0, 5000, 100, 0, 3000), "MX", "MY", "BDT_weight")

c = ROOT.TCanvas("c", "c")
hist.Draw("COLZ")
c.Print(f"All_BKGs_{args.mode}.png")
