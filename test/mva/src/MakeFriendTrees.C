#include "TTree.h"
#include "TFile.h"
#include "TEventList.h"
#include "TROOT.h"
#include "TDirectory.h"

#include <iostream>

void MakeFriendTrees(TTree* tree, TString outfname);

struct particleInfo{
  float pt,eta,phi,other, w, another;
  unsigned short number;
  bool isSet;
};

struct Nb_scenario{
  char index_forward, index_highpt , index_secondpt;
};

#include "TMVA/Reader.h"
// #include "weights/TMVAClassification_BDT.class.C"
void MakeFriendTrees(TTree* tree , TString outfname ){
  //, int method /*1:.class.C , 2:reader*/ ){
  // ReadBDT* rbdt = NULL;  std::vector<double> vals;
  // std::vector< std::string > names = { "nJets", "met.pt", "eventshapes.aplanarity", "THReco.THDPhi", "abs(jetsEta[oneB.forward])", "eventshapes.isotropy", "Top.JPrime" };
  // rbdt = new ReadBDT(names);
 

  char nJets;
  particleInfo  eventshapes, THReco, Top, lepton, DiG , foxwolf1; //met
  Nb_scenario oneB, twoB;
  std::vector<float>* jetsEta = new std::vector<float>();
  float met, forwardJetEta, aplanarity, thdphi , isotropy , jprime , nJetsF , fwf1ONE , digeta;
  char LeptonType;
  
  tree->SetBranchAddress("nJets" , &nJets );
  tree->SetBranchAddress("met"   , &met   );
  tree->SetBranchAddress("eventshapes" , &(eventshapes.pt) );
  tree->SetBranchAddress("DiG" , &(DiG.pt) );
  //tree->SetBranchAddress("Top" , &(Top.pt) );
  tree->SetBranchAddress("oneB" , &(oneB.index_forward) );
  tree->SetBranchAddress("twoB" , &(twoB.index_forward) );
  tree->SetBranchAddress("jetsEta" , &jetsEta );
  tree->SetBranchAddress("LeptonType" , &LeptonType );
  tree->SetBranchAddress("lepton" , &lepton);
  tree->SetBranchAddress( "foxwolf1" , &foxwolf1 );

  TMVA::Reader* reader = new TMVA::Reader("");
  reader->AddVariable( "nJets", &nJetsF );
  reader->AddVariable( "abs(jprimeeta)", &forwardJetEta );
  reader->AddVariable( "met.pt", &met );
  reader->AddVariable( "lepton.charge", &(lepton.another) );
  reader->AddVariable( "eventshapes.aplanarity" , &aplanarity );
  reader->AddVariable( "foxwolf1.ONE" , &fwf1ONE );


  reader->BookMVA( "BDT" , "weights/TMVAClassification_BDT.weights.xml" );

  TMVA::Reader* readerDiG = new TMVA::Reader("DiG");
  readerDiG->AddVariable( "nJets", &nJetsF );
  readerDiG->AddVariable( "met.pt", &met );
  readerDiG->AddVariable( "DiG.pt", &(DiG.pt) );
  readerDiG->AddVariable( "abs(DiG.eta)" , &digeta );
  readerDiG->AddVariable( "DiG.mva" , &(DiG.another) );


  readerDiG->BookMVA( "BDT" , "dataset/weights/TMVAClassification_BDT.weights.xml" );

  
  TString cut = "(DiG.mass > 100) && (Sum$(jetsPt>30) > 1 ) && (nMbJets==1) && (jetsPt[0] > 30) && (met > 30)"; //&& (LeptonType == 1 || LeptonType == 2) && (lepton.pt > 20) 
  gROOT->cd();
  tree->Draw(">>Listofevents" , cut );
  TEventList* listofevents = (TEventList*)(gDirectory->Get("Listofevents"));
  
  TFile* fout = TFile::Open(outfname + ".root", "RECREATE");
  fout->cd();
  TTree FTree("friend", "the friend tree");

  float BDTVal, BDTValDiG;
  FTree.Branch( "BDT" , &BDTVal );
  FTree.Branch( "BDTDiG" , &BDTValDiG );
  FTree.Branch( "mGG" , &DiG.other );

  //cout << listofevents->GetN() << endl;
  for(int ii = 0 ; ii < listofevents->GetN() ; ii++){
  Long64_t i = listofevents->GetEntry( ii );
  // for(unsigned int i = 0 ; i < tree->GetEntries() ; i++){
    tree->GetEntry(i);    
    BDTValDiG = BDTVal = -1000;

    nJetsF = int(nJets);
    aplanarity = eventshapes.pt;
    fwf1ONE = foxwolf1.another;
    thdphi = THReco.eta;
    forwardJetEta = fabs( jetsEta->at(oneB.index_forward) );
    isotropy = eventshapes.w ;
    jprime = Top.phi ;
    digeta = fabs(DiG.eta);
    
    if( jetsEta->size() > 0 ){
      BDTVal = reader->EvaluateMVA("BDT") ;
    }

    BDTValDiG = readerDiG->EvaluateMVA("BDT");
    
    
    //if( BDTVal > 0 )
    FTree.Fill();
  }

  FTree.Write();
  fout->Close();

};
