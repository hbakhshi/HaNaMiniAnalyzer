#ifndef flashggElectronReader_H
#define flashggElectronReader_H


#include "BaseEventReader.h"
#include "flashgg/DataFormats/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "flashgg/DataFormats/interface/DiPhotonCandidate.h"

#include "TH2.h"
#include "TLorentzVector.h"
#include "TROOT.h"
#include "TFile.h"

using namespace edm;
using namespace flashgg;

class flashggElectronReader : public BaseEventReader< edm::View<flashgg::Electron> > {
public:
  flashggElectronReader( edm::ParameterSet const& iPS, edm::ConsumesCollector && iC , bool isData , string SetupDir);
  enum SelectionStep{
    ZeroElectrons,
    MoreThanOne,
    ExactlyOne
  };
  SelectionStep Read( const edm::Event& iEvent , const DiPhotonCandidate* dipho );

  short nElectrons;
  std::vector<flashgg::Electron> goodEles;
  double W;
private :
  /* ELECTRON SF TOOLS */
  TH2* hEleSFID;
  TH2* hEleSFReco;
  /* ELECTRON SF TOOLS */
  double ElectronPtCut;
  double ElectronEtaCut;
  double DeltaRElectronPho;
  double DeltaRElectronTrk;
  double DeltaMassElectronZ;

  int ElectronID;
  bool IsData;
};

#endif
