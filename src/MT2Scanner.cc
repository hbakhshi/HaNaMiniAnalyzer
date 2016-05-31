#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/MT2Scanner.h"
#include "tHqAnalyzer/HaNaMiniAnalyzer/interface/lester_mt2_bisect.h"
#include <cmath>


MT2Scanner::MT2Scanner(  const edm::ParameterSet& pset ) : 
  MT2Scanner::MT2Scanner( 
			 pset.getParameter<string>("Name") ,
			 pset.getParameter<int>("NBinsPhi") ,
			 pset.getParameter<double>("PtMin") ,
			 pset.getParameter<double>("PtMax") ,
			 pset.getParameter<int>("NBinsPt") ,
			 pset.getParameter<double>("VisMass") ,
			 pset.getParameter<double>("InVisMass") ,
			 pset.getParameter<double>("Precision") ,
			 pset.getParameter<bool>("MakeTree"),
			 pset.getParameter<int>("MT2_NBins") ,
			 pset.getParameter<double>("MT2_Min") ,
			 pset.getParameter<double>("MT2_Max") ,
			 pset.getParameter<string>("InputFile") )
{
}

MT2Scanner::MT2Scanner( string name ,  int _nbins_phi , double _pt_min ,double _pt_max , int _nbins_pt ,double _vis_mass, double _invis_mass , double _precision , bool makeTree , int mt2Nbins, double mt2Min , double mt2Max , string InputFileName ):
  Name(name),
  MakeTree(makeTree),
  nbins_phi( _nbins_phi ),
  nbins_pt( _nbins_pt ),
  ntotal_bins( nbins_pt*nbins_phi ),
  mt2_nbins( mt2Nbins ),
  pt_min( _pt_min ),
  pt_max( _pt_max),
  vis_mass( _vis_mass ),
  invis_mass( _invis_mass ),
  precision(_precision),
  mt2_start( mt2Min ),
  mt2_end(mt2Max)
{
  asymm_mt2_lester_bisect::disableCopyrightMessage();

  py_bins = new double[ ntotal_bins ];
  px_bins = new double[ ntotal_bins ];

  pt_bins  = new double[ ntotal_bins ];
  phi_bins = new double[ ntotal_bins ];


  double dphi = (2*M_PI)/double(nbins_phi);
  double dpt  = (pt_max - pt_min)/double(nbins_pt);
  double phi_step = (dphi/2.0) - M_PI ;
  double pt_step = pt_min + (dpt/2.0);

  TFileDirectory subDir;
  TDirectory* iSubDir;
  if( InputFileName == "" ){
    edm::Service<TFileService> fs;
    mainDir = fs->mkdir( name.c_str() );

    if( MakeTree ){
      tree = mainDir.make<TTree>( ("tree_" + name).c_str() , name.c_str() );
      tree_pt = 0 ; tree_phi = 0 ; tree_mt2 = 0 ;
      tree->Branch("pt" , &tree_pt );
      tree->Branch("phi" , &tree_phi );
      tree->Branch("mt2" , &tree_mt2 );
    }

    subDir = mainDir.mkdir( "Histos" );
    InputFile = NULL;
  }else{
    InputFile = TFile::Open( InputFileName.c_str() , "READ" );
    iMainDir = InputFile->GetDirectory( name.c_str() );
    iSubDir = iMainDir->GetDirectory("Histos" );
    MakeTree = false;
  }
  int count = 0;
  for(int i = 0 ; i < nbins_phi ; i++){
    for(int j = 0 ; j < nbins_pt ; j++){
      pt_bins[count] = pt_step;
      phi_bins[count] = phi_step;
      px_bins[count] = pt_step*cos( phi_step );
      py_bins[count] = pt_step*sin( phi_step );
      
      TString histo_name = TString::Format( "%d_histo_pt_%d_phi_%d" , count , i , j );
      TString histo_title = TString::Format( "mt2 when met is modified with pt=%f , dphi=%f" , pt_step , phi_step );
      TH1* histo ;
      if( InputFileName == "" )
	histo = subDir.make<TH1D>( histo_name , histo_title , mt2_nbins , mt2_start , mt2_end );
      else{
	histo = (TH1*)(iSubDir->Get( histo_name ));
	histo->Scale( 1.0/histo->Integral() );
      }
      all_histos.push_back( histo );
      
      pt_step += dpt;
      count++;
    }
    phi_step += dphi ;
    pt_step = pt_min + (dpt/2.0);
  }

  if( count != ntotal_bins )
    std::cout << "(warning) something is wrong here : two counting don't match, count == " << count << " while ntotal_bins == " << ntotal_bins << endl;
}

MT2Scanner::~MT2Scanner(){
  delete[] pt_bins;
  delete[] phi_bins;
  delete[] py_bins;
  delete[] px_bins;
}

double MT2Scanner::Calculate( double vis1_px , double vis1_py , double vis2_px , double vis2_py , double met_x , double met_y ){
  double mod_met_x , mod_met_y , mt2 ;
  double probability = 1.0;


  //rotate to have met direction as x axis
  double met_size = hypot( met_x , met_y );
  double cos_metphi = met_x / met_size;
  double sin_metphi = met_y / met_size;

  met_x = met_size;
  met_y = 0.0 ;

  double tmp_rotation = cos_metphi* vis1_px + sin_metphi * vis1_py ;
  vis1_py = cos_metphi*vis1_py - sin_metphi*vis1_px ;
  vis1_px = tmp_rotation ;

  tmp_rotation = cos_metphi* vis2_px + sin_metphi * vis2_py ;
  vis2_py = cos_metphi*vis2_py - sin_metphi*vis2_px ;
  vis2_px = tmp_rotation ;
  // end of rotations


  for(int i = 0 ; i < ntotal_bins ; i++){
    mod_met_x = met_x - px_bins[i];
    mod_met_y = met_y - py_bins[i];

    mt2 = asymm_mt2_lester_bisect::get_mT2(
					   vis_mass, vis1_px , vis1_py ,
					   vis_mass, vis2_px , vis2_py ,
					   mod_met_x , mod_met_y ,
					   invis_mass , invis_mass ,
					   precision );

    if( mt2 < 0 )
      cout << "negative mt2" <<endl;

    if( InputFile ){
      probability *= all_histos[i]->GetBinContent(
						  all_histos[i]->FindBin( mt2 ) );
    }else{
      all_histos[i]->Fill( mt2 );
      if(MakeTree){
	tree_pt  = pt_bins[i];
	tree_phi = phi_bins[i];
	tree_mt2 = mt2;
	tree->Fill();
      }
    }
  }
  return probability;
}

void MT2Scanner::Finalize(){
  TFileDirectory sumDir = mainDir.mkdir("Summary");
  TH2D* hmax_vals = sumDir.make<TH2D>("max_vals" , "max" ,  nbins_pt , pt_min , pt_max , nbins_phi , -M_PI , M_PI );
  TH2D* havg_vals = sumDir.make<TH2D>("agv_vals" , "avg" , nbins_pt , pt_min , pt_max , nbins_phi , -M_PI , M_PI );
  TH2D* hstdev_vals = sumDir.make<TH2D>("stdev_vals" , "std_dev" , nbins_pt , pt_min , pt_max , nbins_phi , -M_PI , M_PI );
  TH2D* hmax_vals_m_top = sumDir.make<TH2D>("max_vals_m_top" , "max-172" , nbins_pt , pt_min , pt_max , nbins_phi , -M_PI , M_PI );

  for(int i = 0 ; i < ntotal_bins ; i++){
    int bin = hmax_vals->FindBin( pt_bins[i] , phi_bins[i] );
    TH1* hnorm = (TH1*)(all_histos[i]->Clone("Normalized")) ;
    hnorm->Scale( 1.0/hnorm->Integral() );
    double endpoint = hnorm->GetBinCenter( hnorm->FindLastBinAbove(0.005) ) ;
    hmax_vals->SetBinContent( bin , endpoint);
    havg_vals->SetBinContent( bin , 
			      all_histos[i]->GetMean() );
    hstdev_vals->SetBinContent( bin , 
				all_histos[i]->GetStdDev() ) ;
    hmax_vals_m_top->SetBinContent( bin , 
				    endpoint - 172.0 );
    delete hnorm;
  }
}
