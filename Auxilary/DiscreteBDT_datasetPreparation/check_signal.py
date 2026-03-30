import ROOT
f = ROOT.RDataFrame("Events", "datasets/RegSig_nom_1p1_tagged_selected_SKIM_skimmed_2024__SignalMC_XHY4b__MX-3000_MY-300_1p1_ALL.root")
print(f.Filter("Delta_Y > 1.3").Count().GetValue()/f.Count().GetValue())
print(f.Filter("Tagger_H_discrete >= 1 && Tagger_Y_discrete >= 1").Count().GetValue()/f.Count().GetValue())
print(f.Filter("Tagger_H >= 0.8 && Tagger_Y > 0.8").Count().GetValue()/f.Count().GetValue())
