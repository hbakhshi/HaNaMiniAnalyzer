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
  IsData(isData)
{
}

DiPhotonReader::SelectionStatus DiPhotonReader::read( const edm::Event& iEvent ){ 
  BaseEventReader< View<DiPhotonCandidate> >::Read( iEvent );
  mvaResult.Read( iEvent );

  assert( handle->size() == mvaResult.handle->size() );

  int nDiPhos = 0;
  DiPhotonReader::SelectionStatus ret = ZeroPairs;

  diPhoton = NULL;
  MVA = -1000;
  for(  unsigned int diphoIndex = 0; diphoIndex < handle->size(); diphoIndex++ ) {
    edm::Ptr<flashgg::DiPhotonCandidate> dipho = handle->ptrAt( diphoIndex );
    edm::Ptr<flashgg::DiPhotonMVAResult> mvares = mvaResult.handle->ptrAt( diphoIndex );

    if( dipho->leadingPhoton()->pt() < ( dipho->mass() )*leadPhoOverMassThreshold_ ) {if(ret<LeadingPt) ret = LeadingPt ; continue; }
    if( dipho->subLeadingPhoton()->pt() < ( dipho->mass() )*subleadPhoOverMassThreshold_ ) { if(ret<SubLeadingPt) ret = SubLeadingPt ;continue; }
    
    double idmva1 = dipho->leadingPhoton()->phoIdMvaDWrtVtx( dipho->vtx() );
    double idmva2 = dipho->subLeadingPhoton()->phoIdMvaDWrtVtx( dipho->vtx() );
    if( idmva1 < PhoMVAThreshold_ || idmva2 < PhoMVAThreshold_ ) { if(ret<PhotonID) ret = PhotonID ;continue; }
    if( mvares->result < MVAThreshold_ ) { if(ret<MVAFailed) ret = MVAFailed ;continue; }
    
    nDiPhos ++;
    if( mvares->result > MVA ){
      diPhoton = dipho.get();
      MVA = mvares->result ;
      ret = Pass;
    }
  }

  if( nDiPhos == 0 )
    return ret;
  else if( nDiPhos == 1 )
    return Pass;
  else 
    return PassMoreThanOne;
}
