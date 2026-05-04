import ROOT

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--fname', type=str, dest='fname',action='store', required=True)
parser.add_argument('--r1', type=str, dest='r1',action='store', required=True)
parser.add_argument('--r2', type=str, dest='r2',action='store', required=True)
args = parser.parse_args()

region1 = args.r1
region2 = args.r2
fname = args.fname
f = ROOT.TFile.Open(fname, "UPDATE")
f.cd()
for key in f.GetListOfKeys():
    hist1 = key.ReadObj()
    if isinstance(hist1, ROOT.TH2):
        hist1_name = hist1.GetName()
        if ( "_" + region1 + "_") in hist1_name:
            hist2_name = hist1_name.replace(region1, region2)
            hist2 = f.Get(hist2_name)
            print("calculating: ", hist1_name, "-", hist2_name)
            histnew_name = hist1_name.replace(region1, region1 + "m" + region2)
            hist_new = hist1.Clone(histnew_name)
            hist_new.SetTitle(histnew_name)
            hist_new.Add(hist2, -1)
            hist_new.Write()
f.Close()      
