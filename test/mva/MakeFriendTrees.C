#include "TTree.h"
#include "TFile.h"

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
void MakeFriendTrees(TTree* tree , TString outfname ){ //, int method /*1:.class.C , 2:reader*/ ){
  // ReadBDT* rbdt = NULL;  std::vector<double> vals;
  // std::vector< std::string > names = { "nJets", "met.pt", "eventshapes.aplanarity", "THReco.THDPhi", "abs(jetsEta[oneB.forward])", "eventshapes.isotropy", "Top.JPrime" };
  // rbdt = new ReadBDT(names);
 

  char nJets;
  particleInfo  eventshapes, THReco, Top, lepton; //met
  Nb_scenario oneB, twoB;
  std::vector<float>* jetsEta = new std::vector<float>();
  float met, forwardJetEta, aplanarity, thdphi , isotropy , jprime , nJetsF , fwf1ONE;
  char LeptonType;
  
  TMVA::Reader* reader = new TMVA::Reader("");
  reader->AddVariable( "nJets", &nJetsF );
  reader->AddVariable( "abs(jprimeeta)", &forwardJetEta );
  reader->AddVariable( "met.pt", &met );
  reader->AddVariable( "lepton.charge", &(lepton.another) );
  reader->AddVariable( "eventshapes.aplanarity" , &aplanarity );
  reader->AddVariable( "foxwolf1.ONE" , &fwf1ONE );


  reader->BookMVA( "BDT" , "weights/TMVAClassification_BDT.weights.xml" );

  tree->SetBranchAddress("nJets" , &nJets );
  tree->SetBranchAddress("met"   , &met   );
  tree->SetBranchAddress("eventshapes" , &(eventshapes.pt) );
  // tree->SetBranchAddress("THReco" , &(THReco.pt) );
  // tree->SetBranchAddress("Top" , &(Top.pt) );
  tree->SetBranchAddress("oneB" , &(oneB.index_forward) );
  tree->SetBranchAddress("twoB" , &(twoB.index_forward) );
  tree->SetBranchAddress("jetsEta" , &jetsEta );
  tree->SetBranchAddress("LeptonType" , &LeptonType );
  tree->SetBranchAddress("lepton" , &lepton);

  TFile* fout = TFile::Open(outfname + ".root", "RECREATE");
  fout->cd();
  TTree FTree("friend", "the friend tree");

  float BDTVal;
  FTree.Branch( "BDT" , &BDTVal );
  
  for(unsigned int i = 0 ; i < tree->GetEntries() ; i++){
    tree->GetEntry(i);    
    BDTVal = -1000;

    if( jetsEta->size() > 0 ){
      nJetsF = int(nJets);
      aplanarity = eventshapes.pt;
      thdphi = THReco.eta;
      if(LeptonType == 4 ){
	//cout << jetsEta->size() << "  " << int(twoB.index_forward) << endl;
	forwardJetEta = fabs( jetsEta->at( int(twoB.index_forward)-1 ) );
      }else{
	forwardJetEta = fabs( jetsEta->at(oneB.index_forward) );
      }
      isotropy = eventshapes.w ;
      jprime = Top.phi ;
      
      BDTVal = reader->EvaluateMVA("BDT") ;
      // vals.clear();
      // vals.push_back(nJetsF);
      // vals.push_back(met);
      // vals.push_back(aplanarity);
      // vals.push_back(thdphi);
      // vals.push_back(forwardJetEta);
      // vals.push_back(isotropy);
      // vals.push_back(jprime);

      // BDTval = rbdt->GetMvaValue( vals ) ;
    }
    
    FTree.Fill();
  }

  FTree.Write();
  fout->Close();

};
