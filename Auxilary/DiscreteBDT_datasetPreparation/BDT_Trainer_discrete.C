#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
 
#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"
 
#include "TMVA/Factory.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"

int BDT_Trainer_discrete(std::string mode, std::string year, std::string MX, std::string MY ){

    TMVA::Tools::Instance();
    TString BKG_fname = "datasets/BKGs_RegSig_" + mode + "_" + year + "_ALL.root";
    TString Signal_fname = "datasets/reweighted_RegSig_nom_" + mode + "_tagged_selected_SKIM_skimmed_"+ year +"__SignalMC_XHY4b__MX-" + MX + "_MY-" + MY + "_" + mode + "_ALL.root";
    std::cout<<"Running BDT on file "<<BKG_fname<< " and "<<Signal_fname<<std::endl;
    std::unique_ptr<TFile> BKG_file{TFile::Open(BKG_fname)};
    std::unique_ptr<TFile> Signal_file{TFile::Open(Signal_fname)};
    TTree *signalTree     = (TTree*)Signal_file->Get("Events");
    TTree *background     = (TTree*)BKG_file->Get("Events");
    int nSig = signalTree->GetEntries();
    int nBKG = background->GetEntries();
    std::cout<<"Total signal events: "<<signalTree->GetEntries()<<std::endl<<"Total signal events: "<<background->GetEntries()<<std::endl;
    TString outfileName("TMVAC_" + mode + "_" + year + "_discrete.root");
    std::unique_ptr<TFile> outputFile{TFile::Open(outfileName, "RECREATE")};
    auto factory = std::make_unique<TMVA::Factory>(
      "TMVAClassification", outputFile.get(),
      "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification");
    std:;string dataset_name = "dataset_" + mode + "_" + year + "_discrete";
    auto dataloader_raii = std::make_unique<TMVA::DataLoader>(dataset_name.c_str());
    auto *dataloader = dataloader_raii.get();
    if ( mode == "1p1" ){
        //dataloader->AddVariable( "Delta_Eta", 'F' );
        dataloader->AddVariable( "Delta_Y", 'F' );
        dataloader->AddVariable( "MassHiggsCandidate_regressed", 'F' );
        //dataloader->AddVariable( "MH", 'F' );
        dataloader->AddVariable( "Tagger_H_discrete", 'I' );
        dataloader->AddVariable( "Tagger_Y_discrete", 'I' );
        dataloader->AddSpectator( "Tagger_H", 'F' );
        dataloader->AddSpectator( "Tagger_Y", 'F' );
        dataloader->AddSpectator( "BDT_weight", 'F' );
        dataloader->AddSpectator( "sample_ID", 'I' );
    }
    else if ( mode == "2p1" ){
        dataloader->AddVariable( "MassHiggsCandidate_regressed", 'F' );
        //dataloader->AddVariable( "MH", 'F' );
        dataloader->AddVariable( "Tagger_H_discrete", 'I' );
        dataloader->AddVariable( "Tagger_b_Y0_discrete", 'I' );
        dataloader->AddVariable( "Tagger_b_Y1_discrete", 'I' );
        dataloader->AddSpectator( "Tagger_H", 'F' );
        dataloader->AddSpectator( "BDT_weight", 'F' );
        dataloader->AddSpectator( "Tagger_b_Y0", 'F' );
        dataloader->AddSpectator( "Tagger_b_Y1", 'F' );
        dataloader->AddSpectator( "sample_ID", 'I' );
    }
    Double_t signalWeight     = 1.0;
    Double_t backgroundWeight = 1.0;
    dataloader->AddSignalTree    ( signalTree,     signalWeight );
    dataloader->AddBackgroundTree( background, backgroundWeight );
    dataloader->SetBackgroundWeightExpression( "BDT_weight" );
    dataloader->SetSignalWeightExpression( "BDT_weight" );
    TCut mycuts = "";
    TCut mycutb = "";
    dataloader->PrepareTrainingAndTestTree( mycuts, mycutb, "nTrain_Signal="s + std::to_string(nSig * 7  / 10) + ":nTrain_Background="s + std::to_string(nBKG * 7  / 10) + ":SplitMode=Random:NormMode=NumEvents:!V" );
    //factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDT", "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
    //factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDT", "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=100" );
    //factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTG", "!H:!V:NTrees=20:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" );
     factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTG","!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" );
 
    factory->TrainAllMethods();
    factory->TestAllMethods();
    factory->EvaluateAllMethods();
    outputFile->Write();
    return 0;
}
