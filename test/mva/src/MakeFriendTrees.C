#include "TTree.h"
#include "TFile.h"
#include "TEventList.h"
#include "TROOT.h"
#include "TDirectory.h"

#include <iostream>

void MakeFriendTrees(TTree* tree , TString outfname , TString inname , bool dotth , bool dodig , bool dotg , TString cut = "" );
struct particleInfo{
  float pt,eta,phi,other, w, another;
  unsigned short number;
  bool isSet;
};

struct Nb_scenario{
  char index_forward, index_highpt , index_secondpt;
};

#include "TMVA/Reader.h"
void MakeFriendTrees(TTree* tree , TString outfname , TString inname , bool dotth , bool dodig , bool dotg , TString cut  ){
  char nJets;
  particleInfo  eventshapes, THReco, Top, lepton, DiG , foxwolf1 , G1 , G2; //met
  Nb_scenario oneB, twoB;
  std::vector<float>* jetsEta = new std::vector<float>();
  float met, forwardJetEta, aplanarity, thdphi , isotropy , jprime , nJetsF , fwf1ONE , digeta , minGmva;
  char LeptonType;
  
  tree->SetBranchAddress("nJets" , &nJets );
  tree->SetBranchAddress("met"   , &met   );
  tree->SetBranchAddress("eventshapes" , &(eventshapes.pt) );
  tree->SetBranchAddress("DiG" , &(DiG.pt) );
  tree->SetBranchAddress("G1" , &(G1.pt) );
  tree->SetBranchAddress("G2" , &(G2.pt) );
  //tree->SetBranchAddress("Top" , &(Top.pt) );
  tree->SetBranchAddress("oneB" , &(oneB.index_forward) );
  tree->SetBranchAddress("twoB" , &(twoB.index_forward) );
  tree->SetBranchAddress("jetsEta" , &jetsEta );
  tree->SetBranchAddress("LeptonType" , &LeptonType );
  tree->SetBranchAddress("lepton" , &lepton);
  tree->SetBranchAddress( "foxwolf1" , &foxwolf1 );

  // ========================= FOR A SIMPLE TREE GEORGIOS : ===========================
  // double nJetsD, metD, jprimeetaD , chargeD,aplanD, foxD ;
  // float nJets_F, met_F, jprimeeta_F , charge_F,aplan_F, fox_F , absJeta;
  // tree->SetBranchAddress("njets" , &nJetsD );
  // tree->SetBranchAddress("jprime_eta"   , &jprimeetaD   );
  // tree->SetBranchAddress("met" , &(metD) );
  // tree->SetBranchAddress("charge" , &chargeD );
  // tree->SetBranchAddress("aplanarity" , &aplanD);
  // tree->SetBranchAddress( "fox_one" , &foxD );
  // ========================= SIMPLE TREE =============================================
  
  TMVA::Reader* readertth = NULL;
  TMVA::Reader* readerdig = NULL;
  TMVA::Reader* readertg = NULL;

  if(dotth){
    readertth = new TMVA::Reader("ttH");
    readertth->AddVariable( "nJets", &nJetsF );
    readertth->AddVariable( "Max$( abs(jetsEta) )", &forwardJetEta );
    readertth->AddVariable( "met.pt", &met );
    //readertth->AddVariable( "lepton.charge", &(lepton.another) );
    readertth->AddVariable( "lepton.charge", &(lepton.another) );
    readertth->AddVariable( "eventshapes.aplanarity" , &aplanarity );
    readertth->AddVariable( "foxwolf1.ONE" , &fwf1ONE );

    // ========================= FOR A SIMPLE TREE GEORGIOS : ===========================
    // readertth->AddVariable( "nJets", &nJets_F );
    // readertth->AddVariable( "Max$( abs(jetsEta) )", &absJeta );
    // readertth->AddVariable( "met.pt", &met_F );
    // //readertth->AddVariable( "lepton.charge", &(lepton.another) );
    // readertth->AddVariable( "lepton.charge", &(charge_F) );
    // readertth->AddVariable( "eventshapes.aplanarity" , &aplan_F );
    // readertth->AddVariable( "foxwolf1.ONE" , &fox_F );
    // ========================= SIMPLE TREE =============================================
        

    //readertth->BookMVA( inname , "ttH/weights/" + inname + "_BDT_TTH0.weights.xml" );
    readertth->BookMVA( "LowNT" , "ttH/FinalWeights/w10_10_3_15_10.weights.xml" );
    readertth->BookMVA( "HighNT" , "ttH/FinalWeights/w400_30_2_30_10.weights.xml" );
  }

  if(dodig){
    readerdig = new TMVA::Reader("DiG");
    readerdig->AddVariable( "nJets", &nJetsF );
    readerdig->AddVariable( "met.pt", &met );
    readerdig->AddVariable( "DiG.pt", &(DiG.pt) );
    readerdig->AddVariable( "abs(DiG.eta)" , &digeta );
    readerdig->AddVariable( "DiG.mva" , &(DiG.another) );
    readerdig->AddVariable( "((G1.mva>G2.mva)*G2.mva +  (G1.mva<=G2.mva)*G1.mva)" , &(minGmva) );

    readerdig->BookMVA( inname , "DiG/weights/" + inname + "_BDT_DiG.weights.xml" );
  }

  if(dodig){
    readertg = new TMVA::Reader("ttGX");
    readertg->AddVariable( "nJets", &nJetsF );
    readertg->AddVariable( "met.pt", &met );
    readertg->AddVariable( "DiG.pt", &(DiG.pt) );
    readertg->AddVariable( "abs(DiG.eta)" , &digeta );
    readertg->AddVariable( "DiG.mva" , &(DiG.another) );
    readertg->AddVariable( "((G1.mva>G2.mva)*G2.mva +  (G1.mva<=G2.mva)*G1.mva)" , &(minGmva) );


    readertg->BookMVA( inname , "ttGX/weights/" + inname + "_BDT_ttGj.weights.xml" );
  }
  
  TEventList* listofevents = NULL;

  if( cut != ""){
    gROOT->cd();
    tree->Draw(">>Listofevents" , cut );
    listofevents = (TEventList*)(gDirectory->Get("Listofevents"));
  }
  
  TFile* fout = TFile::Open(outfname + ".root", "RECREATE");
  fout->cd();
  TTree FTree("friend", "the friend tree");

  float BDTValTTH_1, BDTValTTH_2, BDTValDiG , BDTValTTGX;
  if(dotth){
    FTree.Branch( "BDT_LowNT" , &BDTValTTH_1 );
    FTree.Branch( "BDT_HighNT" , &BDTValTTH_2 );
  }
  if(dodig)
    FTree.Branch( "BDTDiG" , &BDTValDiG );
  if(dotg)
    FTree.Branch( "BDTttGX" , &BDTValTTGX );
  
  FTree.Branch( "mGG" , &DiG.other );

  Long64_t nentries = listofevents ? listofevents->GetN() : tree->GetEntries() ;
  for(Long64_t ii = 0 ; ii < nentries ; ii++){
    Long64_t i = ii;
    if( listofevents )
      i = listofevents->GetEntry( ii );

    tree->GetEntry(i);    
    BDTValDiG = BDTValTTH_1 = BDTValTTH_2 = BDTValTTGX = -1000;

    nJetsF = int(nJets);
    aplanarity = eventshapes.pt;
    fwf1ONE = foxwolf1.another;
    thdphi = THReco.eta;
    forwardJetEta = 0;
    for(auto j : *jetsEta){
      float absj = fabs( j );
      forwardJetEta = (forwardJetEta > absj) ? forwardJetEta : absj ;
    }
    isotropy = eventshapes.w ;
    jprime = Top.phi ;
    digeta = fabs(DiG.eta);

    if(G1.other > G2.other)
      minGmva = G2.other;
    else
      minGmva = G1.other;

    // ========================= FOR A SIMPLE TREE GEORGIOS : ===============================
    // absJeta = ( jprimeetaD );
    // nJets_F = nJetsD;
    // met_F = metD;
    // charge_F = charge_F;
    // aplan_F = aplanD;
    // fox_F = foxD;
    // ========================= SIMPLE TREE (Comment jetsEta->size() > 0 if needed ) =======
    if( dotth ){
      if(jetsEta->size() > 0 ){
	BDTValTTH_1 = readertth->EvaluateMVA("LowNT");
	BDTValTTH_2 = readertth->EvaluateMVA("HighNT");
      }
    }

    if( dodig )
      BDTValDiG = readerdig->EvaluateMVA(inname);

    if( dotg )
      BDTValTTGX = readertg->EvaluateMVA(inname);

    if( cut != ""){
      if( BDTValTTH_1 > 0 )
	FTree.Fill();
    }else
      FTree.Fill();
  }

  FTree.Write();
  fout->Close();

};
