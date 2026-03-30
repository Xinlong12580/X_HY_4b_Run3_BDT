import ROOT

rdf0 = ROOT.RDataFrame("Events", "DDT_2p1_tilt/DDT_BDT_discrete_BKGs_2p1_ALL.root")
rdf1 = ROOT.RDataFrame("Events", "DDT_2p1/DDT_BDT_discrete_BKGs_2p1_ALL.root")
rdf0 = ROOT.RDataFrame("Events", "DDT_2p1_tilt/DDT_BDT_discrete_reweighted_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_2022EE__SignalMC_XHY4b__MX-4000_MY-2000_2p1_ALL.root")
rdf1 = ROOT.RDataFrame("Events", "DDT_2p1/DDT_BDT_discrete_reweighted_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_2022EE__SignalMC_XHY4b__MX-4000_MY-2000_2p1_ALL.root")
print(rdf0.Filter("Region_SR1").Filter("sample_ID == 0").Sum("BDT_weight").GetValue())
print(rdf1.Filter("Region_SR1").Filter("sample_ID == 0").Sum("BDT_weight").GetValue())
