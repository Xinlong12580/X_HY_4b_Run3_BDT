import ROOT
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--input_file', type=str, dest='input_file',action='store', required=True)
parser.add_argument('--DDT_file', type=str, dest='DDT_file',action='store', required=False)
args = parser.parse_args()
f = args.input_file
ROOT.gROOT.ProcessLine(".L DDT_map.cc+")
ROOT.gInterpreter.Declare('DDT_map Dmap;')
#ROOT.gInterpreter.ProcessLine(f'Dmap.set_KNN("{args.DDT_file}");')
#ROOT.gInterpreter.ProcessLine(f'Dmap.set_parametric("../../raw_namo/Dummy.txt", " (-1.3226e-04 * exp( 9.1526e-04* (x+y)) + 0.9951) - 0.009");')
#ROOT.gInterpreter.ProcessLine(f'Dmap.set_parametric("../../raw_namo/Dummy.txt", " ( -5.9954e-04 * exp (0.0014*x) +  0.9907) - 0.01" );')
#ROOT.gInterpreter.ProcessLine(f'Dmap.set_parametric("../../raw_namo/Dummy.txt", " ( -1e-5 * x + 0.98 )");')
ROOT.gInterpreter.ProcessLine(f'Dmap.set_parametric("../../raw_namo/Dummy.txt", " ( 0.98 )");')
print("Procesing: ", f)

#ROOT.gInterpreter.Declare('DDT_map Dmap("handmade_2p1_discrete.txt", "[0]  + [1] * x  + [2] * y");')
rdf = ROOT.RDataFrame("Events", f.strip())
rdf = rdf.Define("BDTG_threshold", f'Dmap.eval_parametric(MX, MY)')
#rdf = rdf.Define("BDTG_threshold", f'Dmap.eval_KNN(MX, MY, 4, true)')
#rdf = rdf.Define("BDTG_threshold", f'Dmap.eval_SQUARE(MX, MY, 4, true)')
rdf = rdf.Define("Region_SR1", f'BDTG > BDTG_threshold')
rdf = rdf.Define("Region_SB1", f"! Region_SR1")
rdf = rdf.Filter("sample_ID == 1")
print(rdf.Filter("Region_SR1").Sum("BDT_weight").GetValue())
print(rdf.Filter("Region_SB1").Sum("BDT_weight").GetValue())
print(rdf.Filter("Region_SR1").Sum("BDT_weight").GetValue()/ rdf.Filter("Region_SB1").Sum("BDT_weight").GetValue())
rdf.Snapshot("Events", "DDT_" + os.path.basename(f))
