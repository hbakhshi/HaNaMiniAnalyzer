#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/flashggJetReader.h"


flashggJetReader::flashggJetReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC , bool isData , string SetupDir) :
  BaseEventReader< flashggJetCollection >( iConfig , &iC ),
  IsData( isData ),
  ApplyJER( iConfig.getParameter<bool>( "ApplyJER" ) ),
  JetPtCut( iConfig.getParameter<double>( "JetPtCut" ) ),
  JetEtaCut( iConfig.getParameter<double>( "JetEtaCut" ) ),
  MinNJets( iConfig.getParameter<unsigned int>( "MinNJets" ) ),
  
  BTagWPL( iConfig.getParameter<double>( "BTagWPL" ) ),
  BTagWPM( iConfig.getParameter<double>( "BTagWPM" ) ),
  BTagWPT( iConfig.getParameter<double>( "BTagWPT" ) ),
  BTagAlgo( iConfig.getParameter<string>( "BTagAlgo" ) ),
  MinNBJets( iConfig.getParameter<unsigned int>( "MinNBJets" ) ),
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
  

  BTagCuts = iConfig.getParameter<std::vector<int> > ( "BTagCuts" );
  if(BTagCuts.size() > 2){
    std::cout<<"FATAL ERROR: The current code accepts up to two WP's, one for selection one for veto"<<std::endl;
    return;
  } else if(BTagCuts.size() < 2) 
    BTagCuts.push_back(-1);
  
  if( !IsData ){
    btw = new BTagWeight("CSVv2", BTagCuts[0], SetupDir, MinNBJets , 1000 , BTagWPL, BTagWPM, BTagWPT,BTagCuts[1]);

    if(ApplyJER){
      t_Rho_ = (iC.consumes<double>( edm::InputTag( "fixedGridRhoFastjetAll" ) ) );
      resolution = JME::JetResolution( SetupDir + "/MCJetPtResolution.txt" );
      resolution_sf = JME::JetResolutionScaleFactor(SetupDir + "/MCJetSF.txt");
    }
  }
}

const flashggJetCollection* flashggJetReader::GetAllJets(){
  return handle.product() ;
}


flashggJetReader::SelectionStatus flashggJetReader::Read(const edm::Event& iEvent , const DiPhotonCandidate* diPhoton ){

  // cout << diPhoton->jetCollectionIndex() << "Jet Reader " << all_tokens.size() ;
  // for(auto tkn : all_tokens )
  //   cout << "  " << tkn.index() ;
  // cout << endl;

  token = all_tokens[diPhoton->jetCollectionIndex()];

  BaseEventReader< flashggJetCollection >::Read( iEvent );
  W = 1.0;

  if( (!IsData) && ApplyJER ){
    iEvent.getByToken(t_Rho_ ,rho);
    Rho = *rho;
  }

  selectedJets.clear();
  selectedBJets.clear();

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
    if( dr0 < 0.4 || dr1 < 0.4 ) continue ;
    
    selectedJets.push_back(j);
 
    if ( fabs(j.eta() ) < 2.4 ){
      float btagval = j.bDiscriminator( BTagAlgo );
    
      if(BTagCuts[0] == 0) {
	if(btagval > BTagWPL) selectedBJets.push_back(j);
      } else if (BTagCuts[0] == 1) {
	if(btagval > BTagWPM) selectedBJets.push_back(j);
      } else if (BTagCuts[0] == 2) {
	if(btagval > BTagWPT) selectedBJets.push_back(j);
      }
    }
  }
  
  ptSort<flashgg::Jet> mySort; 
  std::sort(selectedJets.begin(),selectedJets.end(),mySort);
  std::sort(selectedBJets.begin(),selectedBJets.end(),mySort);
    
  if( selectedJets.size()  < MinNJets ) return flashggJetReader::NotEnoughJets ;
  if( selectedBJets.size() < MinNBJets ) return flashggJetReader::NotEnoughBJets;
  if(!IsData)
    W = btw->weight(*handle);
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
