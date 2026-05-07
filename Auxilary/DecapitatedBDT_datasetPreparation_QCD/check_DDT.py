import ROOT
import array
from argparse import ArgumentParser
ROOT.gROOT.SetBatch(True)
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
args = parser.parse_args()


rdf = ROOT.RDataFrame("Events", args.f)
rdf = rdf.Filter("event_Idx%2 == 1")
n_pass = rdf.Filter("Region_SR1").Filter("sample_ID == 2").Sum("BDT_weight").GetValue()
n_fail = rdf.Filter("Region_SB1").Filter("sample_ID == 2").Sum("BDT_weight").GetValue()
print(n_pass, n_fail, n_pass/n_fail)

if "1p1" in args.f:
    base_x_bins = [0.2, 0.4, 0.6, 0.8,0.9,1.0, 1.1, 1.2, 1.3, 1.4, 1.7, 2.0, 2.3, 2.6, 3.0, 3.5, 4.0, 5.0]
    base_y_bins = [0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.17, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.7, 2.0, 2.5, 3.0, 4.0]
    MX_bins = array.array("d", [1000 * edge for edge in base_x_bins] ) 
    MY_bins = array.array("d", [1000 * edge for edge in base_y_bins] ) 
if "2p1" in args.f:
    base_x_bins = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,0.9,1.0, 1.2, 1.4, 1.7, 2.0, 2.3, 2.6, 3.0, 3.5, 4.0, 5.0]
    base_y_bins = [[0.2,  0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0]
    MX_bins = array.array("d", [1000 * edge for edge in base_x_bins] ) 
    MY_bins = array.array("d", [1000 * edge for edge in base_y_bins] ) 
h2_pass = rdf.Filter("Region_SR1").Filter("sample_ID == 2").Histo2D(("h2_pass", "h2_fail", len(MX_bins) - 1, MX_bins, len(MY_bins) - 1, MY_bins), "MX", "MY", "BDT_weight").GetValue()
h2_fail = rdf.Filter("Region_SB1").Filter("sample_ID == 2").Histo2D(("h2_pass", "h2_fail", len(MX_bins) - 1, MX_bins, len(MY_bins) - 1, MY_bins), "MX", "MY", "BDT_weight").GetValue()

h2_pass_x = h2_pass.ProjectionX("h2_pass_x")
h2_pass_y = h2_pass.ProjectionY("h2_pass_y")
h2_fail_x = h2_fail.ProjectionX("h2_fail_x")
h2_fail_y = h2_fail.ProjectionY("h2_fail_y")
h2_ratio_x = h2_pass_x.Clone("h2_ratio_x")
h2_ratio_x.Divide(h2_fail_x)
h2_ratio_y = h2_pass_y.Clone("h2_ratio_y")
h2_ratio_y.Divide(h2_fail_y)

h2_ratio_x.SetMaximum(0.01)
h2_ratio_x.SetMinimum(0)
h2_ratio_y.SetMaximum(0.01)
h2_ratio_y.SetMinimum(0)

c = ROOT.TCanvas()
h2_ratio_x.Draw("E")
c.Update()
c.Print(args.f.replace(".root", "_ratio_x.png"))

c = ROOT.TCanvas()
h2_ratio_y.Draw("E")
c.Update()
c.Print(args.f.replace(".root", "_ratio_y.png"))
