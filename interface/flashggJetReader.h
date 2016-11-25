#ifndef flashggJetReader_H
#define flashggJetReader_H

#include "BTagWeight.h"
#include "BaseEventReader.h"
#include "flashgg/DataFormats/interface/Jet.h"
#include "flashgg/DataFormats/interface/Muon.h"
#include "JetMETCorrections/Modules/interface/JetResolution.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "flashgg/DataFormats/interface/DiPhotonCandidate.h"

#include "TRandom3.h"

#include <algorithm>
#include <vector>

using namespace std;
using namespace edm;
using namespace pat;
using namespace flashgg;


class flashggJetReader : public BaseEventReader< flashggJetCollection > {
public:
  std::vector< edm::EDGetTokenT< flashggJetCollection > > all_tokens ;

  flashggJetReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC , bool isData , string SetupDir) ;
  const flashggJetCollection* GetAllJets();

  int GetJetbSorted(int index){
    return bVals[index].second ;
  };
  int GetJetEtaSortedIndex(int index ){
    for(unsigned int i = 0 ; i < selectedJets.size() ; i++)
      if( etaVals[i].second == index )
	return i ;

    return -1;
  };
  int GetJetPtSortedIndex(int index ){
    for(unsigned int i = 0 ; i < selectedJets.size() ; i++)
      if( ptVals[i].second == index )
	return i ;

    return -1;
  };

  enum SelectionStatus {
    NotEnoughJets,
    NotEnoughBJets,
    Pass
  };

  SelectionStatus Read( const edm::Event& iEvent , const DiPhotonCandidate* diPhoton , std::vector<const flashgg::Jet* > toRemove = {}  ); //, const flashgg::Muon* mu);


  std::vector< std::pair<double , int> > bVals, etaVals , ptVals ;

  flashggJetCollection selectedJetsEtaLT24;
  flashggJetCollection selectedJets;
  //flashggJetCollection selectedBJets;

  char nLB, nMB, nTB;
  float W0L , W0M, W0T , W1L , W1M , W1M0L , W1T , W1T0L, W1T0M , W2L , W2M , W2T;
  void getAllWs(float* ptr){
    float ret[] = {W0L , W0M, W0T , W1L , W1M , W1M0L , W1T , W1T0L, W1T0M , W2L , W2M , W2T};
    for(unsigned int i = 0 ; i < 12 ; i++)
      ptr[i] = ret[i] ;
  };
  vector<float*> allWs;
private :
  BTagWeight *btw0L , *btw0M, *btw0T , *btw1L , *btw1M , *btw1M0L , *btw1T , *btw1T0L, *btw1T0M , *btw2L , *btw2M , *btw2T; 
  vector<BTagWeight*> allBTWs;

  bool IsData;
  /* JET SELECTION PARAMS */
  bool ApplyJER;
  double JetPtCut , JetEtaCut ;
  //unsigned int MinNJets;
  /* JET SELECTION PARAMS */


  /* b-JET SELECTION PARAMS */
  double BTagWPL , BTagWPM , BTagWPT ; // , BTagCut ;
  //std::vector<int> BTagCuts; // atm only 2 are accepted, first for selection, second for veto
public:
  bool doBStudies ;
  string BTagAlgo ;
private:
  //unsigned int MinNBJets ;
  /* b-JET SELECTION PARAMS */

  /* JET TOOLS */
  JME::JetResolution resolution;
  JME::JetResolutionScaleFactor resolution_sf;
  TRandom3* rndJER;

  float JER( flashgg::Jet jet , double rho , int syst = 0 );
  bool JetLooseID( flashgg::Jet j );
  /* JET TOOLS */

  edm::EDGetTokenT<double> t_Rho_;
  edm::Handle<double> rho;
  double Rho;
};

#endif
