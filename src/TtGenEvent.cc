#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/TtGenEvent.h"
#include <iostream>

TtGenEventDiLep::~TtGenEventDiLep(){

}

TtGenEventDiLep::TtGenEventDiLep( const TtGenEventDiLep* ttbar , bool JustTransverse  ){
  isSet = ttbar->isSet;
  if( !isSet )
    return ;

  if( !JustTransverse ){
    Top = ttbar->Top;
    TopBar = ttbar->TopBar;
  }

  B = ttbar->B;
  BBar = ttbar->BBar ;
  L = ttbar->L;
  LBar = ttbar->LBar;
  MET = ttbar->MET;
  DDgenMET = ttbar->DDgenMET;
}
TtGenEventDiLep::TtGenEventDiLep( const std::vector<reco::GenParticle>* gen  ) :
  MET(0.0 , 0.0 ),
  DDgenMET(0.0 , 0.0)
{
  int top = getLastCopy( gen , 6 );
  int topbar = getLastCopy( gen , -6 );

  int wm = getLastCopy( gen , -24 , -6 , true , true );
  int wp = getLastCopy( gen , 24 , 6 , true , true);

  int lm = getLastCopy( gen , 11 , -24 );
  int neutrinobar = getLastCopy( gen , -12 , -24 );

  int lp = getLastCopy( gen , -11 , 24 );
  int neutrino = getLastCopy( gen , 12 , 24 );

  if(lm < 0){
    lm = getLastCopy( gen , 13 , -24 );
    neutrinobar = getLastCopy( gen , -14 , -24 );
  }
  if(lp < 0){
    lp = getLastCopy( gen , -13 , 24 );
    neutrino = getLastCopy( gen , 14 , 24 );
  }


  if(lm < 0){
    lm = getLastCopy( gen , 13 , -24 , true , true);
    neutrinobar = getLastCopy( gen , -14 , -24  , true , true);
  }
  if(lp < 0){
    lp = getLastCopy( gen , -13 , 24  , true , true);
    neutrino = getLastCopy( gen , 14 , 24  , true , true);
  }

  if(lm < 0){
    lm = getLastCopy( gen , 11 , -24 , true , true);
    neutrinobar = getLastCopy( gen , -12 , -24  , true , true);
  }
  if(lp < 0){
    lp = getLastCopy( gen , -11 , 24  , true , true);
    neutrino = getLastCopy( gen , 12 , 24  , true , true);
  }


  int b = getLastCopy( gen , 5 , 6 , true );
  if( b < 0 )
    b = getLastCopy( gen , 5 , 6 , true , true );

  int bbar = getLastCopy( gen , -5 , -6 , true );
  if( bbar < 0)
    bbar = getLastCopy( gen , -5 , -6 , true , true );

  if( lm < 0 || lp < 0 ){
    isSet = false;
    return;
  }
  
  //std::cout << top << "->" << b << "+(" << wm << "->" << lm << "," << neutrinobar << ") ,,,  " ;
  //std::cout << topbar << "->" << bbar << "+(" << wp << "->" << lp << "," << neutrino << ")" << std::endl ;

  TopBar.Set(
	     &(gen->at( topbar )),
	     &(gen->at( wp )),
	     &(gen->at(bbar)),
	     &(gen->at( lp )),
	     &(gen->at( neutrino )) );
 
  Top.Set(
	  &(gen->at( top )),
	  &(gen->at( wm )),
	  &(gen->at( b )),
	  &(gen->at( lm )),
	  &(gen->at( neutrinobar )) );

  isSet = true;
}

void TtGenEventDiLep::SetTransverseInfo(double DMMetX , double DMMetY ){
  //this method sets the transvers info of the event and rotate everything so the direction of l is the x-axis
  L.Set( Top.Lepton->pt() , 0.0 );
  double phi = -(Top.Lepton->phi());

  LBar.Set( TopBar.Lepton->px() , TopBar.Lepton->py() );
  LBar = LBar.Rotate( phi );

  B.Set( Top.b->px() , Top.b->py() );
  B = B.Rotate( phi );

  BBar.Set( TopBar.b->px() , TopBar.b->py() );
  BBar = BBar.Rotate( phi );

  MET.Set(  TopBar.Neutrino->px()+Top.Neutrino->px()+DMMetX , TopBar.Neutrino->py()+Top.Neutrino->py()+DMMetY );
  MET = MET.Rotate( phi );

  DDgenMET.Set( DMMetX , DMMetY );
  if( DDgenMET.Mod() != 0.0 ){
    DDgenMET = DDgenMET.Rotate( phi );
  }
}

TVector2 TtGenEventDiLep::getNominalMET() const{
  TVector2 sum = B+BBar+L+LBar ;
  return TVector2( -(sum.Px()) , -(sum.Py()) );
}

bool TtGenEventDiLep::IsTransverseConsistent( TtGenEventDiLep* ref , double lep_phi_res , double lep_e_res , double b_phi_res , double b_e_res  ){
  if( fabs( ref->L.Mod() - L.Mod() ) > (lep_e_res*L.Mod()) )
    return false;

  if( fabs( ref->LBar.Mod() - LBar.Mod() ) > (lep_e_res*LBar.Mod()) )
    return false;
  
  if( fabs( ref->LBar.DeltaPhi( LBar ) ) > lep_phi_res )
    return false;

  if( fabs( ref->BBar.Mod() - BBar.Mod() ) > (b_e_res*BBar.Mod()) )
    return false;
  
  if( fabs( ref->BBar.DeltaPhi( BBar ) ) > b_phi_res )
    return false;

  if( fabs( ref->B.Mod() - B.Mod() ) > (b_e_res*B.Mod()) )
    return false;
  
  if( fabs( ref->B.DeltaPhi( B ) ) > b_phi_res )
    return false;
  
  return true;
}

int TtGenEventDiLep::getLastCopy(const std::vector<reco::GenParticle>* gens, int pdgId , int parentId , bool beforeFSR , bool noCheckLastCopy ){
  int index=-1;
  for(auto genPart : *gens ){
    index ++ ;
    int pdgid = genPart.pdgId();
    if( pdgid != pdgId )
      continue;
    if( parentId != 0 )
      if( genPart.mother()->pdgId() != parentId )
	continue;
    if( noCheckLastCopy )
      return index;
    else if( beforeFSR ){
      if( genPart.isLastCopyBeforeFSR() )
	return index;
    }else if( genPart.isLastCopy() )
      return index;
  }
  return -1;
}
