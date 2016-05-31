// -*- C++ -*-
//
// Package:    tHqAnalyzer/HaNaMiniAnalyzer
// Class:      HaNaMiniAnalyzer
// 
/**\class HaNaMiniAnalyzer HaNaMiniAnalyzer.cc tHqAnalyzer/HaNaMiniAnalyzer/plugins/HaNaMiniAnalyzer.cc

   Description: [one line class summary]

   Implementation:
   [Notes on implementation]
*/
//
// Original Author:  Hamed Bakhshiansohi
//         Created:  Fri, 25 Mar 2016 10:57:06 GMT
//
//

#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/HaNaBaseMiniAnalyzer.h"

HaNaBaseMiniAnalyzer::HaNaBaseMiniAnalyzer(const edm::ParameterSet& iConfig):
  SetupDir( iConfig.getParameter<string>("SetupDir") ),
  IsData( iConfig.getParameter< bool >("isData") ),
  SampleName(iConfig.getParameter< string >("sample") )
{
  LHEReader = NULL;
  if( !IsData ){
    edm::ParameterSet LHE = iConfig.getParameter< edm::ParameterSet >("LHE");
    if( LHE.getParameter< bool >( "useLHEW" ) )
      LHEReader = new LHEEventReader( LHE , consumesCollector() );
  }  

  hltReader = new HLTReader( iConfig.getParameter< edm::ParameterSet >("HLT") , consumesCollector() );
  vertexReader = new VertexReader( iConfig.getParameter< edm::ParameterSet >("Vertex") , consumesCollector() , IsData , SetupDir );

  if( iConfig.exists( "DiMuon" ) ){
    diMuReader = new DiMuonReader( iConfig.getParameter< edm::ParameterSet >("DiMuon") , consumesCollector() , IsData , SetupDir );
  }else
    diMuReader = NULL;

  if( iConfig.exists( "MET" ) ){
    metReader = new METReader( iConfig.getParameter< edm::ParameterSet >("MET") , consumesCollector() , IsData );
  }else
    metReader = NULL;

  if( iConfig.exists( "Jets" ) ){
    jetReader = new JetReader( iConfig.getParameter< edm::ParameterSet >("Jets") , consumesCollector() , IsData , SetupDir );
  }else
    jetReader = NULL;

}

//
void HaNaBaseMiniAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
}




// ------------ method called once each job just before starting event loop  ------------
void HaNaBaseMiniAnalyzer::beginJob()
{
}
void HaNaBaseMiniAnalyzer::endJob() 
{
}

HaNaBaseMiniAnalyzer::~HaNaBaseMiniAnalyzer()
{
}
void HaNaBaseMiniAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
