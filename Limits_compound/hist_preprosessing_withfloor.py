import ROOT
from argparse import ArgumentParser
from XHY4b_Helper import *
import array
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f', action='store', required=True)
parser.add_argument('--mx', type=str, dest='mx', action='store', required=True)
parser.add_argument('--my', type=str, dest='my', action='store', required=True)
args = parser.parse_args()
if "1p1" in args.f:
    mode = "1p1"
elif "2p1" in args.f:
    mode = "2p1"
if "Signal" in args.f:
    Reg = "SR"
if "Validation" in args.f:
    Reg = "VR"
if "Control" in args.f:
    Reg = "CR"
if mode == "1p1":
    MJY_bins = array.array("d", [0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.3, 0.4, 0.5, 1.0])
    MJJ_bins = array.array("d", [0.8, 0.9, 1.0,  1.2, 1.4, 1.7, 2.0, 2.5, 3.0, 5.0] )
elif mode == "2p1":
    MJY_bins = array.array("d", [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0])
    MJJ_bins = array.array("d", [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.7, 2.0, 2.5, 3.0, 4.0, 5.0] )

 
f = ROOT.TFile.Open(args.f, "UPDATE")



years = ["2022", "2022EE", "2023", "2023BPix", "2024", "Allyears"]
regions = ["SR1", "SB1"]
for year in years:
    for region in regions:
        topPt_up = f.Get(f"{year}__MC_TTBarJets__{Reg}_{region}_{mode}__TopPtWeight_up")
        topPt_down = f.Get(f"{year}__MC_TTBarJets__{Reg}_{region}_{mode}__TopPtWeight_down")
        topPt_nom = f.Get(f"{year}__MC_TTBarJets__{Reg}_{region}_{mode}__nominal")
        print(topPt_nom.Integral(), topPt_up.Integral(), topPt_down.Integral())
        topPt_up.Scale(topPt_nom.Integral()/max(topPt_up.Integral(), 1e-6))
        topPt_down.Scale(topPt_nom.Integral()/max(topPt_down.Integral(), 1e-6))
        topPt_up.Write("",  ROOT.TObject.kOverwrite)
        topPt_down.Write("",  ROOT.TObject.kOverwrite)

years = ["2022", "2022EE", "2023", "2023BPix", "2024"]    
processes = ["JetMET", "MC_TTBarJets", f"SignalMC_XHY4b_MX-{args.mx}_MY-{args.my}"]
lumi_years = {"2022":0.014, "2023":0.013, "2024":0.016}
for lumi_year in lumi_years:
    for region in regions:
        for process in processes:
            base_hist = f.Get(f"Allyears__{process}__{Reg}_{region}_{mode}__nominal")
            up_hist = base_hist.Clone(f"Allyears__{process}__{Reg}_{region}_{mode}__Y{lumi_year}_lumi_up")
            up_hist.Reset()
            down_hist = up_hist.Clone(f"Allyears__{process}__{Reg}_{region}_{mode}__Y{lumi_year}_lumi_down")
            print(lumi_year, region, process)
            for year in years:
                year_base = f.Get(f"{year}__{process}__{Reg}_{region}_{mode}__nominal")
                if lumi_year in year:
                    print(f"{lumi_year} in {year}")
                    uncertainty = lumi_years[lumi_year]
                    up_year = year_base.Clone()
                    down_year = year_base.Clone()
                    up_year.SetDirectory(0)
                    down_year.SetDirectory(0)

                    up_year.Scale(1.0 + uncertainty)
                    down_year.Scale(1.0 / (1.0 + uncertainty))

                    up_hist.Add(up_year)
                    down_hist.Add(down_year)
                else:
                    #print(f"{lumi_year} not in {year}")
                    up_hist.Add(year_base)
                    down_hist.Add(year_base)
            print(up_hist.GetName(), up_hist.Integral()) 
            print(down_hist.GetName(), down_hist.Integral()) 
            up_hist.Write("",  ROOT.TObject.kOverwrite)
            down_hist.Write("",  ROOT.TObject.kOverwrite)        
'''
def resetBins(h2):
    for i in range(h2.GetNbinsX()):
        for j in range(h2.GetNbinsY()):
            h2.SetBinContent(i+1, j+1, max(h2.GetBinContent(i+1, j+1), 1e-7 ))
keys = f.GetListOfKeys()
key_names = [key.GetName() for key in keys]
print(len(key_names))
for key_name in key_names :
    if "JetMET" not in key_name and "Allyears" in key_name and "QCDJets" not in key_name:
        h2 = f.Get(key_name)
        print(h2.GetName())
        resetBins(h2)
        h2.Write("",  ROOT.TObject.kOverwrite)
'''

print("REBINNING###############################################################")
f_out = ROOT.TFile.Open(args.f.replace(".root", "_rebinned.root"), "RECREATE")
'''
for key in f.GetListOfKeys():
    if not ("TTBar" in key.GetName() or "SignalMC" in key.GetName() or ("JetMET" in key.GetName() and "nominal" in key.GetName() ) ):
        continue
    hist = key.ReadObj()
    print("rebinning ", hist.GetName())
    if "TTBar" in key.GetName() and ("2024" in key.GetName() or "Allyears" in key.GetName()): 
        hist = rebin_TH2(hist,  MJY_bins, MJJ_bins, "rebinned_" + hist.GetName(), forceOutputPositive = True, outputFloor = 0.5)
    else:
        hist = rebin_TH2(hist,  MJY_bins, MJJ_bins, "rebinned_" + hist.GetName(), forceOutputPositive = True, outputFloor = 0)
    hist.SetDirectory(f_out)
    hist.Write()
'''
'''
import gc

ROOT.TH1.AddDirectory(False)
processed = 0
for key in f.GetListOfKeys():
    name = key.GetName()
    if not ("TTBar" in name or "SignalMC" in name or ("JetMET" in name and "nominal" in name)):
        continue

    source_hist = key.ReadObj()
    print("rebinning", name)

    if "TTBar" in key.GetName() and ("2024" in key.GetName() or "Allyears" in key.GetName()): 
        rebinned_hist = rebin_TH2( source_hist,MJY_bins, MJJ_bins, "rebinned_" + name, forceOutputPositive=True,outputFloor = 0.5)
    else:
        rebinned_hist = rebin_TH2( source_hist,MJY_bins, MJJ_bins, "rebinned_" + name, forceOutputPositive=True,outputFloor = 0)

    f_out.cd()
    rebinned_hist.Write()
    del rebinned_hist
    del source_hist

    #if key.GetCycle() % 100 == 0:
    #    gc.collect()

    processed += 1
    if processed % 100 == 0:
        gc.collect()
print("Finishing preprocessing") 
'''

f.Close()
f_out.Close()

