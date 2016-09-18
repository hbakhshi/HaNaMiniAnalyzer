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

  nDiPhos = 0;
  DiPhotonReader::SelectionStatus ret = ZeroPairs;

  double maxSumPt = 0;
  double sumPt = 0;

  diPhoton = NULL;
  MVA = lPt = lEta = lPhi = slPt = slEta = slPhi = lMVA = slMVA = diGMVA = diGMass = -1000.0;
  for(  unsigned int diphoIndex = 0; diphoIndex < handle->size(); diphoIndex++ ) {
    edm::Ptr<flashgg::DiPhotonCandidate> dipho = handle->ptrAt( diphoIndex );
    edm::Ptr<flashgg::DiPhotonMVAResult> mvares = mvaResult.handle->ptrAt( diphoIndex );

    lPt  = dipho->leadingPhoton()->pt();
    lEta = dipho->leadingPhoton()->eta();
    lPhi = dipho->leadingPhoton()->phi();

    slPt = dipho->subLeadingPhoton()->pt();
    slEta= dipho->subLeadingPhoton()->eta();
    slPhi= dipho->subLeadingPhoton()->phi();

    sumPt = lPt+slPt ;

    lMVA = dipho->leadingPhoton()->phoIdMvaDWrtVtx( dipho->vtx() );
    slMVA = dipho->subLeadingPhoton()->phoIdMvaDWrtVtx( dipho->vtx() );

    diGMVA = mvares->result;
    diGMass = dipho->mass();

    if( ( lPt / diGMass ) < leadPhoOverMassThreshold_ ) {if(ret<LeadingPt) ret = LeadingPt ; continue; }
    if( ( slPt / diGMass ) < subleadPhoOverMassThreshold_ ) { if(ret<SubLeadingPt) ret = SubLeadingPt ;continue; }
    
    if( lMVA < PhoMVAThreshold_ || lMVA < PhoMVAThreshold_ ) { if(ret<PhotonID) ret = PhotonID ;continue; }
    if( diGMVA < MVAThreshold_ ) { if(ret<MVAFailed) ret = MVAFailed ;continue; }
    if( diGMass < InvMassCut ) { if( ret < InvMassFailed ) ret = InvMassFailed ; continue ; }
    nDiPhos ++;
    if( sumPt > maxSumPt ){
      diPhoton = dipho.get();
      maxSumPt = sumPt ;
      ret = Pass;
    }
  }

  if( nDiPhos == 0 ){
    return ret;
  }
  else if( nDiPhos == 1 ){
    return Pass;
  }
  else 
    return PassMoreThanOne;
}
