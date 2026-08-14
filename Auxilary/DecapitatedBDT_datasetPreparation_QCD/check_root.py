import ROOT
from argparse import ArgumentParser
ROOT.gROOT.SetBatch(True)
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
args = parser.parse_args()
f = ROOT.RDataFrame("Events", args.f)
f = f.Filter("year_ID == 2")
print(f.Filter("sample_ID == 2").Count().GetValue())
print(f.Filter("sample_ID == 2").Sum("BDT_weight").GetValue())

print(f.Filter("sample_ID == 2 && Region_SR1").Sum("BDT_weight").GetValue())

