import ROOT
region = "RegCon"
years = ["2022", "2022EE", "2023", "2023BPix"]
for year in years:
    rdf_sig0_sumw = ROOT.RDataFrame("Runs", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_hv0/division_2p1_SELECTION_2P1_BDT_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_{year}__SignalMC_XHY4b__MX-4000_MY-2000_n-10000_i-0.root").Sum("genEventSumw").GetValue()
    rdf_sig0 = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_hv0/division_2p1_SELECTION_2P1_BDT_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_{year}__SignalMC_XHY4b__MX-4000_MY-2000_n-10000_i-0.root").Define("BDT_weight", f"weight_All__nominal/ {rdf_sig0_sumw}")
    rdf_sig1_sumw = ROOT.RDataFrame("Runs", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_noDDT/division_2p1_SELECTION_2P1_BDT_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_{year}__SignalMC_XHY4b__MX-4000_MY-2000_n-10000_i-0.root").Sum("genEventSumw").GetValue()
    rdf_sig1 = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_noDDT/division_2p1_SELECTION_2P1_BDT_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_{year}__SignalMC_XHY4b__MX-4000_MY-2000_n-10000_i-0.root").Define("BDT_weight", f"weight_All__nominal/ {rdf_sig1_sumw}")

    print(year, rdf_sig0.Filter("Region_SR1").Sum("BDT_weight").GetValue(), rdf_sig0.Filter("Region_SB1").Sum("BDT_weight").GetValue())
    print(year, rdf_sig1.Filter("Region_SR1").Sum("BDT_weight").GetValue(), rdf_sig1.Filter("Region_SB1").Sum("BDT_weight").GetValue())
    rdf_sig0.Snapshot("Events", f"check/Sig0_{year}.root")
    rdf_sig1.Snapshot("Events", f"check/Sig1_{year}.root")
    #rdf_sig0_sumw = ROOT.RDataFrame("Runs", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_hv0/division_2p1_SELECTION_2P1_BDT_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_{year}__MC_TTBarJets__TTto4Q_n-10000_i-0.root").Sum("genEventSumw").GetValue()
    #rdf_sig0 = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_hv0/division_2p1_SELECTION_2P1_BDT_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_{year}__MC_TTBarJets__TTto4Q_n-10000_i-0.root").Define("BDT_weight", f"weight_All__nominal/ {rdf_sig0_sumw}")
    #rdf_sig1_sumw = ROOT.RDataFrame("Runs", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_noDDT/division_2p1_SELECTION_2P1_BDT_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_{year}__MC_TTBarJets__TTto4Q_n-10000_i-0.root").Sum("genEventSumw").GetValue()
    #rdf_sig1 = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_noDDT/division_2p1_SELECTION_2P1_BDT_RegSig_nom_tagged_selected_2p1_SKIM_skimmed_{year}__MC_TTBarJets__TTto4Q_n-10000_i-0.root").Define("BDT_weight", f"weight_All__nominal/ {rdf_sig1_sumw}")

    rdf_sig0_sumw = ROOT.RDataFrame("Runs", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_hv0/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_skimmed_{year}__MC_TTBarJets__TTto4Q_n-10000_i-0.root").Sum("genEventSumw").GetValue()
    rdf_sig0 = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_hv0/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_skimmed_{year}__MC_TTBarJets__TTto4Q_n-10000_i-0.root").Define("BDT_weight", f"weight_All__nominal/ {rdf_sig0_sumw}")
    rdf_sig1_sumw = ROOT.RDataFrame("Runs", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_noDDT/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_skimmed_{year}__MC_TTBarJets__TTto4Q_n-10000_i-0.root").Sum("genEventSumw").GetValue()
    rdf_sig1 = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_noDDT/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_skimmed_{year}__MC_TTBarJets__TTto4Q_n-10000_i-0.root").Define("BDT_weight", f"weight_All__nominal/ {rdf_sig1_sumw}")

    print(year, rdf_sig0.Filter("Region_SR1").Sum("BDT_weight").GetValue(), rdf_sig0.Filter("Region_SB1").Sum("BDT_weight").GetValue())
    print(year, rdf_sig1.Filter("Region_SR1").Sum("BDT_weight").GetValue(), rdf_sig1.Filter("Region_SB1").Sum("BDT_weight").GetValue())

    rdf_sig0.Snapshot("Events", f"check/TT0_{year}.root")
    rdf_sig1.Snapshot("Events", f"check/TT1_{year}.root")
    
    rdf_sig0E_sumw = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_hv0/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_masked_skimmed_2022EE__Data__JetMET__Run2022E-22Sep2023-v1__NANOAOD_n-10000_i-0.root").Filter("Region_SR1").Sum("weight_All__nominal").GetValue()
    rdf_sig0F_sumw = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_hv0/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_masked_skimmed_2022EE__Data__JetMET__Run2022F-22Sep2023-v2__NANOAOD_n-10000_i-0.root").Filter("Region_SR1").Sum("weight_All__nominal").GetValue()
    rdf_sig0G_sumw = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_hv0/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_masked_skimmed_2022EE__Data__JetMET__Run2022G-22Sep2023-v2__NANOAOD_n-10000_i-0.root").Filter("Region_SR1").Sum("weight_All__nominal").GetValue()
    print(rdf_sig0E_sumw + rdf_sig0F_sumw + rdf_sig0G_sumw - rdf_sig0.Filter("Region_SR1").Sum("BDT_weight").GetValue())
    rdf_sig1E_sumw = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_noDDT/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_masked_skimmed_2022EE__Data__JetMET__Run2022E-22Sep2023-v1__NANOAOD_n-10000_i-0.root").Filter("Region_SR1").Sum("weight_All__nominal").GetValue()
    rdf_sig1F_sumw = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_noDDT/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_masked_skimmed_2022EE__Data__JetMET__Run2022F-22Sep2023-v2__NANOAOD_n-10000_i-0.root").Filter("Region_SR1").Sum("weight_All__nominal").GetValue()
    rdf_sig1G_sumw = ROOT.RDataFrame("Events", f"root://cmseos.fnal.gov//store/user/xinlong/XHY4bRun3_division_2p1_BDT_noDDT/division_2p1_SELECTION_2P1_BDT_RegCon_nom_tagged_selected_2p1_SKIM_masked_skimmed_2022EE__Data__JetMET__Run2022G-22Sep2023-v2__NANOAOD_n-10000_i-0.root").Filter("Region_SR1").Sum("weight_All__nominal").GetValue()
    print(rdf_sig1E_sumw + rdf_sig1F_sumw + rdf_sig1G_sumw - rdf_sig1.Filter("Region_SR1").Sum("BDT_weight").GetValue())
