from ROOT import TFile, TTree, TObject, TGraphAsymmErrors, TCanvas, kYellow, kBlack
import os
import stat
import array
import math
import shutil
from ROOT import RooWorkspace, TCanvas , RooFit, TColor, kBlue, kRed, kGreen, RooRealVar, RooConstVar, gROOT, TMath
from subprocess import call
import sys

AllNuisances = [ "CMS_hgg_nuisance_MaterialForward_13TeV",
                 "CMS_hgg_nuisance_ShowerShapeHighR9EB_13TeV", 
                 "CMS_hgg_nuisance_MCSmearHighR9EEPhi_13TeV", 
                 "CMS_hgg_nuisance_ShowerShapeHighR9EE_13TeV", 
                 "CMS_hgg_nuisance_MCSmearHighR9EBPhi_13TeV", 
                 "CMS_hgg_nuisance_ShowerShapeLowR9EE_13TeV", 
                 "CMS_hgg_nuisance_MCScaleGain1EB_13TeV", 
                 "CMS_hgg_nuisance_MaterialCentralBarrel_13TeV", 
                 "CMS_hgg_nuisance_MCSmearLowR9EERho_13TeV", 
                 "CMS_hgg_nuisance_MCSmearHighR9EBRho_13TeV", 
                 "CMS_hgg_nuisance_MCScaleGain6EB_13TeV", 
                 "CMS_hgg_nuisance_MCScaleLowR9EB_13TeV", 
                 "CMS_hgg_nuisance_MCSmearLowR9EBRho_13TeV", 
                 "CMS_hgg_nuisance_FNUFEB_13TeV", 
                 "CMS_hgg_nuisance_FNUFEE_13TeV", 
                 "CMS_hgg_nuisance_MCScaleLowR9EE_13TeV", 
                 "CMS_hgg_nuisance_MCScaleHighR9EB_13TeV", 
                 "CMS_hgg_nuisance_MaterialOuterBarrel_13TeV", 
                 "CMS_hgg_nuisance_MCSmearLowR9EEPhi_13TeV", 
                 "CMS_hgg_nuisance_MCScaleHighR9EE_13TeV", 
                 "CMS_hgg_nuisance_MCSmearLowR9EBPhi_13TeV", 
                 "CMS_hgg_nuisance_MCSmearHighR9EERho_13TeV", 
                 "CMS_hgg_nuisance_ShowerShapeLowR9EB_13TeV"]


def GetLimits( syst_name ):
    #path = "./SingleSystINWS11July/higgsCombine%s.Asymptotic.mH125.root" % (syst_name)
    path = "./%s/higgsCombine%s.Asymptotic.mH125.root" % (sys.argv[1] , syst_name)
        
    val = -100
    val1sigmap = -100
    val1sigmam = -100
    val2sigmap = -100
    val2sigmam = -100
        
    if os.path.exists( path ) :
        f = TFile.Open( path )
        if f :
            limit = f.Get("limit")
            if not type(limit) == TTree :
                val = -200
                val1sigmap = -200
                val1sigmam = -200
            else :
                for i in limit :
                    if i.quantileExpected == 0.5 :
                        val = i.limit
                    elif int(100*i.quantileExpected) in [15,16,17] :
                        val1sigmam = i.limit
                    elif int(100*i.quantileExpected) in [83,84,85] :
                        val1sigmap = i.limit
                    elif int(100*i.quantileExpected) in [2,3,4]:
                        val2sigmam = i.limit
                    elif int(100*i.quantileExpected) in [97,98,99]:
                        val2sigmap = i.limit
                    else :
                        print int(100*i.quantileExpected)
            f.Close()
        else :
            val = -400
            val1sigmap = -400
            val1sigmam = -400
    else:
        print path
        val = -300
        val1sigmap = -300
        val1sigmam = -300

    if val <= 0 :
        val /= 1000
    print syst_name, val, val1sigmam, val1sigmap, val2sigmam, val2sigmap
    return val, val1sigmam, val1sigmap, val2sigmam, val2sigmap
        

x = array.array('d')
y = array.array('d')
ex = array.array('d')
ey1sigmap = array.array('d')
ey1sigman = array.array('d')
ey2sigmap = array.array('d')
ey2sigman = array.array('d')


for syst in AllNuisances:
    systName = syst.split("_")[3]
    val, val1sigmam, val1sigmap, val2sigmam, val2sigmap = GetLimits( systName )

    print AllNuisances.index( syst ) , syst
    x.append( AllNuisances.index( syst )  )
    y.append( val )
    ex.append(0)
    ey1sigmap.append( abs(val1sigmap-val) )
    ey1sigman.append( abs(val1sigmam-val) )
    ey2sigmap.append( abs(val2sigmap-val) )
    ey2sigman.append( abs(val2sigmam-val) )

Bin = "Systematics"
canvas2 = TCanvas("sigma_bands")
graph_2sigma = TGraphAsymmErrors( len(x) , x , y , ex , ex , ey2sigman , ey2sigmap )
graph_2sigma.SetName( "GraphAsym_2SigmaBand_%s" % ( Bin ))
#graph_2sigma.SetTitle( Bin+ "(" +date+ ")" )
graph_2sigma.SetLineColor( kYellow-4)     
graph_2sigma.SetFillColor( kYellow -4)    
graph_2sigma.SetFillStyle( 1001 )         
graph_2sigma.Draw( "a3" )                 

graph_1sigma = TGraphAsymmErrors( len(x) , x , y , ex , ex , ey1sigman , ey1sigmap )
graph_1sigma.SetName( "GraphAsym_1SigmaBand_%s" % (Bin ) )
#graph_1sigma.SetTitle( Bin + "(" +date+ ")" )
graph_1sigma.SetLineColor( kGreen - 4)   
graph_1sigma.SetFillColor( kGreen -4)    
graph_1sigma.SetFillStyle( 1001 )        
graph_1sigma.Draw( "3 same" )            


graph_1sigma.SetLineColor( kBlack )
graph_1sigma.SetLineWidth( 2 )
graph_1sigma.SetLineStyle( 2 )            

graph_1sigma.SetMarkerColor( kBlack )
graph_1sigma.SetMarkerStyle( 0 ) 
graph_1sigma.Draw("lp X")                   

xax = graph_2sigma.GetXaxis()
pi = TMath.Pi()
i = 0
while i*pi/3 <= xax.GetXmax():
    systName = AllNuisances[i].split("_")[3]
    bin_index = xax.FindBin(i*pi/3)
    xax.SetBinLabel(bin_index, systName  )
    i+=1
    print i,bin_index,xax.GetBinCenter(bin_index), systName
    
canvas2.Modified()
canvas2.Update()

