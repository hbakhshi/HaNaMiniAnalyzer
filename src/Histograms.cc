#include "../interface/Histograms.h"

Histogram1D::Histogram1D( TString samplename , TString propname , int nbins , double from , double to ) : Histogram1D::base( samplename ,propname){
  theHist = subDir.make<TH1D>( propname + "_" + samplename , propname , nbins , from , to );
  theHistNoW = subDir.make<TH1D>( propname + "_NoW_" + samplename , propname , nbins , from , to );
}

Histogram1D::Histogram1D( TString samplename , TString propname , int nbins , double* bins) : Histogram1D::base( samplename ,propname) {
  theHist = subDir.make<TH1D>( propname + "_" + samplename , propname , nbins , bins );
  theHistNoW = subDir.make<TH1D>( propname + "_NoW_" + samplename , propname , nbins , bins );
}

void Histogram1D::Fill( double v , double w , double , double ){
  theHist->Fill( v , w );
  theHistNoW->Fill( v , 1.0 ) ; //w == 0 ? 1 : (w/fabs(w)) );
}


Histogram2D::Histogram2D( TString samplename , TString propname , int nbins , double from , double to , int nbins_y , double from_y , double to_y ) : Histogram2D::base( samplename ,propname){
  theHist = subDir.make<TH2D>( propname + "_" + samplename , propname , nbins , from , to, nbins_y , from_y , to_y );
  theHistNoW = subDir.make<TH2D>( propname + "_NoW_" + samplename , propname , nbins , from , to , nbins_y , from_y , to_y );
}

void Histogram2D::Fill( double x , double y , double w , double ){
  theHist->Fill( x , y , w );
  theHistNoW->Fill( x , y , 1.0 ) ; //w == 0 ? 1 : (w/fabs(w)) );
}
