import ROOT
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--input_file', type=str, dest='input_file',action='store', required=True)
parser.add_argument('--DDT_file', type=str, dest='DDT_file',action='store', required=True)
args = parser.parse_args()
f = args.input_file
ROOT.gROOT.ProcessLine(".L DDT_map.cc+")
ROOT.gInterpreter.Declare('DDT_map Dmap;')
ROOT.gInterpreter.ProcessLine(f'Dmap.set_KNN("{args.DDT_file}");')
print("Procesing: ", f)

#ROOT.gInterpreter.Declare('DDT_map Dmap("handmade_2p1_discrete.txt", "[0]  + [1] * x  + [2] * y");')
rdf = ROOT.RDataFrame("Events", f.strip())
#rdf = rdf.Define("BDTG_threshold", f'Dmap.eval_KNN(MX, MY, 4, false)')
#rdf = rdf.Define("BDTG_threshold", f'Dmap.eval_KNN(MX, MY, 4, true)')
rdf = rdf.Define("BDTG_threshold", f'Dmap.eval_SQUARE(MX, MY, 4, true)')
rdf = rdf.Define("Region_SR1", f'BDTG > BDTG_threshold')
rdf = rdf.Define("Region_SB1", f"! Region_SR1")
rdf.Snapshot("Events", "DDT_" + os.path.basename(f))
