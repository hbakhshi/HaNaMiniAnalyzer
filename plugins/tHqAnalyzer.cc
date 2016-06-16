#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/BaseMiniAnalyzer.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"
#include <iostream>

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

  UIntReader lumiNumber, runNumber;
  LIntReader eventNumber;
  unsigned int LumiN,RunN;
  unsigned long long EventN;
  unsigned char SelectionStep;
  TTree* theSelectionResultTree;
  int nHistos;
};

DEFINE_FWK_MODULE(tHqAnalyzer);

tHqAnalyzer::~tHqAnalyzer() {}
tHqAnalyzer::tHqAnalyzer( const edm::ParameterSet& ps ) :
  BaseMiniAnalyzer( ps ),
  lumiNumber( "lumiBlock" , consumesCollector() ),
  runNumber( "runNumber" , consumesCollector() ),
  eventNumber( "eventNumber" , consumesCollector() ),
  theSelectionResultTree( NULL ),
  nHistos(1)
{
  if( ps.getParameter<bool>( "StoreEventNumbers" ) ){
    edm::Service<TFileService> fs;
    theSelectionResultTree = fs->make<TTree>("SelectedEventNumbers" , "SelectedEventNumbers");
    theSelectionResultTree->Branch("EventNumber", &EventN );
    theSelectionResultTree->Branch("RunNumber", &RunN );
    theSelectionResultTree->Branch("SelectionStep", &SelectionStep );
  }
}
// ------------ method called once each job just before starting event loop  ------------
void tHqAnalyzer::beginJob()
{
  if( SampleName == "Signal" )
    nHistos = 51;
  
  hCutFlowTable = new Histograms( SampleName , "CutFlowTable" , 15 , 0.5 , 15.5 , nHistos );
}

//
void tHqAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  EventN = eventNumber.read( iEvent );
  RunN = runNumber.read( iEvent );

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
    theSelectionResultTree->Fill();
    return;
  }

  switch( flashggjetreader->Read( iEvent , diPhoton->diPhoton ) ){
  case flashggJetReader::Pass:
    W *= flashggjetreader->W ;
    hCutFlowTable->Fill( ++SelectionStep , W );
    hCutFlowTable->Fill( ++SelectionStep , W );
    break;
  case flashggJetReader::NotEnoughBJets:
    hCutFlowTable->Fill( ++SelectionStep , W );
  case flashggJetReader::NotEnoughJets:
    theSelectionResultTree->Fill();
    return;
  }

  switch( flashggmuonreader->Read( iEvent , diPhoton->diPhoton ) ){
  case flashggMuonReader::ExactlyOne :
    W *= (flashggmuonreader->W);
    hCutFlowTable->Fill( ++SelectionStep , W );
    hCutFlowTable->Fill( ++SelectionStep , W );
    break;
  case flashggMuonReader::MoreThanOne :
    hCutFlowTable->Fill( ++SelectionStep , W );
  case flashggMuonReader::ZeroMuons :
    theSelectionResultTree->Fill();
    return;
  }
  
  if( metReader->Read(iEvent 
		      /*, jetReader->GetAllJets()*/) < 0 ){
    //uncomment the inner part if JES changes wrt the oldjets collection wants to be applied on met , it should be called after reading jets
    theSelectionResultTree->Fill();
    return;
  }
  hCutFlowTable->Fill( ++SelectionStep , W );
}
