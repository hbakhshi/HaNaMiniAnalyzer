#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/BaseMiniAnalyzer.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"
#include <iostream>
#include "TROOT.h"
#include "TDirectory.h"

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

  unsigned int RunN;
  unsigned long long EventN;
  unsigned char SelectionStep;

  unsigned char nVertices, nJets, nbJets, nMuons, nGPairs , nSelGPairs ;
  struct particleinfo{
    float pt, eta, phi , other ; //other : for photon id, for diphoton mass, for jets btagging vals
    particleinfo( double pt_=-999, double eta_ =-999, double phi_=-999 , double other_ = -999 ){
      pt = pt_;
      eta= eta_;
      phi = phi_;
      other = other_;
    };
    void set(double pt_=-999, double eta_ =-999, double phi_=-999 , double other_ = -999 ){
      pt = pt_;
      eta= eta_;
      phi = phi_;
      other = other_;
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
  float puWeight , diGMVA , met , metPhi ;
  particleinfo G1 , G2 , DiG , mu , forwardJ , bJ , J3 ;
  void resetTreeVals(){
    RunN = 0;
    EventN = 0;
    SelectionStep = nVertices = nJets = nbJets = nMuons = nGPairs = nSelGPairs = 250;

    W = 1.0;
    for(unsigned int i=0 ; i < nHistos ; i++)
      Weight[i] = 1.0 ;

    puWeight = met = metPhi = -999;
    particleinfo tmp;
    G1 = G2 = DiG = mu = forwardJ = bJ = J3 =  tmp ;
  }

  TTree* theSelectionResultTree;
  unsigned int nHistos;
  bool MakeTree;


  Histograms* M_GG; //Histograms*  Eta_J; Histograms*  Pt_J ; Histograms*  Pt_Mu ; Histograms*  Eta_Mu; Histograms*  Pt_b ; Histograms*  Eta_b ; Histograms*  DEta_Jb ; Histograms*  DEta_bMu ;
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
}
// ------------ method called once each job just before starting event loop  ------------
void tHqAnalyzer::beginJob()
{
  if( SampleName == "Signal" )
    nHistos = 51;
  W = std::valarray<double>( 1.0 , nHistos);
  Weight = new float[nHistos];
  
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
    theSelectionResultTree->Branch("nbJets", &nbJets);
    theSelectionResultTree->Branch("nMuons", &nMuons);
    theSelectionResultTree->Branch("nGPairs", &nGPairs);
    theSelectionResultTree->Branch("nSelGPairs", &nSelGPairs);

    std::string weightLeafList = "W0";
    for(unsigned int iii = 1 ; iii < nHistos ; iii++)
      weightLeafList += (":W" + std::to_string(iii) );

    theSelectionResultTree->Branch("Weight", Weight , weightLeafList.c_str() );
    theSelectionResultTree->Branch("puWeight", &puWeight);
    theSelectionResultTree->Branch("diGMVA", &diGMVA);
    theSelectionResultTree->Branch("met", &met);
    theSelectionResultTree->Branch("metPhi", &metPhi);
    theSelectionResultTree->Branch("G1" , &G1 , "pt:eta:phi:other" );
    theSelectionResultTree->Branch("G2" , &G2 , "pt:eta:phi:other"  );
    theSelectionResultTree->Branch("DiG", &DiG , "pt:eta:phi:other"  );
    theSelectionResultTree->Branch("mu", &mu , "pt:eta:phi:other"  );
    theSelectionResultTree->Branch("forwardJ", &forwardJ , "pt:eta:phi:other" );
    theSelectionResultTree->Branch("bJ", &bJ, "pt:eta:phi:other" );
    theSelectionResultTree->Branch("J3", &J3 , "pt:eta:phi:other" );

    resetTreeVals();
  }

  hCutFlowTable = new Histograms( SampleName , "CutFlowTable" , 15 , 0.5 , 15.5 , nHistos );
  M_GG = new Histograms( SampleName , "M_GG" , 100 , 50 , 250 , nHistos );
  // Eta_J = new Histograms( SampleName , "Eta_J" , 24 , -4.7 , 4.7 , nHistos );
  // Pt_J  = new Histograms( SampleName , "Pt_J" , 27 , 20 , 200 , nHistos );
  // Pt_Mu  = new Histograms( SampleName , "Pt_Mu" , 27 , 20 , 200 , nHistos );
  // Eta_Mu = new Histograms( SampleName , "Eta_Mu" , 8 , 0 , 2.4 , nHistos );
  // Pt_b  = new Histograms( SampleName , "Pt_b" , 27 , 20 , 200 , nHistos );
  // Eta_b  = new Histograms( SampleName , "Eta_b" , 8 , 0 , 2.5 , nHistos );
  // DEta_Jb  = new Histograms( SampleName , "DEta_Jb" , 16 , 0 , 8 , nHistos );
  // DEta_bMu = new Histograms( SampleName , "DEta_bMu" , 16 , 0 , 8 , nHistos );
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
  
  if( geninfoReader )
    W *= geninfoReader->Read( iEvent );

  hCutFlowTable->Fill( ++SelectionStep , W );

  if( hltReader->Read( iEvent ) < 0 )
    return false;
  hCutFlowTable->Fill( ++SelectionStep , W );

  if( vertexReader->Read( iEvent ) < 0 )
    return false;
  W *= vertexReader->puWeight;
  puWeight = vertexReader->puWeight;
  nVertices = vertexReader->vtxMult;
  hCutFlowTable->Fill( ++SelectionStep , W );

  switch( diPhoton->read( iEvent ) ){
    case DiPhotonReader::Pass:
    case DiPhotonReader::PassMoreThanOne:
      W *= diPhoton->W();
      hCutFlowTable->Fill( ++SelectionStep , W );
      hCutFlowTable->Fill( ++SelectionStep , W );
      hCutFlowTable->Fill( ++SelectionStep , W );
      hCutFlowTable->Fill( ++SelectionStep , W );
      hCutFlowTable->Fill( ++SelectionStep , W );
      hCutFlowTable->Fill( ++SelectionStep , W );
      
      G1.set( diPhoton->diPhoton->leadingPhoton()->pt(),
	      diPhoton->diPhoton->leadingPhoton()->eta(),
	      diPhoton->diPhoton->leadingPhoton()->phi(),
	      diPhoton->diPhoton->leadingPhoton()->phoIdMvaDWrtVtx( diPhoton->diPhoton->vtx() ) );
      G2.set( diPhoton->diPhoton->subLeadingPhoton()->pt(),
	      diPhoton->diPhoton->subLeadingPhoton()->eta(),
	      diPhoton->diPhoton->subLeadingPhoton()->phi(),
	      diPhoton->diPhoton->subLeadingPhoton()->phoIdMvaDWrtVtx( diPhoton->diPhoton->vtx() ) );
      DiG.set( diPhoton->diPhoton->pt() ,
	       diPhoton->diPhoton->eta() ,
	       diPhoton->diPhoton->phi() ,
	       diPhoton->diPhoton->mass() );
      diGMVA = diPhoton->diGMVA;
      nGPairs = diPhoton->handle->size();
      nSelGPairs = diPhoton->nDiPhos ;
      break;
    case DiPhotonReader::InvMassFailed:
      hCutFlowTable->Fill( ++SelectionStep , W );
    case DiPhotonReader::MVAFailed:
      hCutFlowTable->Fill( ++SelectionStep , W );
    case DiPhotonReader::PhotonID:
      hCutFlowTable->Fill( ++SelectionStep , W );
    case DiPhotonReader::SubLeadingPt:
      hCutFlowTable->Fill( ++SelectionStep , W );
    case DiPhotonReader::LeadingPt:
      hCutFlowTable->Fill( ++SelectionStep , W );
      G1.set( diPhoton->lPt, diPhoton->lEta , diPhoton->lPhi , diPhoton->lMVA );
      G2.set( diPhoton->slPt, diPhoton->slEta , diPhoton->slPhi , diPhoton->slMVA );
      DiG.other = diPhoton->diGMass;
      diGMVA = diPhoton->diGMVA;
    case DiPhotonReader::ZeroPairs:
      nGPairs = diPhoton->handle->size();
      nSelGPairs = 0 ;

      FillTree();
      return false;
  }
    
  M_GG->Fill( diPhoton->diPhoton->mass() , W );

  switch( flashggmuonreader->Read( iEvent , diPhoton->diPhoton ) ){
  case flashggMuonReader::ExactlyOne :
    W *= (flashggmuonreader->W);
    hCutFlowTable->Fill( ++SelectionStep , W );
    hCutFlowTable->Fill( ++SelectionStep , W );

    mu.set( flashggmuonreader->goodMus[0].pt() ,
	    flashggmuonreader->goodMus[0].eta() ,
	    flashggmuonreader->goodMus[0].phi() ,
	    flashggmuonreader->Iso );
    nMuons = 1;
    break;
  case flashggMuonReader::MoreThanOne :
    hCutFlowTable->Fill( ++SelectionStep , W );
  case flashggMuonReader::ExactlyOneNonIso :
    W *= (flashggmuonreader->W);
    mu.set( flashggmuonreader->goodMus[0].pt() ,
	    flashggmuonreader->goodMus[0].eta() ,
	    flashggmuonreader->goodMus[0].phi() ,
	    flashggmuonreader->Iso );
  case flashggMuonReader::ZeroMuons :
    nMuons = flashggmuonreader->nMuons ;
    FillTree();
    return true;
  }

  // Eta_Mu->Fill( fabs( flashggmuonreader->goodMus[0].eta() ) , W );
  // Pt_Mu->Fill( flashggmuonreader->goodMus[0].pt() , W );


  switch( flashggjetreader->Read( iEvent , diPhoton->diPhoton , &(flashggmuonreader->goodMus[0]) ) ){
  case flashggJetReader::Pass:
    W *= flashggjetreader->W ;
    hCutFlowTable->Fill( ++SelectionStep , W );
    hCutFlowTable->Fill( ++SelectionStep , W );

    nJets = flashggjetreader->selectedJets.size();
    nbJets = flashggjetreader->selectedBJets.size();

    break;
  case flashggJetReader::NotEnoughBJets:
    hCutFlowTable->Fill( ++SelectionStep , W );
  case flashggJetReader::NotEnoughJets:
    nJets = flashggjetreader->selectedJets.size();
    nbJets = flashggjetreader->selectedBJets.size();
    FillTree();
    return true;
  }


  const flashgg::Jet* bJet = &(flashggjetreader->selectedBJets[0]) ;
  bJ.set( bJet->pt() , bJet->eta() , bJet->phi() , bJet->bDiscriminator( flashggjetreader->BTagAlgo ) );

  //forward jet is set when Get3rdJet method is called
  const flashgg::Jet* Jet3 = flashggjetreader->Get3rdJet() ;
  if( Jet3 )
    J3.set( Jet3->pt() , Jet3->eta() , Jet3->phi() , Jet3->bDiscriminator( flashggjetreader->BTagAlgo ) );

  const flashgg::Jet* forwardJet = flashggjetreader->forwardJet;
  forwardJ.set( forwardJet->pt() , forwardJet->eta() , forwardJet->phi() , forwardJet->bDiscriminator( flashggjetreader->BTagAlgo ) );

  // Pt_b->Fill( flashggjetreader->selectedBJets[0].pt()  , W );
  // Eta_b->Fill( fabs( flashggjetreader->selectedBJets[0].eta() )  , W );

  // DEta_Jb->Fill( fabs( flashggjetreader->selectedBJets[0].eta()-firstJet.eta() ) , W );


  // DEta_bMu->Fill( fabs( flashggmuonreader->goodMus[0].eta() -  flashggjetreader->selectedBJets[0].eta() ) , W );

  if( metReader->Read(iEvent) < 0 ){
    met = metReader->met.pt();
    metPhi = metReader->met.phi();

    FillTree();
    return true;
  }
  hCutFlowTable->Fill( ++SelectionStep , W );

  met = metReader->met.pt();
  metPhi = metReader->met.phi();
  FillTree();

  return true;
}
