#ifndef flashggJetReader_H
#define flashggJetReader_H

#include "BTagWeight.h"
#include "BaseEventReader.h"
#include "flashgg/DataFormats/interface/Jet.h"
#include "JetMETCorrections/Modules/interface/JetResolution.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "flashgg/DataFormats/interface/DiPhotonCandidate.h"

#include "TRandom3.h"

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

  enum SelectionStatus {
    NotEnoughJets,
    NotEnoughBJets,
    Pass
  };

  SelectionStatus Read( const edm::Event& iEvent , const DiPhotonCandidate* diPhoton);

  flashggJetCollection selectedJets;
  flashggJetCollection selectedBJets;
  double W;
private :
  BTagWeight* btw; 

  bool IsData;
  /* JET SELECTION PARAMS */
  bool ApplyJER;
  double JetPtCut , JetEtaCut ;
  unsigned int MinNJets;
  /* JET SELECTION PARAMS */


  /* b-JET SELECTION PARAMS */
  double BTagWPL , BTagWPM , BTagWPT ;
  std::vector<int> BTagCuts; // atm only 2 are accepted, first for selection, second for veto

public:
  string BTagAlgo ;
private:
  unsigned int MinNBJets ;
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
