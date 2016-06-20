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
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  unsigned int RunN;
  unsigned long long EventN;
  unsigned char SelectionStep;
  TTree* theSelectionResultTree;
  int nHistos;
  bool MakeTree;


  Histograms* M_GG; Histograms*  Eta_J; Histograms*  Pt_J ; Histograms*  Pt_Mu ; Histograms*  Eta_Mu; Histograms*  Pt_b ; Histograms*  Eta_b ; Histograms*  DEta_Jb ; Histograms*  DEta_bMu ;
};

DEFINE_FWK_MODULE(tHqAnalyzer);

tHqAnalyzer::~tHqAnalyzer() {}
tHqAnalyzer::tHqAnalyzer( const edm::ParameterSet& ps ) :
  BaseMiniAnalyzer( ps ),
  theSelectionResultTree( NULL ),
  nHistos(1),
  MakeTree( ps.getParameter<bool>( "StoreEventNumbers" ) )
{
}
// ------------ method called once each job just before starting event loop  ------------
void tHqAnalyzer::beginJob()
{
  if( SampleName == "Signal" )
    nHistos = 51;
  
  if( MakeTree ){
    edm::Service<TFileService> fs;
    //fs->cd();
    TFileDirectory treeDir = fs->mkdir( "Trees" );
    //treeDir.cd();

    // TFile* f = TFile::Open("tree.root" , "RECREATE");
    // f->cd();
    gDirectory->Print();
    theSelectionResultTree = treeDir.make<TTree>("SelectedEventNumbers" , "SelectedEventNumbers");
      //fs->make<TTree>("SelectedEventNumbers" , "SelectedEventNumbers");
    
    gDirectory->Print();
    theSelectionResultTree->Branch("EventNumber", &EventN );
    theSelectionResultTree->Branch("RunNumber", &RunN );
    theSelectionResultTree->Branch("SelectionStep", &SelectionStep );
  }

  hCutFlowTable = new Histograms( SampleName , "CutFlowTable" , 15 , 0.5 , 15.5 , nHistos );
  M_GG = new Histograms( SampleName , "M_GG" , 100 , 50 , 250 , nHistos );
  Eta_J = new Histograms( SampleName , "Eta_J" , 24 , -4.7 , 4.7 , nHistos );
  Pt_J  = new Histograms( SampleName , "Pt_J" , 27 , 20 , 200 , nHistos );
  Pt_Mu  = new Histograms( SampleName , "Pt_Mu" , 27 , 20 , 200 , nHistos );
  Eta_Mu = new Histograms( SampleName , "Eta_Mu" , 8 , 0 , 2.4 , nHistos );
  Pt_b  = new Histograms( SampleName , "Pt_b" , 27 , 20 , 200 , nHistos );
  Eta_b  = new Histograms( SampleName , "Eta_b" , 8 , 0 , 2.5 , nHistos );
  DEta_Jb  = new Histograms( SampleName , "DEta_Jb" , 16 , 0 , 8 , nHistos );
  DEta_bMu = new Histograms( SampleName , "DEta_bMu" , 16 , 0 , 8 , nHistos );
}

//
void tHqAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  EventN = iEvent.eventAuxiliary().event() ;
  RunN = iEvent.eventAuxiliary().run() ;

  std::valarray<double> W( 1.0 , 1);
  if( nHistos > 1 && SampleName == "Signal" ) {
    LHEReader->Read( iEvent );
    W = LHEReader->ExtractWeightsInRange( 446 , 495 ); 
  }
  SelectionStep = 0;
  
  if( geninfoReader )
    W *= geninfoReader->Read( iEvent );

  hCutFlowTable->Fill( ++SelectionStep , W );

  if( hltReader->Read( iEvent ) < 0 )
    return;
  hCutFlowTable->Fill( ++SelectionStep , W );

  if( vertexReader->Read( iEvent ) < 0 )
    return;
  W *= vertexReader->puWeight;
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
    break;
  case DiPhotonReader::MVAFailed:
    hCutFlowTable->Fill( ++SelectionStep , W );
  case DiPhotonReader::PhotonID:
    hCutFlowTable->Fill( ++SelectionStep , W );
  case DiPhotonReader::SubLeadingPt:
    hCutFlowTable->Fill( ++SelectionStep , W );
  case DiPhotonReader::LeadingPt:
    hCutFlowTable->Fill( ++SelectionStep , W );
  case DiPhotonReader::ZeroPairs:
    if(MakeTree) theSelectionResultTree->Fill();
    return;
  }

  M_GG->Fill( diPhoton->diPhoton->mass() , W );

  switch( flashggjetreader->Read( iEvent , diPhoton->diPhoton ) ){
  case flashggJetReader::Pass:
    W *= flashggjetreader->W ;
    hCutFlowTable->Fill( ++SelectionStep , W );
    hCutFlowTable->Fill( ++SelectionStep , W );
    break;
  case flashggJetReader::NotEnoughBJets:
    hCutFlowTable->Fill( ++SelectionStep , W );
  case flashggJetReader::NotEnoughJets:
    if(MakeTree) theSelectionResultTree->Fill();
    return;
  }

  
  Pt_b->Fill( flashggjetreader->selectedBJets[0].pt()  , W );
  Eta_b->Fill( fabs( flashggjetreader->selectedBJets[0].eta() )  , W );

  flashgg::Jet firstJet ;
  for( unsigned int i = 0 ; i < flashggjetreader->selectedJets.size() ; i++){
    flashgg::Jet jjj = flashggjetreader->selectedJets[i] ;
    double minDr = 1000000;
    for( unsigned int ib = 0 ; ib < i+1 ; ib++ ){
      double dr = reco::deltaR( jjj.p4() , flashggjetreader->selectedBJets[ib].p4() );
      if( dr < minDr )
	minDr = dr ;
    }
    if( minDr != 0. ){
      firstJet = jjj;
      break;
    }
  }
  Pt_J->Fill( firstJet.pt() , W ) ;
  Eta_J->Fill( firstJet.eta() , W );
  DEta_Jb->Fill( fabs( flashggjetreader->selectedBJets[0].eta()-firstJet.eta() ) , W );

  switch( flashggmuonreader->Read( iEvent , diPhoton->diPhoton ) ){
  case flashggMuonReader::ExactlyOne :
    W *= (flashggmuonreader->W);
    hCutFlowTable->Fill( ++SelectionStep , W );
    hCutFlowTable->Fill( ++SelectionStep , W );
    break;
  case flashggMuonReader::MoreThanOne :
    hCutFlowTable->Fill( ++SelectionStep , W );
  case flashggMuonReader::ZeroMuons :
    if(MakeTree) theSelectionResultTree->Fill();
    return;
  }

  Eta_Mu->Fill( fabs( flashggmuonreader->goodMus[0].eta() ) , W );
  Pt_Mu->Fill( flashggmuonreader->goodMus[0].pt() , W );
  DEta_bMu->Fill( fabs( flashggmuonreader->goodMus[0].eta() -  flashggjetreader->selectedBJets[0].eta() ) , W );

  if( metReader->Read(iEvent 
		      /*, jetReader->GetAllJets()*/) < 0 ){
    //uncomment the inner part if JES changes wrt the oldjets collection wants to be applied on met , it should be called after reading jets
    if(MakeTree) theSelectionResultTree->Fill();
    return;
  }
  hCutFlowTable->Fill( ++SelectionStep , W );
}
