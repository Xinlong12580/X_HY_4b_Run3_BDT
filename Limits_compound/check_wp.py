import ROOT

f = ROOT.TFile.Open("Control_MX-4000_MY-2000_workspace/base.root", "READ")

w = f.Get("w")
data = w.data("data_obs_SB1_Region0")
#w.Print()
data.Print()
print(data.get().first().getBins()) 
print(data.numEntries()) 
