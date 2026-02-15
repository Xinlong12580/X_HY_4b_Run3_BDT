import ROOT

f_name = "Templates/Templates_2p1_Signal_all.root"
#f_name = "Templates/Templates_2p1_Control_all.root"

f = ROOT.TFile.Open(f_name, "READ")
for year in ["2022", "2022EE", "2023", "2023BPix", "2024"]:
    #h = f.Get(f"{year}__SignalMC_XHY4b_MX-4000_MY-2000__SB1_2p1__nominal")
    h = f.Get(f"{year}__MC_TTBarJets__SB1_2p1__nominal")
    #h = f.Get(f"{year}__JetMET__SB1_2p1__nominal")
    h.Print()
exit()
for key in f.GetListOfKeys():
    h = key.ReadObj()
    if "2022EE" in h.GetName() and "SR2" in h.GetName() and "JetMET" not in h.GetName() and "All" not in h.GetName():
        h.Print()
    del h
