import ROOT
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
parser.add_argument('--years', type=str, dest='years',action='store', required=True)
args = parser.parse_args()
years = args.years.split(";")
#base_files = [ "datasets/" + f for f in os.listdir("datasets/") if (f.startswith("BKG") and (years[0] + "_") in f and args.mode in f and "merged" not in f) and (f.startswith("reweighted") and (years[0] + "__") in f and args.mode in f and "merged" not in f) ]
base_files = [ "datasets/" + f for f in os.listdir("datasets/") if (f.startswith("BKG") and (years[0] + "_") in f and args.mode in f and "merged" not in f) and 1 ]
for base_file in base_files:
    files = []
    for year in years:
        files.append(base_file.replace(years[0], year))
    rdf = ROOT.RDataFrame("Events",files)
    print("hadding files: ")
    print(files)
    out_year = args.years.replace(";", "_")
    out_year += "_merged"
    print(out_year)
    columns = ["BDT_weight", "Delta_Y", "Delta_Eta", "Tagger_H", "Tagger_Y", "Tagger_H_discrete", "Tagger_Y_discrete", "Tagger_H_decapitated", "Tagger_H_decapitated", "sample_ID", "year_ID", "MassHiggsCandidate.*" ]
    columns = "BDT_weight|Delta_.*|Tagger_.*|sample_ID|year_ID|MassHiggsCandidate.*|MX|MY|idx.*|Mass.*"
    rdf.Snapshot("Events", base_file.replace(years[0], out_year), columns)
