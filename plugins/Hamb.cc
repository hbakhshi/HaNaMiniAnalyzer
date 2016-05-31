#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/HaNaBaseMiniAnalyzer.h"

#include <iostream>

using namespace std;

class Hamb : public HaNaBaseMiniAnalyzer{
public:
  explicit Hamb(const edm::ParameterSet&);
  ~Hamb();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions){ HaNaBaseMiniAnalyzer::fillDescriptions( descriptions ); }




  // ----------member data ---------------------------
  Histograms* hCutFlowTable;
  Histograms* hNPV_pv;
  Histograms* hMuMult;
  Histograms* hJetMult;
  Histograms* hBJetMult;
  Histograms* hNPV_final;
  Histograms* hMuPt;
  Histograms* hMuEta;
  Histograms* hLeadMuPt;
  Histograms* hLeadMuEta;
  Histograms* hSubLeadMuPt;
  Histograms* hSubLeadMuEta;
  Histograms* hDiMuMass;
  Histograms* hDiMuPt;
  Histograms* hDiMuDr;
  Histograms* hJetPt;
  Histograms* hJetEta;
  Histograms* hJetBTag;
  Histograms* hLeadJetPt;
  Histograms* hLeadJetEta;
  Histograms* hLeadJetBTag;
  Histograms* hSubLeadJetPt;
  Histograms* hSubLeadJetEta;
  Histograms* hSubLeadJetBTag;
  Histograms* hDiBJetMass;
  Histograms* hDiBJetPt;
  Histograms* hDiBJetDr;
  Histograms* hFourBodyMass;
  Histograms* hFourBodyPt;
  Histograms* hDiffMassMuB;
  Histograms* hRelDiffMassMuB;
  Histograms* hMET;
  Histograms* hMETSignificance;
  Histograms* hNMuHits;

  void initHistograms();
protected:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
};

DEFINE_FWK_MODULE(Hamb);

void Hamb::initHistograms(){   
    hNPV_pv = new Histograms(SampleName, "NPV_pv", 100, -0.5, 99.5);
    hMuMult = new Histograms(SampleName, "MuMult", 10, -0.5, 9.5);
    hJetMult = new Histograms(SampleName, "JetMult", 10, -0.5, 9.5);
    hBJetMult = new Histograms(SampleName, "BJetMult", 10, -0.5, 9.5);
    hNPV_final = new Histograms(SampleName, "NPV_final", 100, -0.5, 99.5);
    hMuPt = new Histograms(SampleName, "MuPt", 30, 0., 150.);
    hMuEta = new Histograms(SampleName, "MuEta", 30, -3.0, 3.0);
    hLeadMuPt= new Histograms(SampleName, "LeadMuPt", 30, 0., 150.);
    hLeadMuEta= new Histograms(SampleName, "LeadMuEta", 30, -3.0, 3.0);
    hSubLeadMuPt= new Histograms(SampleName, "SubLeadMuPt", 30, 0., 150.);
    hSubLeadMuEta= new Histograms(SampleName, "SubLeadMuEta", 30, -3.0, 3.0);
    hDiMuMass= new Histograms(SampleName, "DiMuMass", 17, 10., 180.);
    hDiMuPt= new Histograms(SampleName, "DiMuPt", 40, 0., 200.);
    hDiMuDr= new Histograms(SampleName, "DiMuDr", 50, 0, 5.0);
    hJetPt= new Histograms(SampleName, "JetPt", 30, 0., 150.);
    hJetEta= new Histograms(SampleName, "JetEta", 50, -5.0, 5.0);
    hJetBTag= new Histograms(SampleName, "JetBTag", 20, 0, 1.);
    hLeadJetPt= new Histograms(SampleName, "LeadJetPt", 30, 0., 150.);
    hLeadJetEta= new Histograms(SampleName, "LeadJetEta", 50, -5.0, 5.0);
    hLeadJetBTag= new Histograms(SampleName, "LeadJetBTag", 20, 0, 1.);
    hSubLeadJetPt= new Histograms(SampleName, "SunLeadJetPt", 30, 0., 150.);
    hSubLeadJetEta= new Histograms(SampleName, "SubLeadJetEta", 50, -5.0, 5.0);
    hSubLeadJetBTag= new Histograms(SampleName, "SubLeadJetBTag", 20, 0, 1.);
    hDiBJetMass= new Histograms(SampleName, "DiBJetMass", 30, 0., 300.);
    hDiBJetPt= new Histograms(SampleName, "DiBJetPt", 15, 0., 150.);
    hDiBJetDr= new Histograms(SampleName, "DiBJetDr", 50, 0, 5.0);
    hFourBodyMass= new Histograms(SampleName, "FourBodyMass", 30, 0., 300.);
    hFourBodyPt= new Histograms(SampleName, "FourBodyPt", 20, 0., 200.);
    hDiffMassMuB= new Histograms(SampleName, "DiffMassMuB", 15, 0., 150.);
    hRelDiffMassMuB= new Histograms(SampleName, "RelDiffMassMuB", 20, 0, 1.);
    hMET= new Histograms(SampleName, "MET", 20, 0., 200.);
    hMETSignificance= new Histograms(SampleName, "METSignificance", 20, 0, 20.);
    hNMuHits = new Histograms(SampleName, "nMuHits", 10, -0.5, 9.5);
  }




Hamb::~Hamb() {}
Hamb::Hamb( const edm::ParameterSet& ps ) :
  HaNaBaseMiniAnalyzer( ps ) 
{
}
// ------------ method called once each job just before starting event loop  ------------
void Hamb::beginJob()
{
  hCutFlowTable = new Histograms( SampleName , "CutFlowTable" , 10 , 0.5 , 10.5 );
  initHistograms();
}

//
void Hamb::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  W = 1.0;
  stepEventSelection = 0;
  
  if( LHEReader )
    W *= LHEReader->Read( iEvent );

  hCutFlowTable->Fill( ++stepEventSelection , W );

  if( hltReader->Read( iEvent ) < 0 )
    return;
  hCutFlowTable->Fill( ++stepEventSelection , W );

  if( vertexReader->Read( iEvent ) < 0 )
    return;
  W *= vertexReader->puWeight;
  hCutFlowTable->Fill( ++stepEventSelection , W );

  //cout << vertexReader->PV()->ndof() << endl;
  switch( diMuReader->Read( iEvent , vertexReader->PV() ) ){
  case DiMuonReader::Pass :
    W *= (diMuReader->W) ;
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hMuMult->Fill(diMuReader->goodMus.size(), W);
    break;
  case DiMuonReader::UnderTheZPeak:
    W *= (diMuReader->W) ;
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiMuonReader::LowMassPair:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiMuonReader::NoPairWithChargeReq:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiMuonReader::LessThan2Muons :
    hMuMult->Fill(diMuReader->goodMus.size(), W);
    return ;
  }
  
  if( metReader->Read(iEvent 
		      /*, jetReader->GetAllJets()*/) < 0 )
    //uncomment the inner part if JES changes wrt the oldjets collection wants to be applied on met , it should be called after reading jets
    return;
  hCutFlowTable->Fill( ++stepEventSelection , W );


  /***** Filling Histograms ******/
  hNPV_pv->Fill(vertexReader->vtxMult, W / (vertexReader->puWeight==0. ? 1.0 : vertexReader->puWeight) );
  hNPV_final->Fill(vertexReader->vtxMult,W);
  hMuPt->Fill(diMuReader->goodMusOS[0].pt(), W); hMuPt->Fill(diMuReader->goodMusOS[1].pt(), W);
  hMuEta->Fill(diMuReader->goodMusOS[0].eta(), W); hMuEta->Fill(diMuReader->goodMusOS[1].eta(), W);

  hLeadMuPt->Fill(diMuReader->goodMusOS[0].pt(), W);
  hLeadMuEta->Fill(diMuReader->goodMusOS[0].eta(), W);

  hSubLeadMuPt->Fill(diMuReader->goodMusOS[1].pt(), W);
  hSubLeadMuEta->Fill(diMuReader->goodMusOS[1].eta(), W);

  hDiMuMass->Fill( diMuReader->DiMuon.totalP4().M() , W );
  hDiMuPt->Fill( diMuReader->DiMuon.totalP4().Pt(), W);
  hDiMuDr->Fill( diMuReader->DiMuon.deltaR() , W );
  /***** End Filling Histograms **/ 



  switch( jetReader->Read( iEvent , &(diMuReader->DiMuon) ) ){
  case JetReader::Pass:
    W *= jetReader->W ;
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hJetMult->Fill(jetReader->selectedJets.size(), W);
    hBJetMult->Fill(jetReader->selectedBJets.size(), W);
    break;
  case JetReader::NotEnoughBJets:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case JetReader::NotEnoughJets:
    hJetMult->Fill(jetReader->selectedJets.size(), W);
    hBJetMult->Fill(jetReader->selectedBJets.size(), W);
    return;
  }

 
  for( unsigned int iJet = 0; iJet < jetReader->selectedJets.size(); iJet++){
    hJetPt->Fill(jetReader->selectedJets[iJet].pt(), W);
    hJetEta->Fill(jetReader->selectedJets[iJet].eta(), W);
    hJetBTag->Fill(jetReader->selectedJets[iJet].bDiscriminator(jetReader->BTagAlgo), W);
  }

  if( jetReader->selectedJets.size() > 0 ){
    hLeadJetPt->Fill(jetReader->selectedJets[0].pt(), W); 
    hLeadJetEta->Fill(jetReader->selectedJets[0].eta(), W);
    hLeadJetBTag->Fill(jetReader->selectedJets[0].bDiscriminator(jetReader->BTagAlgo), W);
  }

  if( jetReader->selectedJets.size() > 1 ){ 
    hSubLeadJetPt->Fill(jetReader->selectedJets[1].pt(), W);
    hSubLeadJetEta->Fill(jetReader->selectedJets[1].eta(), W);
    hSubLeadJetBTag->Fill(jetReader->selectedJets[1].bDiscriminator(jetReader->BTagAlgo), W);
  }

  pat::DiObjectProxy* DiBJets = NULL;

  if( jetReader->selectedBJets.size() > 1 ){
    DiBJets = new pat::DiObjectProxy( jetReader->selectedBJets[0] , jetReader->selectedBJets[1] );
    hDiBJetMass->Fill(DiBJets->totalP4().M(),W);
    hDiBJetPt->Fill( DiBJets->totalP4().Pt(),W);
    hDiBJetDr->Fill( DiBJets->deltaR() , W);
    hFourBodyMass->Fill( (DiBJets->totalP4() + diMuReader->DiMuon.totalP4()).M(),W);
    hFourBodyPt->Fill( (DiBJets->totalP4() + diMuReader->DiMuon.totalP4()).Pt(),W);
    hDiffMassMuB->Fill(fabs( DiBJets->totalP4().M() - diMuReader->DiMuon.totalP4().M() ),W);
    hRelDiffMassMuB->Fill( fabs( DiBJets->totalP4().M() - diMuReader->DiMuon.totalP4().M() )/ (DiBJets->totalP4() + diMuReader->DiMuon.totalP4()).M() , W );
  }


}
