#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/flashggMuonReader.h"

flashggMuonReader::flashggMuonReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC , bool isData , string SetupDir) :
  BaseEventReader< edm::View<flashgg::Muon> >( iConfig , &iC ),
  MuonPtCut( iConfig.getParameter<double>( "MuonPtCut" ) ),
  MuonIsoCut( iConfig.getParameter<double>( "MuonIsoCut" ) ),
  MuonEtaCut( iConfig.getParameter<double>( "MuonEtaCut" ) ),
  DeltaRMuonPho( iConfig.getParameter<double>( "DeltaRMuonPho" ) ),
  MuonID( iConfig.getParameter<int>( "MuonID" ) ), // 0 no id, 1 loose, 2 medium, 3 tight, 4 soft
  IsData(isData)
{
  if( !IsData ){
    TFile* f1 = TFile::Open( TString(SetupDir + "/MuonIDSF.root") );
    gROOT->cd();
    hMuSFID = NULL;
    if(MuonID == 1 ) // Loose ID
      hMuSFID = (TH2*)( f1->Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")->Clone("MuSFID") );
    else if(MuonID == 2 ) // Medium ID
      hMuSFID = (TH2*)( f1->Get("MC_NUM_MediumID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")->Clone("MuSFID") );
    else if(MuonID == 3 ) // Tight ID
      hMuSFID = (TH2*)( f1->Get("MC_NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")->Clone("MuSFID") );
    else if(MuonID == 4 ) // Soft ID
      hMuSFID = (TH2*)( f1->Get("MC_NUM_SoftID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")->Clone("MuSFID") );
    else
      cout << "No scale factor is availabel for Muon ID " << MuonID << endl;
    f1->Close();
    
    f1 = TFile::Open( TString(SetupDir + "/MuonIsoSF.root") );
    gROOT->cd();
    if( MuonIsoCut == 0.15 )
      hMuSFIso = (TH2*)( f1->Get("MC_NUM_TightRelIso_DEN_TightID_PAR_pt_spliteta_bin1/pt_abseta_ratio")->Clone("MuSFIso") );
    else if( MuonIsoCut == 0.25 )
      hMuSFIso = (TH2*)( f1->Get("MC_NUM_LooseRelIso_DEN_TightID_PAR_pt_spliteta_bin1/pt_abseta_ratio")->Clone("MuSFIso") );
    else
      cout << "No scale factor is availabel for Muon Iso " << MuonIsoCut << endl;
    f1->Close();
  }

  //cout << MuonSubLeadingPtCut << "  " << MuonEtaCut << "  " << MuonLeadingPtCut << "    " << MuonIsoCut << "    " << MuonID << endl;
}

double flashggMuonReader::MuonSFMedium( double etaL , double ptL , double etaSL , double ptSL ){
  //AN2016_025_v7 Figure 6, Middle Row, Right for trigger
  double ret = 1.0;

  double el = fabs(etaL);
  double esl = fabs(etaSL);
  if(el < 1.2 && esl < 1.2 )
    ret = 0.926 ;				
  else if( el < 1.2 )
    ret = 0.943;
  else if( esl < 1.2 )
    ret = 0.958 ;
  else 
    ret = 0.926 ;

  if( ptSL < 20 || ptL < 20 )
    return ret;

  ret *= ( hMuSFID->GetBinContent( hMuSFID->FindBin( ptL , el ) ) * hMuSFID->GetBinContent( hMuSFID->FindBin( ptSL , esl ) ) );
  ret *= (hMuSFIso->GetBinContent(hMuSFIso->FindBin(ptL ,el ) ) * hMuSFIso->GetBinContent( hMuSFIso->FindBin( ptSL , esl ) ) );

  return ret;
}
double flashggMuonReader::MuonSFLoose( double etaL , double ptL , double etaSL , double ptSL ){
  //AN2016_025_v7 Figure 19, Middle Row, Right for trigger
  double ret = 1.0;
    
  double el = fabs(etaL);
  double esl = fabs(etaSL);
  if(el < 1.2 && esl < 1.2 )
    ret = 0.930 ;				
  else if( el < 1.2 )
    ret = 0.933;
  else if( esl < 1.2 )
    ret = 0.951 ;
  else 
    ret = 0.934 ;

  if( ptSL < 20 || ptL < 20 )
    return ret;

  ret *= ( hMuSFID->GetBinContent( hMuSFID->FindBin( ptL , el ) ) * hMuSFID->GetBinContent( hMuSFID->FindBin( ptSL , esl ) ) );
  ret *= (hMuSFIso->GetBinContent(hMuSFIso->FindBin(ptL ,el ) ) * hMuSFIso->GetBinContent( hMuSFIso->FindBin( ptSL , esl ) ) );

  return ret;
}


flashggMuonReader::SelectionStep flashggMuonReader::Read( const edm::Event& iEvent , const DiPhotonCandidate* dipho ){
  BaseEventReader< edm::View<flashgg::Muon> >::Read( iEvent );

  W = 1.0;
  goodMus.clear();

  for (flashgg::Muon mu : *handle) {
    if (mu.pt() < MuonPtCut || fabs(mu.eta()) > MuonEtaCut )
      continue;

    if( MuonID == 1 ){
      if (!muon::isLooseMuon( mu ) ) continue;
    }
    else if(MuonID == 2){
      if (!muon::isMediumMuon( mu ) ) continue;
    }
    else if(MuonID == 3){
      if (!muon::isTightMuon(mu , *(dipho->vtx()) ) ) continue;
    }
    else if(MuonID == 4){
      if (!muon::isSoftMuon( mu , *(dipho->vtx()) ) ) continue;
    }
    reco::MuonPFIsolation iso = mu.pfIsolationR04();
    double reliso = (iso.sumChargedHadronPt+TMath::Max(0.,iso.sumNeutralHadronEt+iso.sumPhotonEt-0.5*iso.sumPUPt))/mu.pt();
    if( reliso > MuonIsoCut) continue;

    double dr0 = reco::deltaR( mu.p4() , dipho->leadingPhoton()->p4() );
    double dr1 = reco::deltaR( mu.p4() , dipho->subLeadingPhoton()->p4() );
    if( dr0 < DeltaRMuonPho || dr1 < DeltaRMuonPho ) continue ;

    goodMus.push_back( mu );
  }
    
  switch( goodMus.size() ){
  case 0 :
    return flashggMuonReader::ZeroMuons ;
  case 1:
    double pt = goodMus[0].pt();
    double eta = goodMus[0].eta();
    W *=  hMuSFID->GetBinContent( hMuSFID->FindBin( pt , eta ) ) ;
    W *= hMuSFIso->GetBinContent( hMuSFIso->FindBin(pt , eta ) ) ;
    return flashggMuonReader::ExactlyOne ;
  }

  return flashggMuonReader::MoreThanOne;
}

