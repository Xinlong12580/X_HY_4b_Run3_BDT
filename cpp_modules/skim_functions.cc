using namespace ROOT::VecOps;

// 1p1 mode
int skimmingTwoAK8Jets(int nFatJet, RVec<float> FatJet_pt, RVec<float> FatJet_eta, RVec<float> FatJet_msoftdrop, RVec<float> FatJet_regressedMass){
    if(nFatJet<2){
        return 0;
    }
    int pt_cut = FatJet_pt.at(0)>300 && FatJet_pt.at(1)>300;
    int eta_cut = TMath::Abs(FatJet_eta.at(0))<2.5 && TMath::Abs(FatJet_eta.at(1))<2.5;
    int mSD_cut = (FatJet_msoftdrop.at(0)>30 && FatJet_regressedMass.at(1)>60) || (FatJet_msoftdrop.at(1)>30 && FatJet_regressedMass.at(0)>60);
    
    if(pt_cut && eta_cut && mSD_cut){
        return 1;
    }
    else{
        return 0;
    }
}

// 2p1 mode.
int skimmingAK8JetwithTwoAK4Jets(int nFatJet, RVec<float> FatJet_pt, RVec<float> FatJet_eta, RVec<float> FatJet_m, int nJet, RVec<float> Jet_pt, RVec<float> Jet_eta){
    if(nFatJet < 1 || nJet < 2){
        return 0;
    }
    int pass = 0;
    for (int i = 0; i < nFatJet; i++){
        if (FatJet_pt.at(i) > 250 && FatJet_m.at(i) > 60 && FatJet_eta.at(i) < 2.5){
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
    return pass;
/*
    int pt_cut = FatJet_pt.at(0)>300 && Jet_pt.at(0)>50;
    
    if(pt_cut){
        return 1;
    }
    else{
        return 0;
    }
*/
}

//skimming
int skimFlag(int nFatJet, RVec<float> FatJet_pt, RVec<float> FatJet_eta, RVec<float> FatJet_msoftdrop, RVec<float> FatJet_regressedMass, int nJet, RVec<float> Jet_pt, RVec<float> Jet_eta){
    Int_t jetSkim1  = skimmingTwoAK8Jets(nFatJet,FatJet_pt,FatJet_eta,FatJet_msoftdrop, FatJet_regressedMass);
    Int_t jetSkim2  = skimmingAK8JetwithTwoAK4Jets(nFatJet,FatJet_pt,FatJet_eta,FatJet_regressedMass, nJet, Jet_pt, Jet_eta);
    Int_t skimScore  = jetSkim1+2*jetSkim2;
    return skimScore;
}
RVec<float> makeRegressedMass(int nFatJet, RVec<float> FatJet_mass, RVec<float> FatJet_particleNet_massCorr){ 
    ROOT::VecOps::RVec<Float_t> RegMass = {};
    for (int i = 0; i < nFatJet; i ++){
        RegMass.push_back(FatJet_mass.at(i) * FatJet_particleNet_massCorr.at(i));
    }
    return RegMass;
}
