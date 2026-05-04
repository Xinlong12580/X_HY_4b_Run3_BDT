import numpy as np
import matplotlib.pyplot as plt
import mplhep
from hist import Hist
import ROOT
import array
import json
import pickle
from XHY4b_Helper import *
ROOT.gROOT.SetBatch(True)
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--mode', type=str, dest='mode',action='store', required=True)
args = parser.parse_args()

years = ["2022", "2022EE", "2023", "2023BPix", "2024"]
#years = ["2022", "2022EE", "2023", "2023BPix"]
processes = {"MC_WZJets": ["*"], "MC_TTBarJets": ["*"], "MC_QCDJets": ["*"], "SignalMC_XHY4b": ["MX-3000_MY-300"]}
processes = {"MC_TTBarJets": ["*"]}
processes = {"MC_TTBarJets": ["*"], "MC_QCDJets": ["*"]}
regions = ["SR1", "SB1"]

MJY_bins = array.array("d", np.linspace(0, 1000, 11) )
MJJ_bins = array.array("d", np.linspace(0, 3000, 21) )
MJY_bins = array.array("d",[40, 100, 140,  200, 300,  600,  800 ,1000])
MJY_bins = array.array("d", [200,  300, 400, 500, 600, 700, 800, 900,1000, 1200, 1500, 2000, 3000, 4000, 5000])
MJY_bins = array.array("d", [200,  300, 400, 500, 600, 700, 800, 900,1000, 1200, 1500, 2000, 2500, 3000,  4000, 5000])
MJJ_bins = array.array("d", [300, 400, 500, 600, 700, 800,900,1000, 1200, 1500, 2000, 2500, 3000,  4000, 5000] )
MJY_bins = array.array("d", [200, 400,  600,  800, 1000, 1200, 1500, 2000, 2500, 3000,  4000, 5000])
MJJ_bins = array.array("d", [300,  500,  700, 900, 1200, 1500, 2000, 2500, 3000,  4000, 5000] )
#MJY_bins = array.array("d", np.linspace(0, 3000, 16) )
#MJJ_bins = array.array("d", np.linspace(0, 5000, 26) )
nbins_x = len(MJY_bins) - 1
nbins_y = len(MJJ_bins) - 1
h_base = ROOT.TH2D("Mass", "MJJ vs MJY", len(MJY_bins) - 1, MJY_bins, len(MJJ_bins) - 1, MJJ_bins) 
h_base_projx = h_base.ProjectionX("MassJY")
h_base_projy = h_base.ProjectionY("MassJJ")

x_edges = np.array(MJY_bins)
y_edges = np.array(MJJ_bins)
mode = args.mode
f_name=f"Templates/Templates_{mode}_Signal_all.root"
save_dir = f"plots/prefit_sig_{mode}"
#######################################################################################################################
#--------------------------rebinning  and creating projection hists--------------------------------------------------------------------------------
######################################################################################################################
h_BKGs_rebinned_merged = {}
h_BKGs_rebinned_projx_merged = {}
h_BKGs_rebinned_projy_merged = {}

for region in regions:
    h_BKGs_rebinned_merged[region] = {}
    h_BKGs_rebinned_projx_merged[region] = {}
    h_BKGs_rebinned_projy_merged[region] = {}
    for year in years:
        h_BKGs_rebinned_merged[region][year] = {}
        h_BKGs_rebinned_projx_merged[region][year] = {}
        h_BKGs_rebinned_projy_merged[region][year] = {}

f = ROOT.TFile.Open(f_name, "READ")
for key in f.GetListOfKeys():
    hist = key.ReadObj()
    if isinstance(hist, ROOT.TH2):
        hist_name = hist.GetName()
        if "nom" not in hist_name or "Allyears" in hist_name:
            continue
        print(hist_name)
        if "MC" in hist_name:
            for region in regions:
                if region in hist_name:
                    for year in years:
                        if (year + "_") in hist_name:
                            for process in processes:
                                if process in hist_name:
                                    h_BKGs_rebinned_merged[region][year][process] = rebin_TH2(hist, MJY_bins, MJJ_bins)
                                    h_BKGs_rebinned_projx_merged[region][year][process] = h_BKGs_rebinned_merged[region][year][process].ProjectionX(f"projx_MC_{process}_{year}_{region}")
                                    h_BKGs_rebinned_projy_merged[region][year][process] = h_BKGs_rebinned_merged[region][year][process].ProjectionY(f"projy_MC_{process}_{year}_{region}")
                                
        

################################################################################################################################
#-----------------------------------------making 2D plots-------------------------
########################################################################################################################


#########################################################################################################################################
#----------------------------------------making stack plots ------------------------------------------------------------------------------------
##############################################################################################################################
for region in regions:
    for year in years:
        print(region, year)
        bin_centers_projx = (np.array(MJY_bins)[:-1] + np.array(MJY_bins)[1:])/2
        bin_centers_projy = (np.array(MJJ_bins)[:-1] + np.array(MJJ_bins)[1:])/2
        

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={"height_ratios": [3, 1]}, sharex=True)
        

        if "MC_QCDJets" not in h_BKGs_rebinned_projx_merged[region][year]:
            h_BKGs_rebinned_projx_merged[region][year]["MC_QCDJets"] = h_BKGs_rebinned_projx_merged[region][year]["MC_TTBarJets"].Clone(f"QCD_x_{year}_{region}")
            h_BKGs_rebinned_projy_merged[region][year]["MC_QCDJets"] = h_BKGs_rebinned_projy_merged[region][year]["MC_TTBarJets"].Clone(f"QCD_y_{year}_{region}")
            h_BKGs_rebinned_projx_merged[region][year]["MC_QCDJets"].Reset()
            h_BKGs_rebinned_projy_merged[region][year]["MC_QCDJets"].Reset()
        mplhep.histplot(
            #[h_BKGs_rebinned_projx_merged[year]["MC_SingleTopJets"][region], h_BKGs_rebinned_projx_merged[year]["MC_DibosonJets"][region], h_BKGs_rebinned_projx_merged[year]["MC_HiggsJets"][region], h_BKGs_rebinned_projx_merged[region][year]["MC_TTBarJets"], h_BKGs_rebinned_projx_merged[year]["MC_WZJets"][region], h_BKGs_rebinned_projx_merged[region][year]["MC_QCDJets"]],
            #label = ["SingleTop", "Diboson", "Higgs", "TTBar", "WZ", "QCD"],
            #color = ["darkblue", "beige", "red", "lightblue", "green", "orange"],
            [h_BKGs_rebinned_projx_merged[region][year]["MC_TTBarJets"], h_BKGs_rebinned_projx_merged[region][year]["MC_QCDJets"]],
            label = ["TTBar", "QCD"],
            color = ["lightblue", "orange"],
            stack = True,
            histtype = "fill",
            ax = ax1,
        )
        mplhep.histplot(
            #[h_BKGs_rebinned_projx_merged[year]["MC_SingleTopJets"][region], h_BKGs_rebinned_projx_merged[year]["MC_DibosonJets"][region], h_BKGs_rebinned_projx_merged[year]["MC_HiggsJets"][region], h_BKGs_rebinned_projx_merged[region][year]["MC_TTBarJets"], h_BKGs_rebinned_projx_merged[year]["MC_WZJets"][region], h_BKGs_rebinned_projx_merged[region][year]["MC_QCDJets"]],
            [h_BKGs_rebinned_projx_merged[region][year]["MC_TTBarJets"],  h_BKGs_rebinned_projx_merged[region][year]["MC_QCDJets"]],
            stack = True,  # Note: keep stack=True so contours align with total stacks
            histtype = "step",
            color = "black",
            ax = ax1,
            linewidth = 1.2,
        )
        mplhep.cms.label("Preliminary", data = False, rlabel = r"7.9804 $fb^{-1}$, 2022(13.6 TeV)", ax = ax1)
        ax1.set_ylabel("Event Counts")
        ax1.set_xlabel("")
        ax1.legend()
        
        fig.tight_layout()
        ax1.set_yscale("linear")
        ax1.set_ylim(auto = True)
        fig.savefig(f"{save_dir}/linear_stack_projx_{year}_{region}.png")
        ax1.set_yscale("log")
        ax1.set_ylim(1,10000000)
        fig.savefig(f"{save_dir}/stack_projx_{year}_{region}.png")
        plt.close(fig)
    
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={"height_ratios": [3, 1]}, sharex=True)

        mplhep.histplot(
            #[h_BKGs_rebinned_projy_merged[year]["MC_SingleTopJets"][region], h_BKGs_rebinned_projy_merged[year]["MC_DibosonJets"][region], h_BKGs_rebinned_projy_merged[year]["MC_HiggsJets"][region], h_BKGs_rebinned_projy_merged[region][year]["MC_TTBarJets"], h_BKGs_rebinned_projy_merged[year]["MC_WZJets"][region], h_BKGs_rebinned_projy_merged[region][year]["MC_QCDJets"]],
            #label = ["SingleTop", "Diboson", "Higgs", "TTBar", "WZ", "QCD"],
            #color = ["darkblue", "beige", "red", "lightblue", "green", "orange"],
            [h_BKGs_rebinned_projy_merged[region][year]["MC_TTBarJets"], h_BKGs_rebinned_projy_merged[region][year]["MC_QCDJets"]],
            label = [ "TTBar",  "QCD"],
            color = [ "lightblue",  "orange"],
            stack = True,
            histtype = "fill",
            ax = ax1,
        )
        mplhep.histplot(
            #[h_BKGs_rebinned_projy_merged[year]["MC_SingleTopJets"][region], h_BKGs_rebinned_projy_merged[year]["MC_DibosonJets"][region], h_BKGs_rebinned_projy_merged[year]["MC_HiggsJets"][region], h_BKGs_rebinned_projy_merged[region][year]["MC_TTBarJets"], h_BKGs_rebinned_projy_merged[year]["MC_WZJets"][region], h_BKGs_rebinned_projy_merged[region][year]["MC_QCDJets"]],
            [h_BKGs_rebinned_projy_merged[region][year]["MC_TTBarJets"], h_BKGs_rebinned_projy_merged[region][year]["MC_QCDJets"]],
            stack = True,  # Note: keep stack=True so contours align with total stacks
            histtype = "step",
            color = "black",
            ax = ax1,
            linewidth = 1.2,
        )
        mplhep.cms.label("Preliminary", data = False, rlabel = r"7.9804 $fb^{-1}$, 2022(13.6 TeV)", ax = ax1)
        ax1.set_ylabel("Event Counts")
        ax1.set_xlabel("")
        ax1.legend()
        
        fig.tight_layout()
        ax1.set_yscale("linear")
        ax1.set_ylim(auto = True)
        fig.savefig(f"{save_dir}/linear_stack_projy_{year}_{region}.png")
        ax1.set_yscale("log")
        ax1.set_ylim(1,10000000)
        fig.savefig(f"{save_dir}/stack_projy_{year}_{region}.png")
        plt.close(fig)
        print("finished: ", region, year)
exit()
h_netQCD_rebinned_projx_merged_allyears_SR1 = h_base_projx.Clone("h_netQCD_rebinned_projx_merged_allyears_SR1")
h_netQCD_rebinned_projx_merged_allyears_SB1 = h_base_projx.Clone("h_netQCD_rebinned_projx_merged_allyears_SB1")
h_netQCD_rebinned_projy_merged_allyears_SR1 = h_base_projy.Clone("h_netQCD_rebinned_projy_merged_allyears_SR1")
h_netQCD_rebinned_projy_merged_allyears_SB1 = h_base_projy.Clone("h_netQCD_rebinned_projy_merged_allyears_SB1")
for year in years:
    h_netQCD_rebinned_projx_merged_allyears_SR1.Add(h_BKGs_rebinned_projx_merged["SR1"][year]["Net_QCDJets"])
    h_netQCD_rebinned_projx_merged_allyears_SB1.Add(h_BKGs_rebinned_projx_merged["SB1"][year]["Net_QCDJets"])
    h_netQCD_rebinned_projy_merged_allyears_SR1.Add(h_BKGs_rebinned_projy_merged["SR1"][year]["Net_QCDJets"])
    h_netQCD_rebinned_projy_merged_allyears_SB1.Add(h_BKGs_rebinned_projy_merged["SB1"][year]["Net_QCDJets"])
QCD_ratio_x_SR1_SB1 =  h_netQCD_rebinned_projx_merged_allyears_SR1.Clone("QCD_ratio_x") 
QCD_ratio_x_SR1_SB1.Divide(h_netQCD_rebinned_projx_merged_allyears_SB1) 
QCD_ratio_y_SR1_SB1 =  h_netQCD_rebinned_projy_merged_allyears_SR1.Clone("QCD_ratio_y") 
QCD_ratio_y_SR1_SB1.Divide(h_netQCD_rebinned_projy_merged_allyears_SB1) 

#QCD_ratio_x_SR1_SB1 =  h_netQCD_rebinned_projx_merged_allyears_SB1.Clone("QCD_ratio_x") 
#QCD_ratio_x_SR1_SB1.Divide(h_netQCD_rebinned_projx_merged_allyears_SR1) 
#QCD_ratio_y_SR1_SB1 =  h_netQCD_rebinned_projy_merged_allyears_SB1.Clone("QCD_ratio_y") 
#QCD_ratio_y_SR1_SB1.Divide(h_netQCD_rebinned_projy_merged_allyears_SR1) 
c = ROOT.TCanvas()
h_netQCD_rebinned_projx_merged_allyears_SR1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/NetQCD_SR1_x.png") 
c = ROOT.TCanvas()
h_netQCD_rebinned_projx_merged_allyears_SB1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/NetQCD_SB1_x.png") 
c = ROOT.TCanvas()
h_netQCD_rebinned_projy_merged_allyears_SR1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/NetQCD_SR1_y.png") 
c = ROOT.TCanvas()
h_netQCD_rebinned_projy_merged_allyears_SB1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/NetQCD_SB1_y.png") 

c = ROOT.TCanvas()

QCD_ratio_x_SR1_SB1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/NetQCD_ratio_SR1_SB1_x.png") 
c = ROOT.TCanvas()
QCD_ratio_y_SR1_SB1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/NetQCD_ratio_SR1_SB1_y.png") 
#exit()     



h_netQCD_rebinned_projx_merged_allyears_SR1 = h_base_projx.Clone("h_MCQCD_rebinned_projx_merged_allyears_SR1")
h_netQCD_rebinned_projx_merged_allyears_SB1 = h_base_projx.Clone("h_MCQCD_rebinned_projx_merged_allyears_SB1")
h_netQCD_rebinned_projy_merged_allyears_SR1 = h_base_projy.Clone("h_MCQCD_rebinned_projy_merged_allyears_SR1")
h_netQCD_rebinned_projy_merged_allyears_SB1 = h_base_projy.Clone("h_MCQCD_rebinned_projy_merged_allyears_SB1")
for year in years:
    h_netQCD_rebinned_projx_merged_allyears_SR1.Add(h_BKGs_rebinned_projx_merged["SR1"][year]["MC_QCDJets"])
    h_netQCD_rebinned_projx_merged_allyears_SB1.Add(h_BKGs_rebinned_projx_merged["SB1"][year]["MC_QCDJets"])
    h_netQCD_rebinned_projy_merged_allyears_SR1.Add(h_BKGs_rebinned_projy_merged["SR1"][year]["MC_QCDJets"])
    h_netQCD_rebinned_projy_merged_allyears_SB1.Add(h_BKGs_rebinned_projy_merged["SB1"][year]["MC_QCDJets"])
MCQCD_ratio_x_SR1_SB1 =  h_netQCD_rebinned_projx_merged_allyears_SR1.Clone("MCQCD_ratio_x") 
MCQCD_ratio_x_SR1_SB1.Divide(h_netQCD_rebinned_projx_merged_allyears_SB1) 
MCQCD_ratio_y_SR1_SB1 =  h_netQCD_rebinned_projy_merged_allyears_SR1.Clone("MCQCD_ratio_y") 
MCQCD_ratio_y_SR1_SB1.Divide(h_netQCD_rebinned_projy_merged_allyears_SB1) 

c = ROOT.TCanvas()
h_netQCD_rebinned_projx_merged_allyears_SR1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/MCQCD_SR1_x.png") 
c = ROOT.TCanvas()
h_netQCD_rebinned_projx_merged_allyears_SB1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/MCQCD_SB1_x.png") 
c = ROOT.TCanvas()
h_netQCD_rebinned_projy_merged_allyears_SR1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/MCQCD_SR1_y.png") 
c = ROOT.TCanvas()
h_netQCD_rebinned_projy_merged_allyears_SB1.Draw("E")  
c.Update()
c.SaveAs(f"{save_dir}/MCQCD_SB1_y.png") 
c = ROOT.TCanvas()
MCQCD_ratio_x_SR1_SB1.SetMarkerColor(ROOT.kRed)
MCQCD_ratio_x_SR1_SB1.SetLineColor(ROOT.kRed)
MCQCD_ratio_x_SR1_SB1.Draw("E")  
QCD_ratio_x_SR1_SB1.Draw("ESAME")  
c.Update()
c.SaveAs(f"{save_dir}/MCQCD_ratio_SR1_SB1_x.png") 
c = ROOT.TCanvas()
MCQCD_ratio_y_SR1_SB1.SetMarkerColor(ROOT.kRed)
MCQCD_ratio_y_SR1_SB1.SetLineColor(ROOT.kRed)
MCQCD_ratio_y_SR1_SB1.Draw("E")  
QCD_ratio_y_SR1_SB1.Draw("ESAME")  
c.Update()
c.SaveAs(f"{save_dir}/MCQCD_ratio_SR1_SB1_y.png") 
exit()     



















##########################################################################################################################
#--------------------------------------fitting R_p/f------------------------------------------------------------------------
###################################################################################################################

h_netQCD_VS4_MJY_all = h_base_projx.Clone("h_netQCD_VS4_MJY_all")
h_netQCD_VB2_MJY_all = h_base_projx.Clone("h_netQCD_VB2_MJY_all")
for year in years:
    h_netQCD_VS4_MJY =  h_data_rebinned_projx["VS4"][year].Clone(f"h_netQCD_VS4_MJY_{year}") 
    h_netQCD_VS4_MJY.Add(h_BKGs_rebinned_projx_merged[year]["MC_TTBarJets"]["VS4"], -1)
    h_netQCD_VB2_MJY =  h_data_rebinned_projx["VB2"][year].Clone(f"h_netQCD_VB2_MJY_{year}") 
    h_netQCD_VB2_MJY.Add(h_BKGs_rebinned_projx_merged[year]["MC_TTBarJets"]["VB2"], -1)
    h_netQCD_VS4_MJY_all.Add(h_netQCD_VS4_MJY)
    h_netQCD_VB2_MJY_all.Add(h_netQCD_VB2_MJY)
    h_ratio_VS4_VB2 = h_netQCD_VS4_MJY.Clone(f"h_ratio_VS4_VB2_{year}")
    h_ratio_VS4_VB2.Devide(h_netQCD_VB2_MJY)
    h_ratio_VS4_VB2.SetTitle(h_ratio_VS4_VB2.GetName())
    c = ROOT.TCanvas()
    fit_func = ROOT.TF1("fit_func", "pol2", 0, 1000)
    fit_result = h_ratio_VS4_VB2.Fit(fit_func, "S")
    h_ratio_VS4_VB2.Draw("E")   
    fit_func.SetLineColor(ROOT.kRed)
    fit_func.Draw("SAME")
    c.Update()
    c.SaveAs(f"plots/VS4_VB2_fit/fitted_{year}_{h.GetName()}.png")

h_ratio_VS4_VB2 = h_netQCD_VS4_MJY_all.Clone("h_ratio_VS4_VB2_all")
h_ratio_VS4_VB2.Devide(h_netQCD_VB2_MJY_all)
h_ratio_VS4_VB2.SetTitle(h_ratio_VS4_VB2_all.GetName())
c = ROOT.TCanvas()
fit_func = ROOT.TF1("fit_func", "pol2", 0, 1000)
fit_result = h_ratio_VS4_VB2.Fit(fit_func, "S")
h_ratio_VS4_VB2.Draw("E")
fit_func.SetLineColor(ROOT.kRed)
fit_func.Draw("SAME")
c.Update()
c.SaveAs(f"plots/VS4_VB2_fit/fitted_all_{h.GetName()}.png")
