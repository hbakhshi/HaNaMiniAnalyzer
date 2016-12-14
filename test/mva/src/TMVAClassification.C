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

using namespace std;

const string DEFAULT_INFNAME  = "/home/hbakhshi/Desktop/tHq/nTuples/FoxWolfram2";

int TMVAClassification( TString myMethodList = "" ,    TString extention = "" )
{
   TMVA::Tools::Instance();
   std::map<std::string,int> Use;
   Use["ttH"] = 1;
   Use["DiG"] = 1;
   Use["ttGj"] = 1;
   
   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++)
	it->second = 0;

      std::vector<TString> mlist = TMVA::gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
	std::string regMethod(mlist[i]);

	if (Use.find(regMethod) == Use.end()) {
	  std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
	  for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) std::cout << it->first << " ";
	  std::cout << std::endl;
	  return 1;
	}
	Use[regMethod] = 1;
      }
   }

   TString infname     = DEFAULT_INFNAME;

   TString outfileName( "TMVA_"+ extention  +".root" );
   TFile* outputFile = TFile::Open( outfileName, "RECREATE" );
   
   TMVA::Factory *factory = new TMVA::Factory( extention , outputFile,
                                               "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );
   
   TFile *inputS = TFile::Open( infname + "/Signal.root" );
   TTree *signalTree     = (TTree*)inputS->Get("tHq/Trees/Events");
   Double_t signalWeight     = 1.0;
   TString default_w_str = "Weight.W0 * G1.w * G2.w";
   
   TMVA::DataLoader *dataloader_tth = NULL;
   TMVA::DataLoader *dataloader_dig = NULL;
   TMVA::DataLoader *dataloader_ttgg = NULL;
   
   if( Use["ttH"] ){

     std::cout << "Loading ttH trees" << endl;
     TFile *inputB = TFile::Open( infname + "/ttH.root" );
     TTree *background_ttH  = (TTree*)inputB->Get("tHq/Trees/Events");

     dataloader_tth =new TMVA::DataLoader("ttH");
     // (please check "src/Config.h" to see all available global options)
     //
     //(TMVA::gConfig().GetVariablePlotting()).fTimesRMS = 8.0;
     //(TMVA::gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory";

     dataloader_tth->AddVariable( "nJets", "nJets", "", 'I' ) ;
     dataloader_tth->AddVariable( "Max$( abs(jetsEta) )","jprimeeta" , "" , 'F' );
     dataloader_tth->AddVariable( "met.pt", "met", "", 'F' );
     dataloader_tth->AddVariable( "lepton.charge","LepCharge" , "" , 'I' );
     dataloader_tth->AddVariable( "eventshapes.aplanarity" , "aplanarity" , "" , 'F' );
     dataloader_tth->AddVariable( "foxwolf1.ONE" , "fwf1ONE" , "" , 'F' );
     
     // dataloader->AddSignalTree( signalTrainingTree, signalTrainWeight, "Training" );
     // dataloader->AddSignalTree( signalTestTree,     signalTestWeight,  "Test" );
     
     dataloader_tth->AddSignalTree( signalTree,     signalWeight );
     dataloader_tth->AddBackgroundTree( background_ttH, 1 );

     dataloader_tth->SetBackgroundWeightExpression( default_w_str  );
     dataloader_tth->SetSignalWeightExpression( default_w_str );
     TString cut_tth = "(DiG.mass > 100) && (Sum$(jetsPt>30) > 1 ) && (nMbJets==1) && (jetsPt[0] > 30) && (met > 30) && (LeptonType == 1 || LeptonType == 2) && (lepton.pt > 20)";
     TCut mycuts_tth = TCut(cut_tth);
     TCut mycutb_tth = TCut(cut_tth);
     dataloader_tth->PrepareTrainingAndTestTree( mycuts_tth, mycutb_tth,
						 "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V");

     factory->BookMethod( dataloader_tth, TMVA::Types::kBDT, "BDT_TTH",
			  "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
   }
   
   if( Use["DiG"] ){
     std::cout << "Loading DiG trees" << endl;
     TChain *backgroundDiG = new TChain("tHq/Trees/Events");
     backgroundDiG->Add(infname + "/DiPhoton_Jets.root" );


     dataloader_dig=new TMVA::DataLoader("DiG");

     dataloader_dig->AddVariable( "nJets", "nJets", "", 'I' ) ;
     dataloader_dig->AddVariable( "met.pt", "met", "", 'F' );
     dataloader_dig->AddVariable( "DiG.pt" , "digpt" , "" , 'F' );
     dataloader_dig->AddVariable( "abs(DiG.eta)" , "digeta" , "" , 'F' );
     dataloader_dig->AddVariable( "DiG.mva" , "digmva" , "" , 'F' );
     dataloader_dig->AddVariable( "((G1.mva>G2.mva)*G2.mva +  (G1.mva<=G2.mva)*G1.mva)" , "minGmva" , "" , 'F' );
     dataloader_dig->AddSignalTree( signalTree,     signalWeight );
     dataloader_dig->AddBackgroundTree( backgroundDiG, 1 );

     dataloader_dig->SetBackgroundWeightExpression( default_w_str  );
     dataloader_dig->SetSignalWeightExpression( default_w_str );
     TString cut_dig = "(DiG.mass > 100) && (met > 30)";
     TCut mycuts_dig = TCut(cut_dig);
     TCut mycutb_dig = TCut(cut_dig);
     dataloader_dig->PrepareTrainingAndTestTree( mycuts_dig, mycutb_dig,
						 "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V");
     factory->BookMethod( dataloader_dig, TMVA::Types::kBDT, "BDT_DiG",
			  "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );     
   }

   if( Use["ttGj"] ){
     std::cout << "Loading ttGj trees" << endl;
     TChain *backgroundTTGG = new TChain("tHq/Trees/Events");
     backgroundTTGG->Add( infname + "/TTGJ.root" );
     backgroundTTGG->Add( infname + "/TGJ.root" );

     dataloader_ttgg=new TMVA::DataLoader("ttGX");

     dataloader_ttgg->AddVariable( "nJets", "nJets", "", 'I' ) ;
     dataloader_ttgg->AddVariable( "met.pt", "met", "", 'F' );
     dataloader_ttgg->AddVariable( "DiG.pt" , "digpt" , "" , 'F' );
     dataloader_ttgg->AddVariable( "abs(DiG.eta)" , "digeta" , "" , 'F' );
     dataloader_ttgg->AddVariable( "DiG.mva" , "digmva" , "" , 'F' );
     dataloader_ttgg->AddVariable( "((G1.mva>G2.mva)*G2.mva +  (G1.mva<=G2.mva)*G1.mva)" , "minGmva" , "" , 'F' );
     
     dataloader_ttgg->AddSignalTree( signalTree,     signalWeight );
     dataloader_ttgg->AddBackgroundTree( backgroundTTGG, 1 );

     dataloader_ttgg->SetBackgroundWeightExpression( default_w_str  );
     dataloader_ttgg->SetSignalWeightExpression( default_w_str );
     TString cut_ttgg = "(DiG.mass > 100) && (Sum$(jetsPt>30) > 1 ) && (nMbJets==1) && (jetsPt[0] > 30) && (met > 30) " ;//&& (LeptonType == 1 || LeptonType == 2) && (lepton.pt > 20)";
     TCut mycuts_ttgg = TCut(cut_ttgg);
     TCut mycutb_ttgg = TCut(cut_ttgg);
     dataloader_ttgg->PrepareTrainingAndTestTree( mycuts_ttgg, mycutb_ttgg,
						  "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V");
     factory->BookMethod( dataloader_ttgg, TMVA::Types::kBDT, "BDT_ttGj",
			  "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
   }
     

   
   // --------------------------------------------------------------------------------------------------
   //  Now you can optimize the setting (configuration) of the MVAs using the set of training events
   // STILL EXPERIMENTAL and only implemented for BDT's !
   //
   // factory->OptimizeAllMethods("SigEffAt001","Scan");
   // factory->OptimizeAllMethods("ROCIntegral","FitGA");
   //
   // --------------------------------------------------------------------------------------------------

   // Now you can tell the factory to train, test, and evaluate the MVAs
   //
   // Train MVAs using the set of training events
   factory->TrainAllMethods();

   // Evaluate all MVAs using the set of test events
   factory->TestAllMethods();

   // Evaluate and compare performance of all configured MVAs
   factory->EvaluateAllMethods();

   // --------------------------------------------------------------

   // Save the output
   outputFile->Close();

   std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
   std::cout << "==> TMVAClassification is done!" << std::endl;

   delete factory;
   return 0;
}

int main( int argc, char** argv )
{
   // Select methods (don't look at this code - not of interest)
  TString methodList,ext;
  for (int i=1; i<argc; i++) {
    TString regMethod(argv[i]);
    if( regMethod=="--ext"){
	i++;
	ext = TString(argv[i]);
	continue;
    }
    if (!methodList.IsNull()) methodList += TString(",");
    methodList += regMethod;
  }
  return TMVAClassification(methodList , ext);
}
