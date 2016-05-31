#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/HaNaBaseMiniAnalyzer.h"

#include <iostream>

using namespace std;

class TTHAnalyzer : public HaNaBaseMiniAnalyzer{
public:
  explicit TTHAnalyzer(const edm::ParameterSet&);
  ~TTHAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions){ HaNaBaseMiniAnalyzer::fillDescriptions( descriptions ); }
protected:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
};

DEFINE_FWK_MODULE(TTHAnalyzer);

TTHAnalyzer::~TTHAnalyzer() {}
TTHAnalyzer::TTHAnalyzer( const edm::ParameterSet& ps ) :
  HaNaBaseMiniAnalyzer( ps ) 
{
}
// ------------ method called once each job just before starting event loop  ------------
void TTHAnalyzer::beginJob()
{
  hCutFlowTable = new Histograms( SampleName , "CutFlowTable" , 10 , 0.5 , 10.5 );
}

//
void TTHAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  W = 1.0;
  stepEventSelection = 0;
  
  if( LHEReader )
    W *= LHEReader->Read( iEvent );

  hCutFlowTable->Fill( ++stepEventSelection , W );

  if( hltReader->Read( iEvent ) < 0 )
    return;
  hCutFlowTable->Fill( ++stepEventSelection , W );

  if( vertexReader->Read( iEvent ) < 0 )
    return;
  W *= vertexReader->puWeight;
  hCutFlowTable->Fill( ++stepEventSelection , W );

  //cout << vertexReader->PV()->ndof() << endl;
  switch( diMuReader->Read( iEvent , vertexReader->PV() ) ){
  case DiMuonReader::Pass :
    W *= (diMuReader->W) ;
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    break;
  case DiMuonReader::UnderTheZPeak:
    W *= (diMuReader->W) ;
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiMuonReader::LowMassPair:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiMuonReader::NoPairWithChargeReq:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiMuonReader::LessThan2Muons :
    return ;
  }
  
  if( metReader->Read(iEvent 
		      /*, jetReader->GetAllJets()*/) < 0 )
    //uncomment the inner part if JES changes wrt the oldjets collection wants to be applied on met , it should be called after reading jets
    return;
  hCutFlowTable->Fill( ++stepEventSelection , W );

  switch( jetReader->Read( iEvent , &(diMuReader->DiMuon) ) ){
  case JetReader::Pass:
    W *= jetReader->W ;
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    break;
  case JetReader::NotEnoughBJets:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case JetReader::NotEnoughJets:
    return;
  }
}
