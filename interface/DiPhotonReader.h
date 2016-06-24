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
    ZeroPairs,
    LeadingPt,
    SubLeadingPt,
    PhotonID,
    MVAFailed,
    InvMassFailed,
    Pass,
    PassMoreThanOne
  };
  SelectionStatus read( const edm::Event& iEvent );

  const DiPhotonCandidate* diPhoton;
  double MVA ;
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
