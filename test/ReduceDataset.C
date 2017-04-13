#include "RooWorkspace.h"
#include "RooAbsData.h"
#include "TFile.h"
#include "RooArgSet.h"
#include "RooArgList.h"
#include "RooFormulaVar.h"

using namespace RooFit;
using namespace std;

TCanvas* theCanvas;

void ReduceDataset(TString infile){

  RooRealVar mhgg("CMS_hgg_mass", "Mass", 100, 200);
  mhgg.setBins(20);
   
  TFile* fIn = TFile::Open(infile);
  TObject* obj = fIn->Get("tagsDumper/cms_hgg_13TeV") ;

  // if( obj == NULL )
  //   obj = fIn->Get("cms_hgg_13TeV") ;
  if( obj == NULL ){
    cout << "no workspace found, exiting" <<endl;
    return;
  }
  RooWorkspace* ws = (RooWorkspace*) obj ;

  
  TString outFname = infile.ReplaceAll(".root" , "_reduced_nocut.root");
  TFile* fout = new TFile(outFname , "recreate");
  fout->mkdir( "tagsDumper" )->cd(); //thqLeptonicTagDumper
  RooWorkspace* final_ws = new RooWorkspace( ws->GetName() ) ;

  for(auto ds : ws->allData() ){
    //RooAbsData* ds = *(ws->allData().begin());
    // RooDataHist *binnedDS = new RooDataHist("binnedDS","binnedDS",RooArgSet(mhgg),*ds);
    // RooHistPdf mggPDF("mggPDF","mggPDF",mhgg,*binnedDS);

    // theCanvas = new TCanvas("c" , "c" );
    // RooPlot* frame = mhgg.frame(Title("title"));
    // mggPDF.plotOn( frame );
  
    std::string cutFinal = "(CMS_hgg_mass > 100 && CMS_hgg_mass < 180) && (diphoMVA > -0.4)&&(n_jets >= 2)&&(n_M_bjets==1)&&(MET > 30)&&(LeptonType == 1 || LeptonType == 2)&&MVA_Medium > 0 ";
    RooArgList formulaVars;

    std::vector<std::string> varsToKeep = {"CMS_hgg_mass", "diphoMVA" ,  "bTagWeight",
					 "vtxprob","ptbal","ptasym","logspt2","p2conv","nconv","vtxmva","vtxdz","vtx_x","vtx_y","vtx_z","gv_x","gv_y","gv_z",
					 "dipho_sumpt","dipho_cosphi","dipho_mass","dipho_pt","dipho_phi","dipho_eta","dipho_PtoM","cosphi","sigmaMrvoM","sigmaMwvoM",
					 "dZ"
    }; //"weight" ,
    RooArgSet selectedVars;
  
    RooArgSet allVars = ws->allVars();
    TIterator* vIter = allVars.createIterator();
    for( int nvar=0 ; nvar < allVars.getSize() ; nvar ++){
      TObject* var = vIter->Next();
      if( ! var ){
	std::cout <<  "NuLL" << std::endl;
	continue;
      }
      if( std::find( varsToKeep.begin() , varsToKeep.end() ,  var->GetName() ) != varsToKeep.end() ){
	std::cout << var->GetName() << std::endl;
	selectedVars.add( *((RooAbsArg*)var) , true );
      }
      if( cutFinal.find( var->GetName() ) != string::npos ){
	std::cout << var->GetName() << std::endl;
	selectedVars.add( *((RooAbsArg*)var) , true );
      }
    }
  
    selectedVars.Print("ALL");

    RooAbsData* reduced = ds->reduce( selectedVars,  cutFinal.c_str() );
    final_ws->import( *reduced );
  
    // RooDataHist *binnedDS_r = new RooDataHist("binnedDS_r","binnedDS_r",RooArgSet(mhgg),*reduced);
    // final_ws->import( *binnedDS_r);
    // RooHistPdf mggPDF_r("mggPDF_r","mggPDF_r",mhgg,*binnedDS_r);
    // final_ws->import( mggPDF_r);
    // mggPDF_r.plotOn(frame);
    
    // frame->Draw();
    // final_ws->Write();
    // theCanvas->Write();
  }
  fout->Close();

  fIn->Close();
}

