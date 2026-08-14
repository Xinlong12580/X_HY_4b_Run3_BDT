import ROOT 
from argparse import ArgumentParser

#Reading input args
parser=ArgumentParser()
parser.add_argument('--1p1', type=str, dest='f1p1',action='store', required=True)
parser.add_argument('--2p1', type=str, dest='f2p1',action='store', required=True)
parser.add_argument('--combined', type=str, dest='fcombined',action='store', required=True)
args = parser.parse_args()

f_combined = args.fcombined
f_1p1 = args.f1p1
f_2p1 = args.f2p1 
rdf_1p1 = ROOT.RDataFrame("Events", f_1p1)
rdf_2p1 = ROOT.RDataFrame("Events", f_2p1)
rdf_combined = ROOT.RDataFrame("Events", f_combined)

print(rdf_combined.Count().GetValue())
print(rdf_combined.Filter("flag1p1").Count().GetValue())
print(rdf_combined.Filter("flag2p1").Count().GetValue())
print(rdf_1p1.Count().GetValue())
print(rdf_2p1.Count().GetValue())

with open("check_combined.txt", "a+") as f:
    f.write(f"{f_1p1} {f_2p1} {f_combined}\n")
    f.write(f'{rdf_1p1.Count().GetValue()} {rdf_2p1.Count().GetValue()} {rdf_combined.Filter("flag1p1").Count().GetValue()} {rdf_combined.Filter("flag2p1").Count().GetValue()}\n')
    f.write(f'{rdf_1p1.Sum("weight_All__nominal").GetValue()} {rdf_2p1.Sum("weight_All__nominal").GetValue()} {rdf_combined.Filter("flag1p1").Sum("weight_1p1__nominal").GetValue()} {rdf_combined.Filter("flag2p1").Sum("weight_2p1__nominal").GetValue()}\n')
    f.write(f'{rdf_1p1.Sum("genWeight").GetValue()} {rdf_2p1.Sum("genWeight").GetValue()} {rdf_combined.Filter("flag1p1").Sum("genWeight").GetValue()} {rdf_combined.Filter("flag2p1").Sum("genWeight").GetValue()}\n')
