import ROOT
from argparse import ArgumentParser
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

 
f = ROOT.TFile.Open(args.f, "UPDATE")
years = ["2022", "2022EE", "2023", "2023BPix", "2024", "Allyears"]
regions = ["SR1", "SB1"]
for year in years:
    for region in regions:
        topPt_up = f.Get(f"{year}__MC_TTBarJets__{Reg}_{region}_{mode}__TopPtWeight_up")
        topPt_down = f.Get(f"{year}__MC_TTBarJets__{Reg}_{region}_{mode}__TopPtWeight_down")
        topPt_nom = f.Get(f"{year}__MC_TTBarJets__{Reg}_{region}_{mode}__nominal")
        print(topPt_nom.Integral(), topPt_up.Integral(), topPt_down.Integral())
        topPt_up.Scale(topPt_nom.Integral()/topPt_up.Integral())
        topPt_down.Scale(topPt_nom.Integral()/topPt_down.Integral())
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
                    year_base.Scale(1 + lumi_years[lumi_year])
                    up_hist.Add(year_base)
                    year_base.Scale(1/ (1 + lumi_years[lumi_year])) # Revserve the opration above
                    year_base.Scale(1/ (1 + lumi_years[lumi_year])) #rescale
                    down_hist.Add(year_base)
                else:
                    print(f"{lumi_year} not in {year}")
                    up_hist.Add(year_base)
                    down_hist.Add(year_base)
            print(up_hist.GetName(), up_hist.Integral()) 
            print(down_hist.GetName(), down_hist.Integral()) 
            print("TEST1")
            up_hist.Write("",  ROOT.TObject.kOverwrite)
            down_hist.Write("",  ROOT.TObject.kOverwrite)        
            print("TEST2")
f.Close()
exit()
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

print("Finishing preprocessing") 

f.Close()

