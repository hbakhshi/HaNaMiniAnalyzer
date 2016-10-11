#ifndef DiPhotonReader_H
#define DiPhotonReader_H

#include "BaseEventReader.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "flashgg/DataFormats/interface/DiPhotonCandidate.h"
#include "flashgg/DataFormats/interface/DiPhotonMVAResult.h"

#include <vector>

#include "TH2.h"
#include "TROOT.h"
#include "TFile.h"

using namespace std;
using namespace edm;
using namespace flashgg;

class DiPhotonReader : public BaseEventReader< edm::View<DiPhotonCandidate> > {
public:
  DiPhotonReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC , bool isData , string SetupDir);
  enum SelectionStatus{
    ZeroPairs = 0,
    LeadingCuts = 1,
    SubLeadingCuts = 2,
    PairCuts = 3,
    Pass = 4,
    PassMoreThanOne = 5
  };
  SelectionStatus read( const edm::Event& iEvent );
  const DiPhotonCandidate* diPhoton;
 
  struct diPhotonInfo {
  public:
    double leadPhoOverMassThreshold_;
    double subleadPhoOverMassThreshold_;
    double MVAThreshold_;
    double PhoMVAThreshold_;
    double InvMassCut;

    double lPt , lEta, lPhi , slPt , slEta , slPhi , lMVA, slMVA , diGMVA , diGMass , sumPt ;
    const DiPhotonCandidate* diPhoton;
    diPhotonInfo( edm::Ptr<flashgg::DiPhotonCandidate> dipho  , edm::Ptr<flashgg::DiPhotonMVAResult> mvares ,   double _leadPhoOverMassThreshold_ ,
		  double _subleadPhoOverMassThreshold_,  double _MVAThreshold_,  double _PhoMVAThreshold_,  double _InvMassCut ){
      diPhoton = dipho.get();
      
      lPt  = dipho->leadingPhoton()->pt();
      lEta = dipho->leadingPhoton()->eta();
      lPhi = dipho->leadingPhoton()->phi();

      slPt = dipho->subLeadingPhoton()->pt();
      slEta= dipho->subLeadingPhoton()->eta();
      slPhi= dipho->subLeadingPhoton()->phi();

      sumPt = lPt+slPt ;

      lMVA = dipho->leadingPhoton()->phoIdMvaDWrtVtx( dipho->vtx() );
      slMVA = dipho->subLeadingPhoton()->phoIdMvaDWrtVtx( dipho->vtx() );

      diGMass = dipho->mass();
      diGMVA = mvares->result;

      leadPhoOverMassThreshold_ = _leadPhoOverMassThreshold_;    
      subleadPhoOverMassThreshold_ = _subleadPhoOverMassThreshold_; 
      MVAThreshold_ =  _MVAThreshold_;		    
      PhoMVAThreshold_ = _PhoMVAThreshold_;		    
      InvMassCut = _InvMassCut;                   
    };
    DiPhotonReader::SelectionStatus status(){
      if( ( lPt < (leadPhoOverMassThreshold_*diGMass) )
	  || (lMVA < PhoMVAThreshold_ ) )
	return DiPhotonReader::LeadingCuts;

      if(  (slPt < (subleadPhoOverMassThreshold_*diGMass ) )
	   || ( slMVA < PhoMVAThreshold_ ) )
	return DiPhotonReader::SubLeadingCuts;

      if(  diGMVA < MVAThreshold_ 
	   || diGMass < InvMassCut )
	return DiPhotonReader::PairCuts;

      return DiPhotonReader::Pass;
    };
  };
  class DiPhotons : public std::vector<diPhotonInfo> {
  public:
    DiPhotons(){};

    DiPhotonReader::SelectionStatus status(int& selectedIndex , int& nSelecteds){
      selectedIndex = -1 ;
      if( this->size() == 0 )
	return DiPhotonReader::ZeroPairs;

      DiPhotonReader::SelectionStatus lastStat = DiPhotonReader::ZeroPairs;
      double lastSumPt = 0;
      nSelecteds = 0;

      for( unsigned int index = 0 ; index < this->size() ; index++ ){
	diPhotonInfo pair = this->at( index );
	DiPhotonReader::SelectionStatus pairStat = pair.status();
	if( pairStat > lastStat ){
	  lastStat = pairStat;
	  lastSumPt = pair.sumPt ;
	  selectedIndex = index ;
	}else if(pairStat == lastStat ){
	  if( lastSumPt < pair.sumPt ){
	    lastSumPt = pair.sumPt;
	    selectedIndex = index ;
	  }
	}

	if( pairStat == DiPhotonReader::Pass )
	  nSelecteds ++ ;
      }

      if( nSelecteds == 0 )
	return lastStat ;
      else if( nSelecteds == 1 ){
	if( lastStat != DiPhotonReader::Pass )
	  cout << "inconsistent lastStat value" << endl;
	return lastStat ; 
      }else {
	return DiPhotonReader::PassMoreThanOne;
      }
    };

  };
  int nSelGPairs;
  DiPhotons diPhotons;
  diPhotonInfo* theSelected;
  int JetsIndex(){return diPhoton->jetCollectionIndex();};
  double W(){return diPhoton->centralWeight();};
private :
  BaseEventReader< View<DiPhotonMVAResult> > mvaResult;

  double leadPhoOverMassThreshold_;
  double subleadPhoOverMassThreshold_;
  double MVAThreshold_;
  double PhoMVAThreshold_;
  double InvMassCut;
  bool IsData;
};
#endif
