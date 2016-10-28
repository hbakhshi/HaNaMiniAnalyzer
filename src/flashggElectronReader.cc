#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/flashggElectronReader.h"

flashggElectronReader::flashggElectronReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC , bool isData , string SetupDir) :
  BaseEventReader< edm::View<flashgg::Electron> >( iConfig , &iC ),
  ElectronPtCut( iConfig.getParameter<double>( "ElectronPtCut" ) ),
  ElectronEtaCut( iConfig.getParameter<double>( "ElectronEtaCut" ) ),
  DeltaRElectronPho( iConfig.getParameter<double>( "DeltaRElectronPho" ) ),
  DeltaRElectronTrk( iConfig.getParameter<double>( "DeltaRElectronTrk" ) ), 
  DeltaMassElectronZ( iConfig.getParameter<double>( "DeltaMassElectronZ" ) ),
  ElectronID( iConfig.getParameter<int>( "ElectronID" ) ), // 0 veto, 1 loose, 2 medium, 3 tight
  IsData(isData)
  {
      if( !IsData )
      {
	  hEleSFID = NULL;
	  if(ElectronID == 0 )// Veto ID
	  {
	      TFile* f1 = TFile::Open( TString(SetupDir + "/egammaEffi_SF2D_Veto.root") );
	      hEleSFID = (TH2*)( f1->Get("EGamma_SF2D")->Clone("EGamma_SF2D_Cloned") );
	      f1->Close();
	  }
	  else if(ElectronID == 2 ) // Loose ID
	  {
	      TFile* f1 = TFile::Open( TString(SetupDir + "/egammaEffi_SF2D_Loose.root") );
	      hEleSFID = (TH2*)( f1->Get("EGamma_SF2D")->Clone("EGamma_SF2D_Cloned" ) );
	      f1->Close();
	  }
	  else if(ElectronID == 3 ) // Medium ID
	  {
	    TFile* f1 = TFile::Open( TString(SetupDir + "/egammaEffi_SF2D_Medium.root") );
	    hEleSFID = (TH2*)( f1->Get("EGamma_SF2D")->Clone("EGamma_SF2D_Cloned" ) );
	    f1->Close();
	  }
	  else if(ElectronID == 4 ) // Tight ID
	  {
	    TFile* f1 = TFile::Open( TString(SetupDir + "/egammaEffi_SF2D_Tight.root") );
	    hEleSFID = (TH2*)( f1->Get("EGamma_SF2D")->Clone("EGamma_SF2D_Cloned" ) );
	    f1->Close();
	  }
	  else
	    cout << "No scale factor is availabel for Electron ID " << ElectronID << endl;

	  
	  TFile* f1 = TFile::Open( TString(SetupDir + "/egammaEffi_SF2D_Reco.root") );
	  hEleSFReco = (TH2*)( f1->Get("EGamma_SF2D")->Clone("EGamma_SF2D_Cloned" ) );
	  f1->Close();
      }
      
  }

flashggElectronReader::SelectionStep flashggElectronReader::Read( const edm::Event& iEvent , const DiPhotonCandidate* dipho ){
  BaseEventReader< edm::View<flashgg::Electron> >::Read( iEvent );

  W = 1.0;
  goodEles.clear();

  
  for (flashgg::Electron ele : *handle) 
  {
      if (ele.pt() < ElectronPtCut) continue;
      if (fabs(ele.superCluster()->eta()) > ElectronEtaCut || ( fabs(ele.superCluster()->eta()) > 1.4442 && fabs(ele.superCluster()->eta()) >1.566) ) continue;

      std::vector<bool> IDs;
      IDs.clear();
      IDs.push_back(ele.passVetoId());
      IDs.push_back(ele.passLooseId());
      IDs.push_back(ele.passMediumId());
      IDs.push_back(ele.passTightId());
      
      if(!IDs[ElectronID]) continue;
      
      double Zmass_ = 91.9;
      bool photon_veto = false;
      
      std::vector<const flashgg::Photon *> photons;        
      photons.push_back( dipho->leadingPhoton() );
      photons.push_back( dipho->subLeadingPhoton() );
      
      TLorentzVector ele_p4;
      ele_p4.SetXYZT( ele.px(), ele.py(), ele.pz(), ele.energy() );
      
      TLorentzVector ele_superClusterVect;
      ele_superClusterVect.SetXYZT(ele.superCluster()->position().x(),ele.superCluster()->position().y(),
				   ele.superCluster()->position().z(),ele.ecalEnergy());            
      
      
      for( unsigned int phoIndex = 0; phoIndex <photons.size(); phoIndex++ ) 
      {
      
	  float drPhoEle=deltaR( ele.eta(), ele.phi(), photons.at( phoIndex )->superCluster()->eta(),  photons.at( phoIndex )->superCluster()->phi() ); 
	  if( drPhoEle < DeltaRElectronPho ) photon_veto=true;
      
	  TLorentzVector p;
	  p.SetXYZT( photons.at( phoIndex )->px(), photons.at( phoIndex )->py(), photons.at( phoIndex )->pz(), photons.at( phoIndex )->energy() );
	  
	  if( p.DeltaR( ele_superClusterVect ) < DeltaRElectronPho ) photon_veto=true;
	  
	  if( &( *photons.at( phoIndex )->superCluster() ) == &( *ele.superCluster() ) ) {
	    float TrkEleSCDeltaR = TMath::Sqrt( ele.deltaEtaSuperClusterTrackAtVtx() * ele.deltaEtaSuperClusterTrackAtVtx() +
						ele.deltaPhiSuperClusterTrackAtVtx() * ele.deltaPhiSuperClusterTrackAtVtx() );
	    
	    if( TrkEleSCDeltaR < DeltaRElectronTrk ) photon_veto=true;               
	  }
      
	  if( p.DeltaR( ele_p4 ) < DeltaRElectronPho ) photon_veto=true;
            
	  TLorentzVector elep = ele_p4 + p;
	  if( fabs( elep.M() - Zmass_ ) < DeltaMassElectronZ ) photon_veto=true;   
      }
  
      if(!photon_veto) goodEles.push_back( ele );
  }

  switch( goodEles.size() )
  {
      case 0 :
      {
	  nElectrons = 0;
	  return flashggElectronReader::ZeroElectrons ;
      }
      case 1:
      {
	  nElectrons = 1;
	  double wId = 1.0; 
	  double wReco = 1.0;
	  
	  if( !IsData )
	  {
	      wId =  hEleSFID->GetBinContent( hEleSFID->FindBin( goodEles[0].pt() , fabs(goodEles[0].superCluster()->eta())) ) ;
	      wReco = hEleSFReco->GetBinContent( hEleSFReco->FindBin(goodEles[0].pt() , fabs(goodEles[0].superCluster()->eta())) ) ;
	  }
	  W *= (wId * wReco);
	  return flashggElectronReader::ExactlyOne ;
      }
      default:
      {
	  nElectrons = goodEles.size() ;
	  return flashggElectronReader::MoreThanOne;
      }
  }
  
}
  


