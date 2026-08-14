import ROOT
import os

from argparse import ArgumentParser
f_nom = ROOT.TFile.Open("SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/base_SR_1p1.root", "READ")
w = f_nom.Get("w")
data_list = w.allData()
for data in w.allData():
    if isinstance(data, ROOT.RooDataHist):
        #print("Found RooDataHist:", data.GetName())
        #if data.GetName() == "Allyears__MC_TTBarJets_CR_SB1_1p1_Region0_MCstat_CR_SB1_1p1_11_16Up":
        #if data.GetName() == "Allyears__SignalMC_XHY4b_MX-3000_MY-300_CR_SB1_1p1_Region0_Y2022EE_JES_Down":
        #if data.GetName() == "Allyears__MC_TTBarJets_CR_SB1_1p1_Region0_MCstat_CR_SR1_1P1_5_3Down":
        if data.GetName() == "Allyears__SignalMC_XHY4b_MX-3500_MY-200_SR_SR1_1p1_Region0":
            data.Print()
            dh = data
            obs = dh.get()  # RooArgSet

            # Total number of bins
            n = dh.numEntries()

            for i in range(n):
                # Load the i-th bin
                dh.get(i)

                # Get coordinates (values of observables)
                coords = {var.GetName(): var.getVal() for var in obs}

                # Get bin content (weight)
                weight = dh.weight()

                print(f"Bin {i}: {coords}, weight = {weight:.8f}")
