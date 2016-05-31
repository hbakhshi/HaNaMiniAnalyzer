#ifndef Histograms_H
#define Histograms_H


#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1D.h"
#include "TH2D.h"

using namespace std;

template<typename T>
class BaseHistograms {
public:
  T* theHist;
  T* theHistNoW;
  TFileDirectory subDir;
  TString SampleName;
  TString PropName;
  
  BaseHistograms( TString samplename , TString propname ) :
    SampleName(samplename),
    PropName(propname) {
    edm::Service<TFileService> fs;
    subDir = fs->mkdir( PropName.Data() );
  };

  virtual void Fill( double  , double ,double , double )=0;  
};

class Histogram1D : public BaseHistograms<TH1> {
public:
  typedef BaseHistograms<TH1> base;
  Histogram1D( TString samplename , TString propname , int nbins , double from , double to );
  Histogram1D( TString samplename , TString propname , int nbins , double* bins );
  virtual void Fill( double v  , double w = 1.0 ,double y=0 , double z=0 ) override;
};

typedef Histogram1D Histograms;

class Histogram2D : public BaseHistograms<TH2> {
public:
  typedef BaseHistograms<TH2> base;
  Histogram2D( TString samplename , TString propname , int nbins , double from , double to , int nbins_y , double from_y , double to_y );
  virtual void Fill( double v  , double y  ,double w=1.0 , double z=0 ) override;
};
#endif
