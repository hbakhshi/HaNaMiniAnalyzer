#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/BaseMiniAnalyzer.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"

#include "TTree.h"
#include <iostream>
#include "TROOT.h"
#include "TDirectory.h"

#include "PhysicsTools/CandUtils/interface/EventShapeVariables.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "SemiLepTopQuark.h"

#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/FoxWolfram.hpp"


using namespace std;

class UIntReader : public BaseEventReader< unsigned int  > {
public:
  UIntReader( std::string tag , edm::ConsumesCollector && iC) :
    BaseEventReader< unsigned int  >(tag , &iC)
  {
  };
  unsigned int read( const edm::Event& iEvent ){
    BaseEventReader< unsigned int  >::Read( iEvent );
    return *handle;
  };
};
class LIntReader : public BaseEventReader< unsigned long long  > {
public:
  LIntReader( std::string tag , edm::ConsumesCollector && iC) :
    BaseEventReader< unsigned long long  >(tag , &iC)
  {
  };
  unsigned long long read( const edm::Event& iEvent ){
    BaseEventReader< unsigned long long  >::Read( iEvent );
    return *handle;
  };
};

class tHqAnalyzer : public BaseMiniAnalyzer{
public:
  explicit tHqAnalyzer(const edm::ParameterSet&);
  ~tHqAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions){ BaseMiniAnalyzer::fillDescriptions( descriptions ); }
protected:
  virtual void beginJob() override;
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;

  flashggJetReader* flashggjetreader_lowpt;
  // void endRun(edm::Run const& iRun, edm::EventSetup const&) override {
  //   edm::Handle<LHERunInfoProduct> run; 
  //   typedef std::vector<LHERunInfoProduct::Header>::const_iterator headers_const_iterator;
 
  //   iRun.getByToken( LHERunInfoProduct_Token , run );
  //   LHERunInfoProduct myLHERunInfoProduct = *(run.product());
 
  //   for (headers_const_iterator iter=myLHERunInfoProduct.headers_begin(); iter!=myLHERunInfoProduct.headers_end(); iter++){
  //     std::cout << iter->tag() << std::endl;
  //     std::vector<std::string> lines = iter->lines();
  //     for (unsigned int iLine = 0; iLine<lines.size(); iLine++) {
  // 	std::cout << lines.at(iLine);
  //     }
  //   }
  // };

  unsigned int RunN;
  unsigned long long EventN;
  unsigned char SelectionStep;

  unsigned char nVertices, nJets, nLbJets , nMbJets , nTbJets, LeptonType , nMuons, nEles , nElesVeto , nGPairs , nSelGPairs ;
  struct particleinfo{
    float pt, eta, phi , other , w , another; //other : for photon id, for diphoton mass, for jets btagging vals
    unsigned short number;
    bool isSet;
    particleinfo( double pt_=-999, double eta_ =-999, double phi_=-999 , double other_ = -999 , double W = 1.0 ){
      pt = pt_;
      eta= eta_;
      phi = phi_;
      other = other_;
      w = W;
      number = 255;
      isSet = false;
    };
    void set(double pt_=-999, double eta_ =-999, double phi_=-999 , double other_ = -999 , double W = 1.0 , double Another = -999 ){
      pt = pt_;
      eta= eta_;
      phi = phi_;
      other = other_;
      w = W;
      another = Another;
      isSet = true;
    };
  };
  void FillTree(){
    if( !MakeTree )
      return;

    for(unsigned int i=0 ; i < nHistos ; i++)
      Weight[i] = W[i];

    theSelectionResultTree->Fill();
  }
  std::valarray<double> W;
  float* Weight;
  float genW , puWeight , diGMVA ;
  float* bSelWeights;
  particleinfo G1 , G2 , DiG , lepton, leptonextrainfo , eventshapes , eventshapesMet , met , THReco , Top ;
  particleinfo foxwolf1 , foxwolf2 , foxwolf1Met, foxwolf2Met ;

  char  closest_jet_index ;
  float closest_jet_dr, HT    ;

  std::vector<float> jetsPt;
  std::vector<float> jetsEta;
  std::vector<float> jetsPhi;
  std::vector<float> jetsE;
  std::vector<int> jetsIndex;

  struct Nb_scenario{
    char index_forward, index_highpt , index_secondpt ;
    void set( int f , int leading , int subleading ){
      index_forward = f ;
      index_highpt = leading ;
      index_secondpt = subleading ;
    };

    void Print(std::string name){
      cout << name << " : f," << int(index_forward) << " ; pt," << int(index_highpt) << " ; pt2," << int(index_secondpt) << endl;
    };
  };
  Nb_scenario zeroB , oneB , twoB ;
  void resetTreeVals(){
    RunN = 0;
    EventN = 0;
    SelectionStep = nVertices = nJets = nLbJets = nMbJets = nTbJets = LeptonType = nMuons = nElesVeto = nEles = nGPairs = nSelGPairs = 250;

    W = 1.0;
    for(unsigned int i=0 ; i < nHistos ; i++)
      Weight[i] = 1.0 ;

    for(unsigned int i=0 ; i < 12 ; i++)
      bSelWeights[i] = 1.0;

    genW = puWeight = -999;
    particleinfo tmp;
    Top = THReco = G1 = G2 = DiG = lepton = leptonextrainfo = met = tmp ;
    eventshapes = foxwolf1 = foxwolf2 = foxwolf1Met = foxwolf2Met = tmp ;

    jetsPhi.clear();
    jetsPt.clear();
    jetsEta.clear();
    jetsE.clear();
    jetsIndex.clear();

    zeroB.set( 255 , 255 , 255 );
    oneB.set( 255 , 255 , 255 );
    twoB.set( 255 , 255 , 255 );

    closest_jet_index = 255;
    closest_jet_dr = 1000. ;
    HT = 0. ;
  }

  TTree* theSelectionResultTree;
  unsigned int nHistos;
  bool MakeTree;


  Histograms* M_GG;
  Histograms* Ph1Pt;
  Histograms* Ph1PtRatio;
  
  //edm::EDGetTokenT<LHERunInfoProduct> LHERunInfoProduct_Token;
};

DEFINE_FWK_MODULE(tHqAnalyzer);

tHqAnalyzer::~tHqAnalyzer() {}
tHqAnalyzer::tHqAnalyzer( const edm::ParameterSet& ps ) :
  BaseMiniAnalyzer( ps ),
  theSelectionResultTree( NULL ),
  nHistos(1),
  MakeTree( ps.getParameter<bool>( "StoreEventNumbers" ) )
{
  usesResource("TFileService");

  edm::ParameterSet jetlowpt_pset = ps.getParameter< edm::ParameterSet >("JetsLowPt");
  flashggjetreader_lowpt = new flashggJetReader( jetlowpt_pset , consumesCollector() , IsData , SetupDir );
  //LHERunInfoProduct_Token = consumes<LHERunInfoProduct,edm::InRun>(edm::InputTag("source","","LHEFile"));
}
// ------------ method called once each job just before starting event loop  ------------
void tHqAnalyzer::beginJob()
{
  if( SampleName == "Signal" )
    nHistos = 51;

  if( !IsData && nHistos==1 )
    nHistos = 2;

  W = std::valarray<double>( 1.0 , nHistos);
  Weight = new float[nHistos];

  bSelWeights = new float[12];

  if( MakeTree ){
    edm::Service<TFileService> fs;
    //fs->cd();
    TFileDirectory treeDir = fs->mkdir( "Trees" );
    //treeDir.cd();

    // TFile* f = TFile::Open("tree.root" , "RECREATE");
    // f->cd();
    // gDirectory->Print();
    theSelectionResultTree = treeDir.make<TTree>("Events" , "Events");
    //fs->make<TTree>("SelectedEventNumbers" , "SelectedEventNumbers");
    
    // gDirectory->Print();
    theSelectionResultTree->Branch("EventNumber", &EventN );
    theSelectionResultTree->Branch("RunNumber", &RunN );
    theSelectionResultTree->Branch("SelectionStep", &SelectionStep );
    theSelectionResultTree->Branch("nVertices" , &nVertices);
    theSelectionResultTree->Branch("nJets" , &nJets);
    theSelectionResultTree->Branch("nLbJets", &nLbJets);
    theSelectionResultTree->Branch("nMbJets", &nMbJets);
    theSelectionResultTree->Branch("nTbJets", &nTbJets);
    theSelectionResultTree->Branch("nMuons", &nMuons);
    theSelectionResultTree->Branch("LeptonType", &LeptonType);
    theSelectionResultTree->Branch("nEles", &nEles);
    theSelectionResultTree->Branch("nElesVeto", &nElesVeto);
    theSelectionResultTree->Branch("nGPairs", &nGPairs);
    theSelectionResultTree->Branch("nSelGPairs", &nSelGPairs);

    std::string weightLeafList = "W0";
    for(unsigned int iii = 1 ; iii < nHistos ; iii++)
      weightLeafList += (":W" + std::to_string(iii) );

    theSelectionResultTree->Branch("Weight", Weight , weightLeafList.c_str() );
    theSelectionResultTree->Branch("puWeight", &puWeight);
    theSelectionResultTree->Branch("genW", &genW);
    theSelectionResultTree->Branch("bWs", bSelWeights , "W0L:W0M:W0T:W1L:W1M:W1M0L:W1T:W1T0L:W1T0M:W2L:W2M:W2T");
    //theSelectionResultTree->Branch("diGMVA", &diGMVA);
    theSelectionResultTree->Branch("met", &met , "pt:phi" );
    theSelectionResultTree->Branch("G1" , &G1.eta , "pt:eta:phi:mva:w:match/s" );
    theSelectionResultTree->Branch("G2" , &G2.eta , "pt:eta:phi:mva:w:match/s"  );
    theSelectionResultTree->Branch("DiG", &DiG , "pt:eta:phi:mass:w:mva"  );
    theSelectionResultTree->Branch("lepton", &lepton , "pt:eta:phi:iso:w:charge"  );
    theSelectionResultTree->Branch("leptonextrainfo", &leptonextrainfo , "muMultiplicity:muEnergyFraction:elecMultiplicity:chargeEMFranction:neutralEMFraction"  );
    theSelectionResultTree->Branch("eventshapes", &eventshapes , "aplanarity:C:circularity:D:isotropy:sphericity"  );
    theSelectionResultTree->Branch("eventshapesMET", &eventshapesMet , "aplanarity:C:circularity:D:isotropy:sphericity"  );
    theSelectionResultTree->Branch("foxwolf1", &foxwolf1 , "SHAT:PT:ETA:PSUM:PZ:ONE" );
    theSelectionResultTree->Branch("foxwolf2", &foxwolf2 , "SHAT:PT:ETA:PSUM:PZ:ONE" );
    theSelectionResultTree->Branch("foxwolf1Met", &foxwolf1Met , "SHAT:PT:ETA:PSUM:PZ:ONE" );
    theSelectionResultTree->Branch("foxwolf2Met", &foxwolf2Met , "SHAT:PT:ETA:PSUM:PZ:ONE" );

    theSelectionResultTree->Branch("THReco", &THReco , "THInvM:THDPhi:THDR" );
    theSelectionResultTree->Branch("Top", &Top , "THDEta:CosTheta:JPrime:WM:topM:CosThetaStar:nLoops/s:goodEvent/O" );

    theSelectionResultTree->Branch("jMuIndex", &closest_jet_index );
    theSelectionResultTree->Branch("jMuDr", &closest_jet_dr );
    theSelectionResultTree->Branch("HT", &HT );

    theSelectionResultTree->Branch("jetsPt", (&jetsPt) );
    theSelectionResultTree->Branch("jetsPhi", (&jetsPhi) );
    theSelectionResultTree->Branch("jetsEta", (&jetsEta) );

    theSelectionResultTree->Branch("zeroB" , &zeroB , "forward/C:leading:subleading" );
    theSelectionResultTree->Branch("oneB" , &oneB , "forward/C:leading:subleading" );
    theSelectionResultTree->Branch("twoB" , &twoB , "forward/C:leading:subleading" );

    resetTreeVals();
  }


  hCutFlowTable = new Histograms( SampleName , "CutFlowTable" , 15 , 0.5 , 15.5 , nHistos );
  M_GG = new Histograms( SampleName , "M_GG" , 10 , 50 , 250 , nHistos );
  Ph1PtRatio = new Histograms(SampleName , "Ph1PtRatio" , 100 , 0 , 10 , nHistos );
  Ph1Pt = new Histograms(SampleName , "Ph1Pt" , 100 , 20 , 520 , nHistos );
}


bool tHqAnalyzer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  resetTreeVals();

  EventN = iEvent.eventAuxiliary().event() ;
  RunN = iEvent.eventAuxiliary().run() ;

  if( nHistos > 1 && SampleName == "Signal" ) {
    LHEReader->Read( iEvent );
    W = LHEReader->ExtractWeightsInRange( 446 , 495 ); 
  }
  SelectionStep = 0;
  
  if( geninfoReader ){
    W *= geninfoReader->Read( iEvent );
    genW = geninfoReader->Weight ;
  }
  if( !IsData && nHistos==2 )
    W[1] = 1.0;
  hCutFlowTable->Fill( ++SelectionStep , W );

  if( hltReader->Read( iEvent ) < 0 )
    return false;
  if( !IsData && nHistos==2 )
    W[1] = 1.0;

  hCutFlowTable->Fill( ++SelectionStep , W );

  if( vertexReader->Read( iEvent ) < 0 )
    return false;
  W *= vertexReader->puWeight;
  if( !IsData && nHistos==1 )
    W[1] = 1.0;

  puWeight = vertexReader->puWeight;
  nVertices = vertexReader->vtxMult;
  hCutFlowTable->Fill( ++SelectionStep , W );

  DiPhotonReader::SelectionStatus diPhoSelStatus = diPhoton->read(iEvent);
  switch( diPhoSelStatus ){
    case DiPhotonReader::Pass:
    case DiPhotonReader::PassMoreThanOne:
      W *= diPhoton->W();
      if( !IsData && nHistos==2 )
	W[1] = 1.0;


      hCutFlowTable->Fill( ++SelectionStep , W );
      DiG.set( diPhoton->diPhoton->pt() ,
	       diPhoton->diPhoton->eta() ,
	       diPhoton->diPhoton->phi() ,
	       diPhoton->diPhoton->mass() ,
	       diPhoton->W() ,
	       diPhoton->theSelected->diGMVA );
  case DiPhotonReader::PairCuts:
    W *= diPhoton->diPhoton->subLeadingPhoton()->centralWeight();
    if( !IsData && nHistos==2 )
      W[1] = 1.0;

    hCutFlowTable->Fill( ++SelectionStep , W );
    G2.set( 0,
	    diPhoton->diPhoton->subLeadingPhoton()->pt(),
	    diPhoton->diPhoton->subLeadingPhoton()->eta(),
	    diPhoton->diPhoton->subLeadingPhoton()->phi(),
	    diPhoton->diPhoton->subLeadingPhoton()->phoIdMvaDWrtVtx( diPhoton->diPhoton->vtx() ) ,
	    diPhoton->diPhoton->subLeadingPhoton()->centralWeight() );
    G2.number = diPhoton->diPhoton->subLeadingPhoton()->genMatchType() ;
  case DiPhotonReader::SubLeadingCuts:
    W *= diPhoton->diPhoton->leadingPhoton()->centralWeight();
    if( !IsData && nHistos==2 )
      W[1] = 1.0;

    hCutFlowTable->Fill( ++SelectionStep , W );
    G1.set( 0,
	    diPhoton->diPhoton->leadingPhoton()->pt(),
	    diPhoton->diPhoton->leadingPhoton()->eta(),
	    diPhoton->diPhoton->leadingPhoton()->phi(),
	    diPhoton->diPhoton->leadingPhoton()->phoIdMvaDWrtVtx( diPhoton->diPhoton->vtx() ),
	    diPhoton->diPhoton->leadingPhoton()->centralWeight() );
    G1.number = diPhoton->diPhoton->leadingPhoton()->genMatchType() ;
  case DiPhotonReader::LeadingCuts:
    hCutFlowTable->Fill( ++SelectionStep , W );

    Ph1PtRatio->Fill( diPhoton->theSelected->lPt / diPhoton->theSelected->diGMass , W );
    Ph1Pt->Fill( diPhoton->theSelected->lPt , W );
  case DiPhotonReader::ZeroPairs:
    nGPairs = diPhoton->handle->size();
    nSelGPairs = diPhoton->nSelGPairs;
  }

  if(diPhoSelStatus < DiPhotonReader::Pass){
    //FillTree();
    return false;
  }

  M_GG->Fill( diPhoton->diPhoton->mass() , W );

  metReader->Read(iEvent);
  met.set( metReader->met.pt() , metReader->met.phi() );


  flashggjetreader->Read( iEvent , diPhoton->diPhoton ); // , &(flashggmuonreader->goodMus[0]) ) )
  //W *= flashggjetreader->W ;

  nJets = flashggjetreader->selectedJets.size();
  if( nJets > 1 )
    hCutFlowTable->Fill( ++SelectionStep , W );

  SelectionStep++;
  SelectionStep++;
  hCutFlowTable->Fill( ++SelectionStep , W );
  hCutFlowTable->Fill( ++SelectionStep , W );


  nLbJets = flashggjetreader->nLB;
  nMbJets = flashggjetreader->nMB;
  nTbJets = flashggjetreader->nTB;


  if(nJets > 0){
    flashggjetreader->getAllWs(bSelWeights);
    // cout << "from thq : " ;
    // for(int ii = 0 ; ii < 12 ; ii++)
    //   cout <<  bSelWeights[ii] << " " ;
    // cout << endl;

    map<int,int> etaSortedJetIndices;
    map<int,int> ptSortedJetIndices;
    for(unsigned int ij = 0 ; ij < flashggjetreader->selectedJets.size() ; ij++){
      int index = flashggjetreader->GetJetbSorted( ij );
      const flashgg::Jet* theJet = &(flashggjetreader->selectedJets[index]) ;
      
      jetsPhi.push_back( theJet->phi() );
      jetsEta.push_back( theJet->eta() );
      jetsPt.push_back( theJet->pt() );
      jetsE.push_back( theJet->energy() );
      jetsIndex.push_back( index );

      int eta_index = flashggjetreader->GetJetEtaSortedIndex( index );
      etaSortedJetIndices[eta_index]  = ij ;

      int pt_index = flashggjetreader->GetJetPtSortedIndex( index );
      ptSortedJetIndices[pt_index] = ij ;
    }

    // cout << "eta indices" ;
    // for(auto iii : etaSortedJetIndices)
    //   cout << iii.first << "," << iii.second << " - " ;
    // cout << endl;

    // cout << "pt indices" ;
    // for(auto iii : ptSortedJetIndices)
    //   cout << iii.first << "," << iii.second << " - " ;
    // cout << endl;

    if( nJets > 3 ){
      zeroB.set( etaSortedJetIndices[0] ,
		 ptSortedJetIndices[0] , 
		 ptSortedJetIndices[1] );

      oneB.set(etaSortedJetIndices[0]==0 ? etaSortedJetIndices[1] : etaSortedJetIndices[0] ,
	       ptSortedJetIndices[0] , 
	       ptSortedJetIndices[1] );

      int index_f = 2;
      for(int ij = 0 ; ij < nJets ; ij++)
	if( etaSortedJetIndices[ij] > 1 ){
	  index_f = etaSortedJetIndices[ij] ;
	  break;
	}
      twoB.set( index_f ,
		ptSortedJetIndices[0] ,
		ptSortedJetIndices[1] );
    }
    else if( nJets == 3 ){
      zeroB.set( etaSortedJetIndices[0] ,
		 ptSortedJetIndices[0] , 
		 ptSortedJetIndices[1] );

      oneB.set(etaSortedJetIndices[0]==0 ? etaSortedJetIndices[1] : etaSortedJetIndices[0] ,
	       ptSortedJetIndices[0] , 
	       ptSortedJetIndices[1] );

      twoB.set(2 , ptSortedJetIndices[0] , ptSortedJetIndices[1] );
    }
    else if( nJets == 2 ){
      zeroB.set( etaSortedJetIndices[0] ,
		 ptSortedJetIndices[0] , 
		 ptSortedJetIndices[1] );

      oneB.set( 1 , ptSortedJetIndices[0] , ptSortedJetIndices[1] );
      twoB.set( etaSortedJetIndices[0] , ptSortedJetIndices[0] , ptSortedJetIndices[1] );
    }
    else if( nJets == 1 ){
      zeroB.set( 0 , 
		 0 ,
		 255 );
      oneB.set( 0 , 
		0 ,
		255 );
      twoB.set( 0 , 
		0 ,
		255 );
    }

    // zeroB.Print("zero");
    // oneB.Print("one");
    // twoB.Print("two");
  }

  flashggMuonReader::SelectionStep muSelStep = flashggmuonreader->Read( iEvent , diPhoton->diPhoton );
  flashggElectronReader::SelectionStep eleSelStep = flashggelectronreader->Read( iEvent , diPhoton->diPhoton );
  flashggElectronReader::SelectionStep eleVetoStep = flashggelectronVetoReader->Read( iEvent , diPhoton->diPhoton );

  nMuons = flashggmuonreader->nMuons;
  nEles  = flashggelectronreader->nElectrons;
  nElesVeto = flashggelectronVetoReader->nElectrons;
  LeptonType = 0;

  if( nMuons == 1 && nElesVeto == 0 ){
    LeptonType = 1 ;


    W *= (flashggmuonreader->W);
    lepton.set( flashggmuonreader->goodMus[0].pt() ,
		flashggmuonreader->goodMus[0].eta() ,
		flashggmuonreader->goodMus[0].phi() ,
		flashggmuonreader->Iso ,
		flashggmuonreader->W ,
		flashggmuonreader->goodMus[0].charge() );
  }else if(nMuons == 0 && nEles == 1 ){
    LeptonType = 2 ;

    W *= (flashggelectronreader->W);
    lepton.set( flashggelectronreader->goodEles[0].pt() ,
		flashggelectronreader->goodEles[0].eta() ,
		flashggelectronreader->goodEles[0].phi() ,
		flashggelectronreader->goodEles[0].energy() ,
		flashggelectronreader->W ,
		flashggelectronreader->goodEles[0].charge() );

  }else if( nMuons == 100 ){
    LeptonType = 3;


    W *= (flashggmuonreader->W);
    lepton.set( flashggmuonreader->goodMus[0].pt() ,
		flashggmuonreader->goodMus[0].eta() ,
		flashggmuonreader->goodMus[0].phi() ,
		flashggmuonreader->Iso ,
		flashggmuonreader->W ,
		flashggmuonreader->goodMus[0].charge() );
  }else if( nJets > 1 && false){
    const flashgg::Jet* theBJet = &(flashggjetreader->selectedJets[ jetsIndex[0] ]) ;
    const flashgg::Jet* theFJet = &(flashggjetreader->selectedJets[ jetsIndex[oneB.index_forward] ]) ;
    flashggjetreader_lowpt->Read( iEvent , diPhoton->diPhoton , {theBJet, theFJet} );
    if( flashggjetreader_lowpt->selectedJets.size() == 1 ){
      LeptonType = 4;

      const flashgg::Jet* theJet = &(flashggjetreader_lowpt->selectedJets[ 0 ] );
      lepton.set( theJet->pt(),
		  theJet->eta() ,
		  theJet->phi() );
      leptonextrainfo.set( theJet->muonMultiplicity (),
			   theJet->muonEnergyFraction () ,
			   theJet->electronMultiplicity (),
			   theJet->chargedEmEnergyFraction ( ),
			   theJet->neutralEmEnergyFraction() );
    }
  }
  


  if( lepton.isSet ){


    for(int i=0 ; i < nJets ; i++){
      float dri = reco::deltaR( jetsEta[i] , jetsPhi[i] , lepton.eta , lepton.phi );
      if( dri < closest_jet_dr ){
	closest_jet_index = i;
	closest_jet_dr = dri ;
      }
    }

    //fprintf (stderr, "l%d.", __LINE__);
    TLorentzVector g1,g2,higgs;


    g1.SetPtEtaPhiM( G1.eta , G1.phi , G1.other , 0 );
    g2.SetPtEtaPhiM( G2.eta , G2.phi , G2.other , 0 );

    higgs = (g1+g2);


    
    TLorentzVector muL,metL ;
    muL.SetPtEtaPhiM( lepton.pt, lepton.eta, lepton.phi , 0 );
    metL.SetPtEtaPhiM( met.pt , 0 , met.eta , 0 );

    std::vector< TLorentzVector > particles_;
    if( LeptonType != 4 ){
      particles_.push_back( muL );
      //cout << "mu:" ; muL.Print();
    }else if(closest_jet_dr > 0.1){// it means that this jet-lepton is not included in the jet collection
      particles_.push_back( muL );
    }
    particles_.push_back( g1 );     //cout << "g1:" ; g1.Print();
    particles_.push_back( g2 );     //cout << "g2:" ; g2.Print();
    for(unsigned int i = 0 ; i < jetsPhi.size() ; i++){
      TLorentzVector ji;
      ji.SetPtEtaPhiE(  jetsPt[i] , jetsEta[i] , jetsPhi[i] , jetsE[i] );
      particles_.push_back( ji );
      //cout << "j" << i << ": "; ji.Print();
    }
    for(auto p : particles_)
      HT += p.Pt();

    FoxWolfram fwam( particles_ );	
    std::vector< particleinfo*> allfoxwolfs = {&foxwolf1 , &foxwolf2 };
    for(uint ifw = 1 ; ifw < allfoxwolfs.size()+1 ; ifw++)
      allfoxwolfs[ifw-1]->set( fwam.getMoment( FoxWolfram::SHAT , ifw ),
			       fwam.getMoment( FoxWolfram::PT , ifw ),
			       fwam.getMoment( FoxWolfram::ETA , ifw ),
			       fwam.getMoment( FoxWolfram::PSUM , ifw ),
			       fwam.getMoment( FoxWolfram::PZ , ifw ),
			       fwam.getMoment( FoxWolfram::ONE , ifw ) );
    std::vector< math::RhoEtaPhiVector > particles;
    if( LeptonType != 4 )
      particles.push_back( math::RhoEtaPhiVector(lepton.pt, lepton.eta , lepton.phi) );

    particles.push_back( math::RhoEtaPhiVector(G1.eta, G1.phi , G1.other) );
    particles.push_back( math::RhoEtaPhiVector(G2.eta, G2.phi , G2.other) );
    for(unsigned int i = 0 ; i < jetsPhi.size() ; i++)
      particles.push_back( math::RhoEtaPhiVector( jetsPt[i] , jetsEta[i] , jetsPhi[i] ) );
    
    EventShapeVariables shapeVars(particles);
    eventshapes.set( shapeVars.aplanarity() ,
		     shapeVars.C() ,
		     shapeVars.circularity(),
		     shapeVars.D() ,
		     shapeVars.isotropy(),
		     shapeVars.sphericity() );
    
    
    if( nJets > 0 ){
      TLorentzVector bL,fwdJL;
      bL.SetPtEtaPhiE( jetsPt[0] , jetsEta[0] , jetsPhi[0] , jetsE[0] );
      
      SemiLepTopQuark singletop( bL , metL , muL , fwdJL, fwdJL );
      metL = singletop.getMET();

      TLorentzVector topRec = singletop.top() ;

      //"THInvM:THDPhi:THDR:"
      TVector3 hv3 = higgs.Vect();
      TVector3 tv3 = topRec.Vect();
      double costheta = tv3.Dot( hv3 )/ (tv3.Mag()*hv3.Mag()) ;

      TVector3 jprimev3;
      int jpIndex = oneB.index_forward;
      if( LeptonType == 4 )
	jpIndex = twoB.index_forward;
      jprimev3.SetPtEtaPhi( jetsPt[ jpIndex ] , 
			    jetsEta[ jpIndex ] ,
			    jetsPhi[ jpIndex ] );

      TVector3 htopcross = hv3.Cross( tv3 );
      double costhetajprime = htopcross.Dot( jprimev3 ) / ( htopcross.Mag() * jprimev3.Mag() );
      THReco.set( (topRec+higgs).M() , 
		  topRec.DeltaPhi( higgs ) , topRec.DrEtaPhi( higgs ) );

      //"THDEta:CosTheta:JPrime:WM:topM:CosThetaStar:nLoops/s:goodEvent/O"
      Top.set( topRec.Eta() - higgs.Eta() , costheta , costhetajprime ,
	       singletop.W().M() , topRec.M() , singletop.cosThetaStar() );

      Top.number = singletop.nLoopsToSolve;
      Top.isSet = singletop.goodEvent;
    }

    particles.emplace_back( metL.Pt() ,  metL.Eta() , metL.Phi() );

    EventShapeVariables shapeVars2(particles);
    eventshapesMet.set( shapeVars2.aplanarity() ,
			shapeVars2.C() ,
			shapeVars2.circularity(),
			shapeVars2.D() ,
			shapeVars2.isotropy(),
			shapeVars2.sphericity() );
    
    particles_.push_back(metL);
    FoxWolfram fwam2( particles_ );
    allfoxwolfs.clear();
    allfoxwolfs.push_back(&foxwolf1Met);
    allfoxwolfs.push_back(&foxwolf2Met);
    for(uint ifw = 1 ; ifw < allfoxwolfs.size()+1 ; ifw++)
      allfoxwolfs[ifw-1]->set( fwam2.getMoment( FoxWolfram::SHAT , ifw ),
			       fwam2.getMoment( FoxWolfram::PT , ifw ),
			       fwam2.getMoment( FoxWolfram::ETA , ifw ),
			       fwam2.getMoment( FoxWolfram::PSUM , ifw ),
			       fwam2.getMoment( FoxWolfram::PZ , ifw ),
			       fwam2.getMoment( FoxWolfram::ONE , ifw ) );
    
  }

  FillTree();
  return true;
}
