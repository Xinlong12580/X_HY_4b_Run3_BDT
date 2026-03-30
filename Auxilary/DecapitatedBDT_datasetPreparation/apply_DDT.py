import ROOT
from TIMBER.Tools.Common import CompileCpp, OpenJSON
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()

CompileCpp("DDT_map.cc")
#ROOT.gInterpreter.Declare(f'DDT_map Dmap("DDT_map_para_discrete_{args.mode}.txt", "0.8 + 0 * x * [5]");')
#ROOT.gInterpreter.Declare('DDT_map Dmap("raw_nano/DDT_map_para_discrete_{args.mode}.txt", "1.45/(1+exp(- [5] /x * ( [0] + [1]*x+[2]*y + [3]*x*x + [4]*y*y ))) - 0.5");')
#ROOT.gInterpreter.Declare('DDT_map Dmap("handmade_2p1_discrete.txt", "[0]  + [1] * x  + [2] * y");')
ROOT.gInterpreter.Declare(f'DDT_map Dmap("DDT_map_para_discrete_{args.mode}.txt", "0.8 + 0 * x * [5]");')
fs = os.listdir("datasets/")
for f in fs: 
    if ( not f.startswith("BDT") or "SignalMC" not in f or not args.mode in f or not "MX-4000_MY-2000" in f) and f != f"BDT_discrete_BKGs_{args.mode}_ALL.root":
        continue
    print("Procesing: ", f)
    input_f = "datasets/" + f

    rdf = ROOT.RDataFrame("Events", input_f)
    rdf = rdf.Define("BDTG_threshold", f'Dmap.eval(MX, MY)')
    rdf = rdf.Define("Region_SR1", f'BDTG > BDTG_threshold')
    rdf = rdf.Define("Region_SB1", f"! Region_SR1")
    rdf.Snapshot("Events", f"DDT_{args.mode}/DDT_" + f)
