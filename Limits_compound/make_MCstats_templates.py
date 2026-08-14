import ROOT
from argparse import ArgumentParser
import array
from XHY4b_Helper import *
parser=ArgumentParser()

parser.add_argument('-f', type=str, action='store', required=True)
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
counterpart={"SR1":"SB1", "SB1":"SR1"}
for region in ["SR1", "SB1"]:
    TTBar = f.Get(f"rebinned_Allyears__MC_TTBarJets__{Reg}_{region}_{mode}__nominal")
    TTBar_counterpart = f.Get(f"rebinned_Allyears__MC_TTBarJets__{Reg}_{counterpart[region]}_{mode}__nominal")
    nbins_x = TTBar.GetNbinsX()
    nbins_y = TTBar.GetNbinsY()


    for i in range(nbins_x):
        for j in range(nbins_y):
            content_i_j = TTBar.GetBinContent(i + 1, j + 1)
            errorup_i_j = TTBar.GetBinErrorUp(i + 1, j + 1)
            errorlow_i_j = TTBar.GetBinErrorLow(i + 1, j + 1)
            if TTBar.GetXaxis().GetBinLowEdge(i) >= TTBar.GetYaxis().GetBinUpEdge(j) - 1e-3: continue
            if (content_i_j <= 1e-6): continue
            
            #TTBar_up = TTBar.Clone(f"rebinned_Allyears__MC_TTBarJets_{Reg}_{region}_{mode}_Region0_MCstat_{Reg}_{region}_{mode}_{i}_{j}_up")
            #TTBar_down = TTBar.Clone(f"rebinned_Allyears__MC_TTBarJets_{Reg}_{region}_{mode}_Region0_MCstat_{Reg}_{region}_{mode}_{i}_{j}_down")
            #TTBar_up_counterpart = TTBar.Clone(f"rebinned_Allyears__MC_TTBarJets_{Reg}_{counterpart[region]}_{mode}_Region0_MCstat_{Reg}_{region}_{mode}_{i}_{j}_up")
            #TTBar_down_counterpart = TTBar.Clone(f"rebinned_Allyears__MC_TTBarJets_{Reg}_{counterpart[region]}_{mode}_Region0_MCstat_{Reg}_{region}_{mode}_{i}_{j}_down")
            TTBar_up = TTBar.Clone(f"rebinned_Allyears__MC_TTBarJets__{Reg}_{region}_{mode}__MCstat_{Reg}_{region}_{mode.upper()}_{i}_{j}_up")#Using upper case to avoid coincide with the region name
            TTBar_down = TTBar.Clone(f"rebinned_Allyears__MC_TTBarJets__{Reg}_{region}_{mode}__MCstat_{Reg}_{region}_{mode.upper()}_{i}_{j}_down")
            TTBar_up_counterpart = TTBar_counterpart.Clone(f"rebinned_Allyears__MC_TTBarJets__{Reg}_{counterpart[region]}_{mode}__MCstat_{Reg}_{region}_{mode.upper()}_{i}_{j}_up")
            TTBar_down_counterpart = TTBar_counterpart.Clone(f"rebinned_Allyears__MC_TTBarJets__{Reg}_{counterpart[region]}_{mode}__MCstat_{Reg}_{region}_{mode.upper()}_{i}_{j}_down")
            print(i, j, content_i_j, errorup_i_j, errorlow_i_j)
            TTBar_up.SetBinContent(i + 1, j + 1, content_i_j + errorup_i_j )
            TTBar_down.SetBinContent(i + 1, j + 1, content_i_j - errorlow_i_j )
            TTBar_up.Write()
            TTBar_down.Write()
            TTBar_up_counterpart.Write()
            TTBar_down_counterpart.Write()

f.Close()

