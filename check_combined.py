import ROOT 
f_combined = "RegSig_JER__down_combined_tagged_selected_SKIM_skimmed_2024__MC_TTBarJets__TTtoLNu2Q_n-1_i-393.root"
f_1p1 = "RegSig_JER__down_1p1_tagged_selected_SKIM_skimmed_2024__MC_TTBarJets__TTtoLNu2Q_n-1_i-393.root"
f_2p1 = "RegSig_JER__down_2p1_tagged_selected_SKIM_skimmed_2024__MC_TTBarJets__TTtoLNu2Q_n-1_i-393.root" 
rdf_1p1 = ROOT.RDataFrame("Events", f_1p1)
rdf_2p1 = ROOT.RDataFrame("Events", f_2p1)
rdf_combined = ROOT.RDataFrame("Events", f_combined)

print(rdf_combined.Count().GetValue())
print(rdf_combined.Filter("flag1p1").Count().GetValue())
print(rdf_combined.Filter("flag2p1").Count().GetValue())
print(rdf_1p1.Count().GetValue())
print(rdf_2p1.Count().GetValue())
