#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/DiPhotonReader.h"

using namespace edm;
using namespace pat;

DiPhotonReader::DiPhotonReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC , bool isData , string SetupDir) :
  BaseEventReader< View<DiPhotonCandidate> >( iConfig , &iC ),
  mvaResult( iConfig.getParameter<ParameterSet>( "mvaResults" ) , &iC ),
  leadPhoOverMassThreshold_ ( iConfig.getParameter<double>( "leadPhoOverMassThreshold") ),
  subleadPhoOverMassThreshold_ ( iConfig.getParameter<double>( "subleadPhoOverMassThreshold") ),
  MVAThreshold_ ( iConfig.getParameter<double>( "MVAThreshold") ),
  PhoMVAThreshold_ ( iConfig.getParameter<double>( "PhoMVAThreshold") ),
  InvMassCut(  iConfig.getParameter<double>( "InvMassCut") ),
  IsData(isData)
{
}

DiPhotonReader::SelectionStatus DiPhotonReader::read( const edm::Event& iEvent ){ 
  BaseEventReader< View<DiPhotonCandidate> >::Read( iEvent );
  mvaResult.Read( iEvent );

  assert( handle->size() == mvaResult.handle->size() );
  diPhotons.clear();
  assert( diPhotons.size() == 0 );

  for(  unsigned int diphoIndex = 0; diphoIndex < handle->size(); diphoIndex++ ) {
    edm::Ptr<flashgg::DiPhotonCandidate> dipho = handle->ptrAt( diphoIndex );
    edm::Ptr<flashgg::DiPhotonMVAResult> mvares = mvaResult.handle->ptrAt( diphoIndex );

    diPhotons.push_back( diPhotonInfo( dipho , mvares , leadPhoOverMassThreshold_ ,
				       subleadPhoOverMassThreshold_ , MVAThreshold_ , PhoMVAThreshold_ , InvMassCut ) );
  }

  diPhoton = NULL;
  int selectedIndex = -1;
  nSelGPairs = 0;
  DiPhotonReader::SelectionStatus ret = diPhotons.status( selectedIndex , nSelGPairs ) ;
  if( ret > DiPhotonReader::ZeroPairs ){
    diPhoton = diPhotons.at( selectedIndex ).diPhoton ;
    theSelected = &(diPhotons.at( selectedIndex ));
  }

  return ret;
}
