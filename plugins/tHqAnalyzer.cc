#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/BaseMiniAnalyzer.h"

#include <iostream>

using namespace std;

class tHqAnalyzer : public BaseMiniAnalyzer{
public:
  explicit tHqAnalyzer(const edm::ParameterSet&);
  ~tHqAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions){ BaseMiniAnalyzer::fillDescriptions( descriptions ); }
protected:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
};

DEFINE_FWK_MODULE(tHqAnalyzer);

tHqAnalyzer::~tHqAnalyzer() {}
tHqAnalyzer::tHqAnalyzer( const edm::ParameterSet& ps ) :
  BaseMiniAnalyzer( ps ) 
{
}
// ------------ method called once each job just before starting event loop  ------------
void tHqAnalyzer::beginJob()
{
  hCutFlowTable = new Histograms( SampleName , "CutFlowTable" , 15 , 0.5 , 15.5 );
}

//
void tHqAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  W = 1.0;
  stepEventSelection = 0;
  
  if( geninfoReader )
    W *= geninfoReader->Read( iEvent );

  hCutFlowTable->Fill( ++stepEventSelection , W );

  if( hltReader->Read( iEvent ) < 0 )
    return;
  hCutFlowTable->Fill( ++stepEventSelection , W );

  if( vertexReader->Read( iEvent ) < 0 )
    return;
  W *= vertexReader->puWeight;
  hCutFlowTable->Fill( ++stepEventSelection , W );

  switch( diPhoton->read( iEvent ) ){
  case DiPhotonReader::Pass:
  case DiPhotonReader::PassMoreThanOne:
    W *= diPhoton->W();
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    break;
  case DiPhotonReader::MVAFailed:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiPhotonReader::PhotonID:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiPhotonReader::SubLeadingPt:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiPhotonReader::LeadingPt:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiPhotonReader::ZeroPairs:
    return;
  }

  switch( flashggjetreader->Read( iEvent , diPhoton->diPhoton ) ){
  case flashggJetReader::Pass:
    W *= flashggjetreader->W ;
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    break;
  case flashggJetReader::NotEnoughBJets:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case flashggJetReader::NotEnoughJets:
    return;
  }

  switch( flashggmuonreader->Read( iEvent , diPhoton->diPhoton ) ){
  case flashggMuonReader::ExactlyOne :
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    break;
  case flashggMuonReader::MoreThanOne :
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case flashggMuonReader::ZeroMuons :
    return;
  }
  
  if( metReader->Read(iEvent 
		      /*, jetReader->GetAllJets()*/) < 0 )
    //uncomment the inner part if JES changes wrt the oldjets collection wants to be applied on met , it should be called after reading jets
    return;
  hCutFlowTable->Fill( ++stepEventSelection , W );
}
