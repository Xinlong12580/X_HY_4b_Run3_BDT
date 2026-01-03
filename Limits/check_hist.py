import ROOT

f_name = "Templates/Templates_1p1_all.root"
f = ROOT.TFile.Open(f_name, "READ")
for key in f.GetListOfKeys():
    h = key.ReadObj()
    if "2022EE" in h.GetName() and "SR2" in h.GetName() and "JetMET" not in h.GetName() and "All" not in h.GetName():
        h.Print()
    del h
