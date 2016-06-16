#include "../interface/Histograms.h"

Histogram1D::Histogram1D( TString samplename , TString propname , int nbins , double from , double to , unsigned int nW) : Histogram1D::base( samplename ,propname , nW){
  for(unsigned int i=0 ; i < nW ; i++)
    theHists.push_back( subDir.make<TH1D>( propname + "_" + samplename + "_" + std::to_string(i) , propname , nbins , from , to ) );
}

Histogram1D::Histogram1D( TString samplename , TString propname , int nbins , double* bins , unsigned int nW) : Histogram1D::base( samplename ,propname , nW) {
  theHists.push_back( subDir.make<TH1D>( propname + "_" + samplename , propname , nbins , bins ) );
}

void Histogram1D::Fill( double v , double w ){
  for( auto hh : theHists )
    hh->Fill( v , w );
}

void Histogram1D::Fill( double v , std::valarray<double> w ){
  double ww;
  for(unsigned int i=0 ; i < NW ; i++ ){
    ww = 1.0;
    if( w.size() > i )
      ww = w[i];
    theHists[i]->Fill( v , ww );
  }
}


Histogram2D::Histogram2D( TString samplename , TString propname , int nbins , double from , double to , int nbins_y , double from_y , double to_y , unsigned int nW ) : Histogram2D::base( samplename ,propname , nW){
  for(unsigned int i=0 ; i < nW ; i++)
    theHists.push_back( subDir.make<TH2D>( propname + "_" + samplename  + "_" + std::to_string(i) , propname , nbins , from , to, nbins_y , from_y , to_y ) );
}

void Histogram2D::Fill( double x , double y , double w ){
  for( auto hh : theHists )
    hh->Fill( x , y , w );
}

void Histogram2D::Fill( double x , double y , std::valarray<double> w ){
  double ww;
  for(unsigned int i=0 ; i < NW ; i++ ){
    ww = 1.0;
    if( w.size() > i )
      ww = w[i];
    theHists[i]->Fill( x , y , ww );
  }
}
