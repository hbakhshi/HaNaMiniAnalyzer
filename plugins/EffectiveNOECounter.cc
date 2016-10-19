// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "../interface/GenEventInfoProductReader.h"
#include "../interface/HLTReader.h"

#include "../interface/Histograms.h"

//using namespace reco;
using namespace edm;
using namespace std;
//using namespace pat;

class EffectiveNOECounter : public edm::one::EDFilter<edm::one::SharedResources> {
//<edm::one::SharedResources>  {
public:
  explicit EffectiveNOECounter(const edm::ParameterSet& iConfig) :
    IsData( iConfig.getParameter< bool >("isData") ),
    SampleName(iConfig.getParameter< string >("sample") )
  {
    usesResource("TFileService");

    if( !IsData ){
      edm::ParameterSet genPset;
      genPset.addParameter( "Input" , edm::InputTag( "generator" ) );
      geninfoReader = new GenEventInfoProductReader( genPset , consumesCollector() );
    }

    hltReader = new HLTReader( iConfig.getParameter< edm::ParameterSet >("HLT") , consumesCollector() );
    hCutFlowTable = new Histograms( SampleName , "CutFlowTable" , 1 , 0.5 , 2.5 , 1 );
  }
  ~EffectiveNOECounter(){};

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions){};
protected:
  bool IsData;
  string SampleName;
  GenEventInfoProductReader* geninfoReader;
  HLTReader* hltReader;
  Histograms* hCutFlowTable;

  virtual void beginJob() override{};
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup&) override{
    int W = 1;
    if( geninfoReader )
      W *= geninfoReader->Read( iEvent );

    hCutFlowTable->Fill( 1 , W );

    if( hltReader->Read( iEvent ) < 0 )
      return false;
    else{
      hCutFlowTable->Fill( 2 , W );
      return true;
    }
  };
  virtual void endJob() override{};

};

DEFINE_FWK_MODULE(EffectiveNOECounter);
