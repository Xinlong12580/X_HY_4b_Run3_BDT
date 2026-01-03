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

int BDT_Trainer(std::string mode){

    TMVA::Tools::Instance();
    TString BKG_fname = "datasets/BKGs_" + mode + "_ALL.root";
    TString Signal_fname = "datasets/reweighted_Signal_nom_tagged_selected_SKIM_skimmed_2022EE__SignalMC_XHY4b__MX-1600_MY-200_" + mode + "_ALL.root";
    std::unique_ptr<TFile> BKG_file{TFile::Open(BKG_fname)};
    std::unique_ptr<TFile> Signal_file{TFile::Open(Signal_fname)};
    TTree *signalTree     = (TTree*)Signal_file->Get("Events");
    TTree *background     = (TTree*)BKG_file->Get("Events");
    std::cout<<"Total signal events: "<<signalTree->GetEntries()<<std::endl<<"Total signal events: "<<background->GetEntries()<<std::endl;
    TString outfileName("TMVAC_" + mode + ".root");
    std::unique_ptr<TFile> outputFile{TFile::Open(outfileName, "RECREATE")};
    auto factory = std::make_unique<TMVA::Factory>(
      "TMVAClassification", outputFile.get(),
      "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification");
    std:;string dataset_name = "dataset_" + mode;
    auto dataloader_raii = std::make_unique<TMVA::DataLoader>(dataset_name.c_str());
    auto *dataloader = dataloader_raii.get();
    //dataloader->AddVariable( "DeltaEta", 'F' );
    dataloader->AddVariable( "DeltaY", 'F' );

    dataloader->AddVariable( "MassHiggsCandidate", 'F' );
    dataloader->AddVariable( "PNet_H", 'F' );
    dataloader->AddVariable( "PNet_Y", 'F' );
    dataloader->AddSpectator( "BDT_weight", 'F' );
    dataloader->AddSpectator( "minPNet", 'F' );
    dataloader->AddSpectator( "sample_ID", 'I' );
    Double_t signalWeight     = 1.0;
    Double_t backgroundWeight = 1.0;
    dataloader->AddSignalTree    ( signalTree,     signalWeight );
    dataloader->AddBackgroundTree( background, backgroundWeight );
    dataloader->SetBackgroundWeightExpression( "BDT_weight" );
    dataloader->SetSignalWeightExpression( "BDT_weight" );
    //TCut mycuts = "PNet_H > 0.2 && PNet_Y > 0.2 && PNet_H < 0.9 && PNet_Y < 0.9";
    //TCut mycutb = "PNet_H > 0.2 && PNet_Y > 0.2 && PNet_H < 0.9 && PNet_Y < 0.9";
    TCut mycuts = "PNet_H > 0.3 && PNet_Y > 0.3";
    TCut mycutb = "PNet_H > 0.3 && PNet_Y > 0.3";
    //TCut mycuts = "";
    //TCut mycutb = "";
    dataloader->PrepareTrainingAndTestTree( mycuts, mycutb, "nTrain_Signal=10000:nTrain_Background=30000:SplitMode=Random:NormMode=NumEvents:!V" );
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
