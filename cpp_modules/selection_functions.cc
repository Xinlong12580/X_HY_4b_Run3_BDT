#include "TIMBER/Framework/include/common.h"
#include "cpp_modules/share.h"

//Calculating DeltaR of two points
float DeltaR(RVec<float> Etas, RVec<float> Phies){
    float deltaEta = std::abs(Etas[0] - Etas[1]);
    float deltaPhi = std::abs(Phies[0]-Phies[1]) < M_PI ? std::abs(Phies[0] - Phies[1]) : 2*M_PI - std::abs(Phies[0] - Phies[1]);
    float deltaR=sqrt(deltaEta * deltaEta + deltaPhi * deltaPhi);
    return deltaR;
}

//Calculating DeltaR of each object in a collection with respect to a given point
RVec<float> DeltaR(RVec<float> Etas, RVec<float> Phies, float eta, float phi){
    if (Etas.size() != Phies.size())
        throw std::runtime_error("Eta vector and Phi vector should be of the same size");
    RVec<float> Delta_Rs = {};
    for (int i = 0; i < Etas.size(); i++){
        float deltaR = DeltaR({Etas.at(i), eta}, {Phies.at(i), phi});
        //std::cout<<deltaR<<std::endl;
        Delta_Rs.push_back(deltaR);
    }
    return Delta_Rs;
}

//2p1 mode only. Looking for two Y Jets satifying DeltaR and B score requirement
RVec<int> FindIdxJY(RVec<float> Etas, RVec<float> Phies, float eta, float phi, RVec<float> BScores, float deltaR,  RVec<bool> Goodnesses){
    RVec<int> IdxJYs = {-1, -1};
    int count = 0;
    float max1 = -100.;
    float max2 = -100.;
    RVec<float> DeltaR_HJ = DeltaR(Etas, Phies, eta, phi);
    for (int i = 0; i < DeltaR_HJ.size(); i++)
    {
        if (DeltaR_HJ.at(i) <= deltaR || (! Goodnesses.at(i)) )
            continue;
        if(BScores.at(i) > max1)
        {
            max2 = max1;
            max1 = BScores.at(i);
            IdxJYs.at(1) = IdxJYs.at(0);
            IdxJYs.at(0) = i;
        }
        else if (BScores.at(i) <= max1 && BScores.at(i) > max2)
        {
            max2 = BScores.at(i);
            IdxJYs.at(1) = i;
        } 

    }
    return IdxJYs; 
}

//2p1 mode only. Looking for two Y Jets satifying DeltaR and B score requirement
RVec<int> FindIdxJY(RVec<float> Etas, RVec<float> Phies, float eta, float phi, RVec<int> BScores, float deltaR,  RVec<bool> Goodnesses){
    RVec<int> IdxJYs = {-1, -1};
    int count = 0;
    int max1 = -100;
    int max2 = -100;
    RVec<float> DeltaR_HJ = DeltaR(Etas, Phies, eta, phi);
    for (int i = 0; i < DeltaR_HJ.size(); i++)
    {
        if (DeltaR_HJ.at(i) <= deltaR || (! Goodnesses.at(i)) )
            continue;
        if(BScores.at(i) > max1)
        {
            max2 = max1;
            max1 = BScores.at(i);
            IdxJYs.at(1) = IdxJYs.at(0);
            IdxJYs.at(0) = i;
        }
        else if (BScores.at(i) <= max1 && BScores.at(i) > max2)
        {
            max2 = BScores.at(i);
            IdxJYs.at(1) = i;
        } 

    }
    return IdxJYs; 
}


RVec<int> FindIdxJY_bscore_limits(RVec<float> Etas, RVec<float> Phies, float eta, float phi, RVec<float> BScores, float deltaR, float minBScore, float maxBScore, RVec<bool> Goodnesses){
    RVec<int> IdxJYs = {-1, -1};
    int count = 0;
    RVec<float> DeltaR_HJ = DeltaR(Etas, Phies, eta, phi);
    for (int i = 0; i < DeltaR_HJ.size(); i++)
    {
        if (DeltaR_HJ.at(i) > deltaR && BScores.at(i) >= minBScore && BScores.at(i) < maxBScore && Goodnesses.at(i) )
        {
            IdxJYs.at(count) = i;
            count ++;
            if (count == 2)
                break;
        }
    }
    return IdxJYs; 
}
// 2p1 mode only. Looking for Higgs Jet from the first nmass FatJets, with mass requirement only
Int_t FindIdxJH(RVec<float> Masses, float minM, float maxM, RVec<bool> Goodnesses, float HiggsM = 125){
    int ind_best = 0;
    float diff_mass_best = 10000;
    // Looking for best match
    for (int i = 0; i < Masses.size(); i++)
    {
        if (Goodnesses.at(i) && (abs(Masses[i] - HiggsM) < diff_mass_best) ) {
            ind_best = i;
            diff_mass_best = abs(Masses[i] - HiggsM);
        }
    }
    //return best match
    float mass_best = Masses[ind_best];
    if (mass_best < maxM && mass_best > minM)
        return ind_best;
    else
	    return -1;
}



Int_t FindIdxJH_random(RVec<float> Masses, float minM, float maxM, int nMass, RVec<bool> Goodnesses){
    //Looking for all possible FatJets
    RVec<int> validIdxs = {};
    int n_goodjet = 0;
    for (int i = 0; i < Masses.size(); i++)
    {
        if(Goodnesses.at(i)){
            n_goodjet ++;
            if (Masses.at(i) >= minM && Masses.at(i) <= maxM)
                validIdxs.push_back(i);
        }
        if (n_goodjet >= nMass) 
            break;
    }
    //If there are more than one such FatJet, choose one randomly
    if (validIdxs.size() >= 1){
        std::random_device rd;                 
        std::mt19937 gen(rd());                
        std::uniform_int_distribution<> dist(0, validIdxs.size() - 1);  

        return validIdxs.at(dist(gen));
	}
    //if no FatJet found, return -1
	return -1;
}

Int_t FindIdxJY(RVec<bool> Goodnesses, int IdxJH){
    for (int i = 0; i < Goodnesses.size(); i++)
        if (Goodnesses.at(i) && i != IdxJH )
            return i;
    return -1;
}




RVec<bool> goodJet(int nJet, RVec<int> Jet_jetId, int jetId_min, RVec<float> Jet_pt, float pt_min, RVec<float> Jet_eta, float absEta_max){
    RVec<bool> IsGood = {};
    for (int i = 0; i < nJet; i ++){
        if (Jet_jetId.at(i) >= jetId_min && Jet_pt.at(i) >= pt_min && std::abs(Jet_eta.at(i)) <= absEta_max )
            IsGood.push_back(true);
        else
             IsGood.push_back(false);
    }
    return IsGood;
}



RVec<bool> goodJet_withMass(int nJet, RVec<int> Jet_jetId, int jetId_min, RVec<float> Jet_pt, float pt_min, RVec<float> Jet_mass0, float mass0_min, RVec<float> Jet_mass1, float mass1_min, RVec<float> Jet_eta, float absEta_max){
    RVec<bool> IsGood = {};
    for (int i = 0; i < nJet; i ++){
        if (Jet_jetId.at(i) >= jetId_min && Jet_pt.at(i) >= pt_min && (Jet_mass0.at(i) >= mass0_min || Jet_mass1.at(i) >= mass1_min) && std::abs(Jet_eta.at(i)) <= absEta_max )
            IsGood.push_back(true);
        else
             IsGood.push_back(false);
    }
    return IsGood;
}















//Calculate Inv mass for a list of variables
Float_t InvMass_PtEtaPhiM(ROOT::VecOps::RVec<Float_t> Pts, ROOT::VecOps::RVec<Float_t> Etas,  ROOT::VecOps::RVec<Float_t> Phis, ROOT::VecOps::RVec<Float_t> Masss)
{
	Float_t inv_mass = SHARE::InvalidF;
	RVec<ROOT::Math::PtEtaPhiMVector> Vectors = {};
	
	for(Int_t i = 0; i < Pts.size(); i++)
	{
		//If one value in the list is invalid, return invalid inv mass
		if(Pts.at(i) < (SHARE::InvalidF + 10) ||  Etas.at(i) < (SHARE::InvalidF + 10) || Phis.at(i) < (SHARE::InvalidF + 10) || Masss.at(i) < (SHARE::InvalidF + 10))
		{
			inv_mass = SHARE::InvalidF;
			return inv_mass;
		}
		
		ROOT::Math::PtEtaPhiMVector vector(Pts.at(i), Etas.at(i), Phis.at(i), Masss.at(i));
		Vectors.push_back(vector);
	}
	inv_mass = hardware::InvariantMass(Vectors);
	return inv_mass;
}

float Rapidity(float pt, float eta, float phi, float mass){
    ROOT::Math::PtEtaPhiMVector vector(pt, eta, phi, mass);
    return vector.Rapidity();
}

float DeltaRapidity(float pt_0, float eta_0, float phi_0, float mass_0, float pt_1, float eta_1, float phi_1, float mass_1){
    float Y_0 = Rapidity(pt_0, eta_0, phi_0, mass_0);
    float Y_1 = Rapidity(pt_1, eta_1, phi_1, mass_1);
    return (Y_0 - Y_1);
}

ROOT::VecOps::RVec<Float_t> makeTXbb(int nFatJet, ROOT::VecOps::RVec<Float_t> FatJet_Xbb, ROOT::VecOps::RVec<Float_t> FatJet_QCD){
    ROOT::VecOps::RVec<Float_t> TXbb = {};
    for (int i = 0; i < nFatJet; i ++){
        TXbb.push_back(FatJet_Xbb.at(i) / (FatJet_Xbb.at(i) + FatJet_QCD.at(i)));
    }
    return TXbb;
}
template <class _type>
bool debugger(_type input, std::string extra = ""){
    std::cout<<extra<<" DEBUGGER: "<<input<<std::endl;
    return 0;
}
