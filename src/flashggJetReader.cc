#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/flashggJetReader.h"


flashggJetReader::flashggJetReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC , bool isData , string SetupDir) :
  BaseEventReader< flashggJetCollection >( iConfig , &iC ),
  IsData( isData ),
  ApplyJER( iConfig.getParameter<bool>( "ApplyJER" ) ),
  JetPtCut( iConfig.getParameter<double>( "JetPtCut" ) ),
  JetEtaCut( iConfig.getParameter<double>( "JetEtaCut" ) ),
  //MinNJets( iConfig.getParameter<unsigned int>( "MinNJets" ) ),
  
  BTagWPL( iConfig.getParameter<double>( "BTagWPL" ) ),
  BTagWPM( iConfig.getParameter<double>( "BTagWPM" ) ),
  BTagWPT( iConfig.getParameter<double>( "BTagWPT" ) ),
  BTagAlgo( iConfig.getParameter<string>( "BTagAlgo" ) ),
  //MinNBJets( iConfig.getParameter<unsigned int>( "MinNBJets" ) ),
  rndJER(new TRandom3( 13611360 ) )
{
  all_tokens.push_back( token );
  if( iConfig.exists( "MoreInputs" ) ){
    std::vector<edm::InputTag> moreinputs = iConfig.getParameter< std::vector<edm::InputTag> >( "MoreInputs" );
    for( auto input : moreinputs ){
      edm::EDGetTokenT< flashggJetCollection > _token = iC.consumes< flashggJetCollection >( input ) ;
      all_tokens.push_back( _token );
    }
  }

  // cout << "Jet Reader " << all_tokens.size() ;
  // for(auto tkn : all_tokens )
  //   cout << "  " << tkn.index() ;
  // cout << endl;
  

  // BTagCuts = iConfig.getParameter<std::vector<int> > ( "BTagCuts" );
  // if(BTagCuts.size() > 2){
  //   std::cout<<"FATAL ERROR: The current code accepts up to two WP's, one for selection one for veto"<<std::endl;
  //   return;
  // } else if(BTagCuts.size() < 2) 
  //   BTagCuts.push_back(-1);

  // if(BTagCuts[0] == 0) {
  //   BTagCut = BTagWPL;
  // } else if (BTagCuts[0] == 1) {
  //   BTagCut = BTagWPM ;
  // } else if (BTagCuts[0] == 2) {
  //   BTagCut = BTagWPT ;
  // }
  
  if( !IsData ){
    btw0L = new BTagWeight("CSVv2", 0 , SetupDir, 0 , 0 , BTagWPL, BTagWPM, BTagWPT,-1);
    btw0M = new BTagWeight("CSVv2", 1 , SetupDir, 0 , 0 , BTagWPL, BTagWPM, BTagWPT,-1);
    btw0T = new BTagWeight("CSVv2", 2 , SetupDir, 0 , 0 , BTagWPL, BTagWPM, BTagWPT,-1);
    btw1L = new BTagWeight("CSVv2", 0 , SetupDir, 1 , 1 , BTagWPL, BTagWPM, BTagWPT,-1);
    btw1M = new BTagWeight("CSVv2", 1 , SetupDir, 1 , 1 , BTagWPL, BTagWPM, BTagWPT,-1);
    btw1T = new BTagWeight("CSVv2", 2 , SetupDir, 1 , 1 , BTagWPL, BTagWPM, BTagWPT,-1);
    btw2L = new BTagWeight("CSVv2", 0 , SetupDir, 2 , 2 , BTagWPL, BTagWPM, BTagWPT,-1);
    btw2M = new BTagWeight("CSVv2", 1 , SetupDir, 2 , 2 , BTagWPL, BTagWPM, BTagWPT,-1);
    btw2T = new BTagWeight("CSVv2", 2 , SetupDir, 2 , 2 , BTagWPL, BTagWPM, BTagWPT,-1);
    btw1M0L = new BTagWeight("CSVv2", 1 , SetupDir, 1 , 1 , BTagWPL, BTagWPM, BTagWPT,0 , 0 , 0);
    btw1T0L = new BTagWeight("CSVv2", 2 , SetupDir, 1 , 1 , BTagWPL, BTagWPM, BTagWPT,0 , 0 , 0);
    btw1T0M = new BTagWeight("CSVv2", 2 , SetupDir, 1 , 1 , BTagWPL, BTagWPM, BTagWPT,1 , 0 , 0);
    allBTWs = {btw0L , btw0M, btw0T , btw1L , btw1M , btw1M0L , btw1T , btw1T0L, btw1T0M , btw2L , btw2M , btw2T};
    allWs = {&W0L , &W0M, &W0T , &W1L , &W1M , &W1M0L , &W1T , &W1T0L, &W1T0M , &W2L , &W2M , &W2T};

    if(ApplyJER){
      t_Rho_ = (iC.consumes<double>( edm::InputTag( "fixedGridRhoFastjetAll" ) ) );
      resolution = JME::JetResolution( SetupDir + "/MCJetPtResolution.txt" );
      resolution_sf = JME::JetResolutionScaleFactor(SetupDir + "/MCJetSF.txt");
    }
  }
}

#include <stdexcept>
#include <algorithm> 
//exactly one b-jet is requeste, so only the selectedJet collection should be searched for

const flashggJetCollection* flashggJetReader::GetAllJets(){
  return handle.product() ;
}


flashggJetReader::SelectionStatus flashggJetReader::Read(const edm::Event& iEvent , const DiPhotonCandidate* diPhoton ){ // , const flashgg::Muon* mu ){

  // cout << diPhoton->jetCollectionIndex() << "Jet Reader " << all_tokens.size() ;
  // for(auto tkn : all_tokens )
  //   cout << "  " << tkn.index() ;
  // cout << endl;

  token = all_tokens[diPhoton->jetCollectionIndex()];

  BaseEventReader< flashggJetCollection >::Read( iEvent );
  //W = 1.0;

  if( (!IsData) && ApplyJER ){
    iEvent.getByToken(t_Rho_ ,rho);
    Rho = *rho;
  }

  bVals.clear(); etaVals.clear() ; ptVals.clear() ;

  selectedJets.clear();
  nLB = nMB = nTB = 0;
  //selectedBJets.clear();
  selectedJetsEtaLT24.clear();

  for ( flashgg::Jet j : *handle) {
    if( !IsData && ApplyJER ){
      float pt = JER(j , Rho);
      reco::Candidate::LorentzVector tmp(j.p4());
      tmp.SetPx( tmp.X()*pt/tmp.Pt() );
      tmp.SetPy( tmp.Y()*pt/tmp.Pt() );
      j.setP4(tmp);
    }
    if (j.pt() < JetPtCut) continue;
    if ( fabs(j.eta() ) > JetEtaCut ) continue;
    if ( !JetLooseID( j ) ) continue;
    
    double dr0 = reco::deltaR( j.p4() , diPhoton->leadingPhoton()->p4() );
    double dr1 = reco::deltaR( j.p4() , diPhoton->subLeadingPhoton()->p4() );
    //double dr2 = reco::deltaR( j.p4() , mu->p4() );
    if( dr0 < 0.4 || dr1 < 0.4 ) continue ;
    
    //bool isB = false;
 
    if ( fabs(j.eta() ) < 2.4 ){
      selectedJetsEtaLT24.push_back(j);
      
      float btagval = j.bDiscriminator( BTagAlgo );
      if( btagval > BTagWPL )
	nLB ++;
      if( btagval > BTagWPM )
	nMB ++;
      if( btagval > BTagWPT )
	nTB ++;
    //   if( isB )
    // 	selectedBJets.push_back( j );
    }

    // if( !isB )
    selectedJets.push_back(j);
    int index = ( selectedJets.size() - 1 ) ;
    bVals.push_back( make_pair( j.bDiscriminator( BTagAlgo ) , index ) );
    ptVals.push_back( make_pair( j.pt() , index ) );
    etaVals.push_back( make_pair( fabs( j.eta() ) , index ) );
  }

  //ptSort<flashgg::Jet> mySort; 
  //std::sort(selectedJets.begin(),selectedJets.end(),mySort);
  //std::sort(selectedBJets.begin(),selectedBJets.end(),mySort);
    
  // if( (selectedJets.size()+selectedBJets.size())  < MinNJets ) return flashggJetReader::NotEnoughJets ;
  // if( selectedBJets.size() != MinNBJets ) return flashggJetReader::NotEnoughBJets;
  //cout << "fromJet : " ;
  if(!IsData)
    for(uint i =0 ; i < allBTWs.size(); i++){
      double ww = allBTWs[i]->weight(selectedJetsEtaLT24);
      //cout << ww << " " ;
      *(allWs[i]) = ww ;
    }
  //cout << endl;
  std::sort( bVals.rbegin() , bVals.rend() );
  std::sort( etaVals.rbegin() , etaVals.rend() );
  std::sort( ptVals.rbegin() , ptVals.rend() );

  // cout << "bVals : " << endl;
  // for( unsigned int i = 0 ; i < bVals.size() ; i++ )
  //   cout << "\t" << i << ":" << bVals[i].first << "," << bVals[i].second << endl;
  // cout << "etaVals : "<< endl ;
  // for( unsigned int i = 0 ; i < etaVals.size() ; i++ )
  //   cout << "\t" << i << ":" << etaVals[i].first << "," << etaVals[i].second << endl;
  // cout << "ptVals : " << endl;
  // for( unsigned int i = 0 ; i < ptVals.size() ; i++ )
  //   cout << "\t" << i << ":" << ptVals[i].first << "," << ptVals[i].second << endl;

  return flashggJetReader::Pass;
}

float flashggJetReader::JER( flashgg::Jet jet , double rho , int syst ){
  JME::JetParameters parameters_1;
  parameters_1.setJetPt(jet.pt());
  parameters_1.setJetEta(jet.eta());
  parameters_1.setRho( rho );
  float sf = resolution_sf.getScaleFactor(parameters_1);

  const reco::GenJet*  genjet =  jet.genJet ();
  float ret = jet.pt();
  if( genjet != NULL && genjet->pt() > 0 ){
    ret = max(0., genjet->pt() + sf*( jet.pt() - genjet->pt() ) );
  }else{
    float r = resolution.getResolution(parameters_1);
    ret = rndJER->Gaus( jet.pt() , r*sqrt( sf*sf - 1) );
  }
  return ret;
}

bool flashggJetReader::JetLooseID( flashgg::Jet j ){
  float NHF = j.neutralHadronEnergyFraction ();
  float NEMF = j.neutralEmEnergyFraction ();
  int NumConst = j.numberOfDaughters ();
  float eta = j.eta();
  float CHF = j.chargedHadronEnergyFraction ( ) ;
  float CHM = j.chargedMultiplicity ();
  float CEMF = j.chargedEmEnergyFraction ();
  int NumNeutralParticle = j.neutralMultiplicity ( );
  bool looseJetID1 = (NHF<0.99 && NEMF<0.99 && NumConst>1) && ((abs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.99) || abs(eta)>2.4) && abs(eta)<=3.0 ;
  bool looseJetID2 = (NEMF<0.90 && NumNeutralParticle>10 && abs(eta)>3.0 ) ;
  
  return looseJetID1 || looseJetID2 ;
}
