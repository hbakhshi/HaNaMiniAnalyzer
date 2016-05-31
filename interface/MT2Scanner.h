#ifndef MT2Scanner_H
#define MT2Scanner_H

#include "TH3.h"
#include "TH1.h"
#include "TH2.h"
#include "TTree.h"
#include <string>
#include <vector>
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

using namespace std;

class MT2Scanner{

public:
  MT2Scanner( string name, int _nbins_phi , double pt_min ,double pt_max , int _nbins_pt , double vis_mass , double invis_mass , double precision , bool makeTree , int mt2Nbins, double mt2Min , double mt2Max , string InputFileName );
  MT2Scanner(  const edm::ParameterSet& pset );

  ~MT2Scanner();
  
  double Calculate( double vis1_px , double vis1_py , double vis2_px , double vis2_py , double met_x , double met_y );
  void Finalize();

  std::vector< TH1* > all_histos;
  TTree* tree;
  double tree_pt , tree_phi , tree_mt2 ;
private:
  string Name;
  bool MakeTree;
  int nbins_phi , nbins_pt , ntotal_bins , mt2_nbins  ;
  double pt_min , pt_max , vis_mass, invis_mass , precision;
  double mt2_start , mt2_end;

  double* pt_bins;
  double* phi_bins;
  double* py_bins;
  double* px_bins;

  TFileDirectory mainDir;
  TDirectory* iMainDir;
  TFile* InputFile ; 
};


#endif
