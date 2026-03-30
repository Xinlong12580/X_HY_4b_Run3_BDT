import ROOT

rdf_data = ROOT.RDataFrame("Events", "datasets/Data_RegCon_2p1_ALL.root")
rdf_bkg = ROOT.RDataFrame("Events", "datasets/BKGs_RegCon_2p1_ALL.root")
rdf_data = ROOT.RDataFrame("Events", "datasets/Data_2p1_ALL.root")
rdf_bkg = ROOT.RDataFrame("Events", "datasets/BKGs_2p1_ALL.root")

print(rdf_data.Sum("BDT_weight").GetValue())
print(rdf_bkg.Filter("sample_ID == 1").Sum("BDT_weight").GetValue())
print(rdf_bkg.Filter("sample_ID == 2").Sum("BDT_weight").GetValue())
print((rdf_data.Sum("BDT_weight").GetValue() - rdf_bkg.Filter("sample_ID == 1").Sum("BDT_weight").GetValue())/rdf_bkg.Filter("sample_ID == 2").Sum("BDT_weight").GetValue() )
