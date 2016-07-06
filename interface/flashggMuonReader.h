#ifndef flashggMuonReader_H
#define flashggMuonReader_H


#include "BaseEventReader.h"
#include "flashgg/DataFormats/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "flashgg/DataFormats/interface/DiPhotonCandidate.h"

#include "TH2.h"
#include "TROOT.h"
#include "TFile.h"

using namespace edm;
using namespace flashgg;

class flashggMuonReader : public BaseEventReader< edm::View<flashgg::Muon> > {
public:
  flashggMuonReader( edm::ParameterSet const& iPS, edm::ConsumesCollector && iC , bool isData , string SetupDir);
  enum SelectionStep{
    ZeroMuons,
    MoreThanOne,
    ExactlyOneNonIso,
    ExactlyOne
  };
  SelectionStep Read( const edm::Event& iEvent , const DiPhotonCandidate* dipho );

  short nMuons;
  double Iso;
  std::vector<flashgg::Muon> goodMus;
  double W;
private :
  /* MUON SF TOOLS */
  double MuonSFMedium( double etaL , double ptL , double etaSL , double ptSL );
  double MuonSFLoose( double etaL , double ptL , double etaSL , double ptSL );
  TH2* hMuSFID;
  TH2* hMuSFIso;
  /* MUON SF TOOLS */
  double MuonPtCut;
  double MuonIsoCut;
  double MuonEtaCut;
  double DeltaRMuonPho;

  int MuonID;
  bool IsData;
};

#endif
