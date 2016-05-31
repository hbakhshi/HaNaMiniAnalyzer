// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/Histograms.h"

#include <vector>
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "TVector2.h"

#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/TtGenEvent.h"

using namespace std;

class GenMETProbabilityStudies : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit GenMETProbabilityStudies(const edm::ParameterSet&);
  ~GenMETProbabilityStudies();

protected:
  virtual void analyze(const edm::Event& event, const edm::EventSetup&) override;
  virtual void endJob() override;

  edm::Handle< std::vector<reco::GenParticle> > prunedGens;
  edm::Handle< std::vector<pat::MET> > MET;

  edm::EDGetTokenT<std::vector<reco::GenParticle> > prunedGenToken_;
  edm::EDGetTokenT<std::vector<pat::MET> > slimmedMETToken_;

  std::vector<TtGenEventDiLep*> ref;
  std::vector< std::vector< TVector2 > > ref_mets;

  Histogram2D hMETs;
  Histogram2D hL_Mets;
  Histogram2D hB_Mets;
  Histogram2D hL_L;
  Histogram2D hB_B;
  Histogram2D hLB_LB;
  Histogram2D hL_B;
  Histogram2D hLB_MET;
};

DEFINE_FWK_MODULE(GenMETProbabilityStudies);

void GenMETProbabilityStudies::endJob(){
  int nZeros = 0;
  for(uint ii = 0 ; ii < ref.size() ; ii++)
    if( ref_mets[ii].size() > 0 ){
      cout << ref[ii]->MET.Mod() << " , " << ref[ii]->MET.Phi() << " --- " << ref_mets[ii].size() << endl;
      
      for( uint jj = 0 ; jj < ref_mets[ii].size() ; jj++ ){
	cout << "\t" << ref_mets[ii].at(jj).Mod() << " , " << ref_mets[ii].at(jj).Phi() << endl;
      }
    }else
      nZeros ++;

  cout << nZeros << " events with zero matches" << endl;
}

GenMETProbabilityStudies::GenMETProbabilityStudies( const edm::ParameterSet& pset ):
  prunedGenToken_(consumes<std::vector<reco::GenParticle> >(pset.getParameter<edm::InputTag>("prunedGen"))),
  slimmedMETToken_(consumes< std::vector<pat::MET>  >(pset.getParameter<edm::InputTag>("slimmedMET"))),
  hMETs("sample" , "MET_Nominal_Real" , 200 , -10 , 10 , 200 , -10 , 10 ),
  hL_Mets("sample" , "MET_Lepton" , 200 , -10 , 10 , 200 , -10 , 10 ),
  hB_Mets("sample" , "MET_B" , 200 , -10 , 10 , 200 , -10 , 10 ),
  hL_L("sample" , "L_L" , 200 , -10 , 10 , 200 , -10 , 10 ),
  hB_B("sample" , "B_B" , 200 , -10 , 10 , 200 , -10 , 10 ),
  hLB_LB("sample" , "LB_LB" , 200 , -10 , 10 , 200 , -10 , 10 ),
  hL_B("sample" , "L_B" , 200 , -10 , 10 , 200 , -10 , 10 ),
  hLB_MET("sample" , "LB_MET" , 200 , -10 , 10 , 200 , -10 , 10 ){
}

GenMETProbabilityStudies::~GenMETProbabilityStudies() {}

void GenMETProbabilityStudies::analyze(const edm::Event& event, const edm::EventSetup&){
  prunedGens.clear();

  event.getByToken( prunedGenToken_ , prunedGens );
  event.getByToken( slimmedMETToken_ , MET );

  const std::vector<reco::GenParticle>* gen = prunedGens.product();

  TtGenEventDiLep ttbar( gen );
  if(! ttbar.isSet )
    return;
 
  const reco::GenParticle* dm1 = NULL;
  const reco::GenParticle* dm2 = NULL;
  double dm_met_x = 0.0 , dm_met_y = 0.0;
  int dm1_idx = ttbar.getLastCopy( gen , 9100022 ) ;
  if( dm1_idx > -1 ){
    dm1 = &(gen->at( dm1_idx ));
    dm_met_x += dm1->px();
    dm_met_y += dm1->py();
  }
  int dm2_idx = ttbar.getLastCopy( gen , -9100022 ) ;
  if( dm2_idx > -1 ){
    dm2 = &(gen->at( dm2_idx ));
    dm_met_x += dm2->px();
    dm_met_y += dm2->py();
  }
  ttbar.SetTransverseInfo(dm_met_x , dm_met_y);


  // int ii = 0;
  // bool added = false;
  // for( auto rr : ref ){
  //   if ( ttbar.IsTransverseConsistent( rr , 0.3 , 0.5 , 0.3 , 0.5 ) ){
  //     ref_mets[ii].push_back( TVector2(ttbar.MET.Px() , ttbar.MET.Py()) );
  //     added = true;
  //   }
  //   ii ++;
  // }
  // if( !added ){
  //   ref.push_back( new TtGenEventDiLep( &ttbar, true ) );
  //   ref_mets.push_back( std::vector<TVector2>(0) );
  // }

  TVector2 nominalMET = ttbar.getNominalMET();
  double ratio = ttbar.MET.Mod()/nominalMET.Mod() ;
  double dphi_ = ttbar.MET.DeltaPhi( nominalMET );

  hMETs.Fill( dphi_ , ratio );

  ratio = ttbar.MET.Mod()/ttbar.L.Mod() ;
  dphi_ = ttbar.MET.DeltaPhi( ttbar.L );
  hL_Mets.Fill( dphi_ , ratio );

  ratio = ttbar.MET.Mod()/ttbar.LBar.Mod() ;
  dphi_ = ttbar.MET.DeltaPhi( ttbar.LBar );
  hL_Mets.Fill( dphi_ , ratio );

  ratio = ttbar.MET.Mod()/ttbar.B.Mod() ;
  dphi_ = ttbar.MET.DeltaPhi( ttbar.B );
  hB_Mets.Fill( dphi_ , ratio );

  ratio = ttbar.MET.Mod()/ttbar.BBar.Mod() ;
  dphi_ = ttbar.MET.DeltaPhi( ttbar.BBar );
  hB_Mets.Fill( dphi_ , ratio );

  ratio = ttbar.L.Mod()/ttbar.LBar.Mod() ;
  dphi_ = ttbar.L.DeltaPhi( ttbar.LBar );
  hL_L.Fill( dphi_ , ratio );

  ratio = ttbar.B.Mod()/ttbar.BBar.Mod() ;
  dphi_ = ttbar.B.DeltaPhi( ttbar.BBar );
  hB_B.Fill( dphi_ , ratio );

  ratio = ttbar.L.Mod()/ttbar.B.Mod() ;
  dphi_ = ttbar.L.DeltaPhi( ttbar.B );
  hL_B.Fill( dphi_ , ratio );

  ratio = ttbar.LBar.Mod()/ttbar.BBar.Mod() ;
  dphi_ = ttbar.LBar.DeltaPhi( ttbar.BBar );
  hL_B.Fill( dphi_ , ratio );

  TVector2 lb = ttbar.L + ttbar.B ;
  TVector2 lbbar = ttbar.LBar + ttbar.BBar ;
  ratio = lb.Mod()/lbbar.Mod() ;
  dphi_ = lb.DeltaPhi( lbbar );
  hLB_LB.Fill( dphi_ , ratio );

  ratio = lb.Mod()/ttbar.MET.Mod() ;
  dphi_ = lb.DeltaPhi( ttbar.MET );
  hLB_MET.Fill( dphi_ , ratio );

  ratio = lbbar.Mod()/ttbar.MET.Mod() ;
  dphi_ = lbbar.DeltaPhi( ttbar.MET );
  hLB_MET.Fill( dphi_ , ratio );
}
