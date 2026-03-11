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

int BDT_Trainer(){

    TMVA::Tools::Instance();
    TString BKG_fname = "BDT_training/BDT_TTBar.root";
    TString Signal_fname = "BDT_training/BDT_Signal.root";
    std::unique_ptr<TFile> BKG_file{TFile::Open(BKG_fname)};
    std::unique_ptr<TFile> Signal_file{TFile::Open(Signal_fname)};
    TTree *signalTree     = (TTree*)Signal_file->Get("Events");
    TTree *background     = (TTree*)BKG_file->Get("Events");
    TString outfileName("TMVAC.root");
    std::unique_ptr<TFile> outputFile{TFile::Open(outfileName, "RECREATE")};
    auto factory = std::make_unique<TMVA::Factory>(
      "TMVAClassification", outputFile.get(),
      "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification");
    auto dataloader_raii = std::make_unique<TMVA::DataLoader>("dataset");
    auto *dataloader = dataloader_raii.get();
    dataloader->AddVariable( "DeltaEta", 'F' );
    dataloader->AddVariable( "MassHiggsCandidate", 'F' );
    dataloader->AddVariable( "PNet_H", 'F' );
    dataloader->AddVariable( "PNet_Y", 'F' );
    //dataloader->AddSpectator( "PNet_Y", 'F' );
    Double_t signalWeight     = 1.0;
    Double_t backgroundWeight = 1.0;
    dataloader->AddSignalTree    ( signalTree,     signalWeight );
    dataloader->AddBackgroundTree( background, backgroundWeight );
    dataloader->SetBackgroundWeightExpression( "genWeight" );
    //TCut mycuts = "PNet_H > 0.2 && PNet_Y > 0.2 && PNet_H < 0.9 && PNet_Y < 0.9";
    //TCut mycutb = "PNet_H > 0.2 && PNet_Y > 0.2 && PNet_H < 0.9 && PNet_Y < 0.9";
    //TCut mycuts = "PNet_H > 0.3 && PNet_Y > 0.3";
    //TCut mycutb = "PNet_H > 0.3 && PNet_Y > 0.3";
    TCut mycuts = "";
    TCut mycutb = "";
    dataloader->PrepareTrainingAndTestTree( mycuts, mycutb, "nTrain_Signal=1000:nTrain_Background=1000:SplitMode=Random:NormMode=NumEvents:!V" );
    //factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDT", "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
    //factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDT", "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=100" );
    //factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTG", "!H:!V:NTrees=20:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" );
     factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTG","!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" );
 
    factory->TrainAllMethods();
    factory->TestAllMethods();
    factory->EvaluateAllMethods();
    outputFile->Write();
    //if (!gROOT->IsBatch()) TMVA::TMVAGui( outfileName );
    return 0;
}
