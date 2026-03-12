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

int BDT_Trainer_discrete_paraTuning(std::string mode, std::string year, std::string MX, std::string MY, std::vector<int> NTreeses, std::vector<float> MinNodeSizes, std::vector<float> Shrinkages, std::vector<float> BaggedSampleFractions, std::vector<int> nCutses,  std::vector<int> MaxDepthes){
    TMVA::Tools::Instance();
    TString BKG_fname = "datasets/BKGs_RegSig_" + mode + "_" + year + "_ALL.root";
    TString Signal_fname = "datasets/reweighted_RegSig_nom_" + mode + "_tagged_selected_SKIM_skimmed_"+ year +"__SignalMC_XHY4b__MX-" + MX + "_MY-" + MY + "_" + mode + "_ALL.root";
    std::unique_ptr<TFile> BKG_file{TFile::Open(BKG_fname)};
    std::unique_ptr<TFile> Signal_file{TFile::Open(Signal_fname)};
    TTree *signalTree     = (TTree*)Signal_file->Get("Events");
    TTree *background     = (TTree*)BKG_file->Get("Events");
    std::cout<<"Total signal events: "<<signalTree->GetEntries()<<std::endl<<"Total signal events: "<<background->GetEntries()<<std::endl;
    TString outfileName("TMVAC_optimization_" + mode + "_" + year + "_discrete.root");
    std::unique_ptr<TFile> outputFile{TFile::Open(outfileName, "RECREATE")};
    auto factory = std::make_unique<TMVA::Factory>(
      "TMVAClassification", outputFile.get(),
      "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification");
    std:;string dataset_name = "dataset_optimization_" + mode + "_" + year + "_discrete";
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
    //TCut mycuts = "PNet_H > 0.2 && PNet_Y > 0.2 && PNet_H < 0.9 && PNet_Y < 0.9";
    //TCut mycutb = "PNet_H > 0.2 && PNet_Y > 0.2 && PNet_H < 0.9 && PNet_Y < 0.9";
    //TCut mycuts = "PNet_H > 0.3 && PNet_Y > 0.3";
    //TCut mycutb = "PNet_H > 0.3 && PNet_Y > 0.3";
    TCut mycuts = "";
    TCut mycutb = "";
    if (mode == "1p1" ){
        dataloader->PrepareTrainingAndTestTree( mycuts, mycutb, "nTrain_Signal=10000:nTrain_Background=30000:SplitMode=Random:NormMode=NumEvents:!V" );
    }
    else if ( mode == "2p1" ){
        dataloader->PrepareTrainingAndTestTree( mycuts, mycutb, "nTrain_Signal=7000:nTrain_Background=30000:SplitMode=Random:NormMode=NumEvents:!V" );
    }
    for (int i = 0; i < NTreeses.size(); i++)
    {
        std::string NTrees = std::to_string(NTreeses.at(i));
        std::string MinNodeSize = std::to_string(MinNodeSizes.at(i));
        std::string Shrinkage = std::to_string(Shrinkages.at(i));
        std::string BaggedSampleFraction = std::to_string(BaggedSampleFractions.at(i));
        std::string nCuts = std::to_string(nCutses.at(i));
        std::string MaxDepth = std::to_string(MaxDepthes.at(i));
        std::string config = "!H:!V:NTrees=" + NTrees + ":MinNodeSize=" + MinNodeSize + "%:BoostType=Grad:Shrinkage=" + Shrinkage + ":UseBaggedBoost:BaggedSampleFraction=" + BaggedSampleFraction + ":nCuts=" + nCuts + ":MaxDepth=" + MaxDepth;
        std::string val_name = "BDTG_" + NTrees + "_" + MinNodeSize + "_" + Shrinkage + "_" + BaggedSampleFraction + "_" + nCuts + "_" + MaxDepth;
        std::cout<<"Adding Config: "<< config << std::endl;
        factory->BookMethod( dataloader, TMVA::Types::kBDT, val_name.c_str(), config.c_str() );
    }
    factory->TrainAllMethods();
    factory->TestAllMethods();
    factory->EvaluateAllMethods();
    outputFile->Write();
    return 0;
}
