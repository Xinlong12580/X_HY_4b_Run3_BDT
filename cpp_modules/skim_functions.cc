using namespace ROOT::VecOps;

// 1p1 mode
int skimmingTwoAK8Jets(int nFatJet, RVec<float> FatJet_pt, RVec<float> FatJet_eta, RVec<float> FatJet_msoftdrop, RVec<float> FatJet_regressedMass){
    if(nFatJet<2){
        return 0;
    }
    std::vector<int> col_Higgs = {};
    std::vector<int> col_Y = {};
    for(int i = 0; i < nFatJet; i ++){
        bool pt_cut = FatJet_pt.at(i)>300;
        bool eta_cut = TMath::Abs(FatJet_eta.at(i))<2.5;
        bool mSD_cut = (FatJet_msoftdrop.at(i)>30);
        bool mreg_cut = (FatJet_regressedMass.at(i)>50);
        if(pt_cut && eta_cut && mreg_cut)
            col_Higgs.push_back(i);
        if(pt_cut && eta_cut && mSD_cut)
            col_Y.push_back(i);
    }
    if (col_Higgs.size() == 0 || col_Y.size() == 0 )
        return 0;
    if (col_Higgs.size() == 1 && col_Y.size() == 1 && col_Higgs.at(0) == col_Y.at(0) )
        return 0;
    //Looks GOOD
    return 1;
    
}

// 2p1 mode.
int skimmingAK8JetwithTwoAK4Jets(int nFatJet, RVec<float> FatJet_pt, RVec<float> FatJet_eta, RVec<float> FatJet_m, int nJet, RVec<float> Jet_pt, RVec<float> Jet_eta){
    if(nFatJet < 1 || nJet < 2){
        return 0;
    }
    int pass = 0;
    for (int i = 0; i < nFatJet; i++){
        if (FatJet_pt.at(i) > 250 && FatJet_m.at(i) > 50 && FatJet_eta.at(i) < 2.5){
            pass = 1;
            break;
        }
    }
    if (pass == 1) {
        pass = 0;
        int count = 0;
        for (int i = 0; i < nJet; i++){
            if (Jet_pt.at(i) > 40 && Jet_eta.at(i) < 2.5){
                count ++;
            }
            if (count == 2){
                pass = 1;
                break;
            }
        }
    }
    //LOOKS GOOD
    return pass;
}

//skimming
int skimFlag(int nFatJet, RVec<float> FatJet_pt, RVec<float> FatJet_eta, RVec<float> FatJet_msoftdrop, RVec<float> FatJet_regressedMass, int nJet, RVec<float> Jet_pt, RVec<float> Jet_eta){
    Int_t jetSkim1  = skimmingTwoAK8Jets(nFatJet,FatJet_pt,FatJet_eta,FatJet_msoftdrop, FatJet_regressedMass);
    Int_t jetSkim2  = skimmingAK8JetwithTwoAK4Jets(nFatJet,FatJet_pt,FatJet_eta,FatJet_regressedMass, nJet, Jet_pt, Jet_eta);
    Int_t skimScore  = jetSkim1+2*jetSkim2;
    //LOOKS GOOD
    return skimScore;
}
RVec<float> makeRegressedMass(int nFatJet, RVec<float> FatJet_mass, RVec<float> FatJet_massCorr){ 
    ROOT::VecOps::RVec<Float_t> RegMass = {};
    for (int i = 0; i < nFatJet; i ++){
        RegMass.push_back(FatJet_mass.at(i) * FatJet_massCorr.at(i));
    }
    //LOOKS GOOD
    return RegMass;
}
RVec<float> getRawVal(int nJet, RVec<float> val, RVec<float> rawFactor){
    ROOT::VecOps::RVec<Float_t> rawVal = {};
    for (int i = 0; i < nJet; i ++){
        rawVal.push_back( val.at(i) * (1 - rawFactor.at(i) ) );
    }
    return rawVal;
}
