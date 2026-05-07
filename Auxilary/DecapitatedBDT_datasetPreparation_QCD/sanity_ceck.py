import ROOT
years = ["2022", "2022EE", "2023", "2023BPix", "2024"]
lumi_dict = {
    "2022": 7980.454151,
    "2022EE": 26671.609707000002,
    "2023": 18062.659110999995,
    "2023BPix": 9693.130053000003,
    "2024": 109987.998903 
}
for year in years:
    rdf = ROOT.RDataFrame("Events", f"datasets/BKGs_RegSig_1p1_{year}_ALL.root")
    weight = rdf.Sum("BDT_weight").GetValue()
    print(year, weight)
print(lumi_dict)
