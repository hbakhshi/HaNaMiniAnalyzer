// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/MT2Scanner.h"
#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/Histograms.h"

#include <vector>
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "TVector2.h"

using namespace std;

class GenMT2Studies : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit GenMT2Studies(const edm::ParameterSet&);
  ~GenMT2Studies();

  MT2Scanner scanner;

  Histograms* hMET;
  Histogram2D* hD_DM_TT;
  Histogram2D* hD_DM_Total;
protected:
  virtual void analyze(const edm::Event& event, const edm::EventSetup&) override;
  virtual void endJob() override;

  edm::Handle< edm::View<reco::GenParticle> > prunedGens;
  edm::Handle< edm::View<pat::PackedGenParticle> > packedGens;
  edm::Handle< std::vector<pat::MET> > MET;

  edm::EDGetTokenT<edm::View<reco::GenParticle> > prunedGenToken_;
  edm::EDGetTokenT<edm::View<pat::PackedGenParticle> > packedGenToken_;
  edm::EDGetTokenT<std::vector<pat::MET> > slimmedMETToken_;
};

DEFINE_FWK_MODULE(GenMT2Studies);

void GenMT2Studies::endJob(){
  scanner.Finalize();
}

GenMT2Studies::GenMT2Studies( const edm::ParameterSet& pset ):
  scanner( pset  ),
  prunedGenToken_(consumes<edm::View<reco::GenParticle> >(pset.getParameter<edm::InputTag>("prunedGen"))),
  //packedGenToken_(consumes<edm::View<pat::PackedGenParticle> >(pset.getParameter<edm::InputTag>("packedGen"))),
  slimmedMETToken_(consumes< std::vector<pat::MET>  >(pset.getParameter<edm::InputTag>("slimmedMET"))){

  hMET = new Histograms("GenMET" , "MET" , 100 , 0 , 500 );
  hD_DM_Total = new Histogram2D("D_DM_Total" , "DM and Total MET Differences" , 100 , 0 , 5.0 , 20 , -M_PI , M_PI );
  hD_DM_TT = new Histogram2D("D_DM_TT" , "DM and TT MET Differences" , 100 , 0 , 5.0 , 20 , -M_PI , M_PI );
}

GenMT2Studies::~GenMT2Studies() {}

void GenMT2Studies::analyze(const edm::Event& event, const edm::EventSetup&){
  event.getByToken( prunedGenToken_ , prunedGens );
  //event.getByToken( packedGenToken_ , packedGens );
  event.getByToken( slimmedMETToken_ , MET );
  
  double b_px = 0 ; 
  double b_py = 0 ; 
  double bbar_px = 0 ; 
  double bbar_py = 0;
  double l_px = 0 ; 
  double l_py = 0 ; 
  double lbar_px = 0 ; 
  double lbar_py = 0;
  
  bool lbar = false;
  bool l = false;
  bool b = false;
  bool bbar = false;
  bool tau = false;
  bool neutrino = false;
  bool neutrinobar = false;

  double genMetPx = 0.0;
  double genMetPy = 0.0;

  double DDgenMetPx = 0.0;
  double DDgenMetPy = 0.0;

  for(auto genPart : *prunedGens ){
    int pdgid = genPart.pdgId();
    int apdgid = abs(pdgid);
    if( apdgid != 5 && apdgid != 13 && apdgid != 11 && apdgid != 15 &&
	apdgid != 12 && apdgid != 14 && apdgid != 16 && apdgid != 9100022 )
      {
	//if( genPart.isHardProcess() )
	//cout << pdgid << "  " ;
	continue;
      }
    //if( ! (genPart.isLastCopy()) )
    //continue;

    switch( pdgid ){
    case 9100022:
    case -9100022:
      if( !genPart.isHardProcess() )
	continue;
      DDgenMetPy += genPart.py();
      DDgenMetPx += genPart.px();
      break;
    case 16:
    case 14:
    case 12:
      if(neutrino ||  !( abs(genPart.mother()->pdgId()) == 24 ) )
	continue; //cout << "l already set" <<endl;
      genMetPy += genPart.py() ;
      genMetPx += genPart.px() ;
      neutrino = true;
      break;
    case -16:
    case -14:
    case -12:
      if(neutrinobar ||  !( abs(genPart.mother()->pdgId()) == 24 ) )
	continue; //cout << "l already set" <<endl;
      genMetPy += genPart.py() ;
      genMetPx += genPart.px() ;
      neutrinobar = true;
      break;
    case 5:
      if(b || !( abs(genPart.mother()->pdgId()) == 6 ) )
	continue; //cout << "b already set" <<endl;
      b_px = genPart.px();
      b_py = genPart.py();
      b = true;
      break;
    case -5:
      if(bbar ||  !( abs(genPart.mother()->pdgId()) == 6 ) )
	continue; //cout << "bbar already set" <<endl;
      bbar_px = genPart.px();
      bbar_py = genPart.py();
      bbar = true;
      break;
    case 15:
      tau = true;
    case 13:
    case 11:
      if(l ||  !( abs(genPart.mother()->pdgId()) == 24 ) )
	continue; //cout << "l already set" <<endl;
      l_px = genPart.px();
      l_py = genPart.py();
      l = true;
      break;
    case -15:
      tau = true;
    case -13:
    case -11:
      if(lbar || !( abs(genPart.mother()->pdgId()) == 24 ) )
	continue; //cout << "lbar already set" <<endl;
      lbar_px = genPart.px();
      lbar_py = genPart.py();
      lbar = true;
      break;
    }
  }
  //cout << endl;
  if( l && lbar && b && bbar && !tau ){
    scanner.Calculate( b_px ,  b_py ,  bbar_px ,  bbar_py , 
		       genMetPx  + DDgenMetPx + l_px + lbar_px ,
		       genMetPy  + DDgenMetPx + l_py + lbar_py  );
    hMET->Fill( hypot( genMetPy+DDgenMetPy , genMetPx+DDgenMetPx ) );

    TVector2 total_met( genMetPx + DDgenMetPx + l_px + lbar_px  , genMetPy + DDgenMetPy + l_py + lbar_py );
    TVector2 tt_met( genMetPx  + l_px + lbar_px  , genMetPy + l_py + lbar_py  );
    TVector2 dm_met( DDgenMetPx , DDgenMetPy );
    hD_DM_TT->Fill( (tt_met-dm_met).Mod()/dm_met.Mod() ,  tt_met.DeltaPhi( dm_met ) )  ;
    hD_DM_Total->Fill( (total_met - dm_met).Mod()/total_met.Mod() ,  total_met.DeltaPhi( dm_met ) ) ;
  }
  // else
  //   if( !tau )
  //     cout << "one of the constituents was not found : " << l << "\t" << lbar << "\t" << b << "\t" << bbar  << "\t" << tau << endl;
}
