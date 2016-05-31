#ifndef TtGenEvent_h
#define TtGenEvent_h

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include <vector>
#include "TVector2.h"

class TopDecayChain {
public:
  TopDecayChain(){};
  void Set(const reco::GenParticle* _Top,
		const reco::GenParticle* _W,
		const reco::GenParticle* _b,
		const reco::GenParticle* _Lepton,
		const reco::GenParticle* _Neutrino ){
    Top = _Top;
    W = _W;
    b = _b;
    Lepton = _Lepton;
    Neutrino = _Neutrino;
  }

  const reco::GenParticle* Top;
  const reco::GenParticle* W;
  const reco::GenParticle* b;  
  const reco::GenParticle* Lepton;
  const reco::GenParticle* Neutrino;
};

class TtGenEventDiLep {
public:
  TtGenEventDiLep( const TtGenEventDiLep* ttbar , bool JustTransverse );
  TtGenEventDiLep( const std::vector<reco::GenParticle>* );
  ~TtGenEventDiLep();
  int getLastCopy( const std::vector<reco::GenParticle>* gens, int pdgId , int parentId=0 , bool beforeFSR = false , bool noCheckLastCopy = false );

  void SetTransverseInfo(double DMMetX = 0.0 , double DMMetY = 0.0);
  bool IsTransverseConsistent( TtGenEventDiLep* ref  , double lep_phi_res , double lep_e_res , double b_phi_res , double b_e_res );

  TVector2 getNominalMET() const;
  
  bool isSet ;

  TopDecayChain Top;
  TopDecayChain TopBar;
  
  TVector2 MET;
  TVector2 L,LBar,B,BBar;
  TVector2 DDgenMET;
};


#endif

