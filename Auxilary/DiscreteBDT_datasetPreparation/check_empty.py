import ROOT
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
args = parser.parse_args()
f = ROOT.TFile.Open(args.f, "READ" )
tree = f.Get("Events")
if tree.GetEntries() < 1:
    print(1)
else:
    print(0)
