from ROOT import TFile, TTree, TObject, TGraphAsymmErrors, TCanvas, kYellow, kBlack, TGraph
import os
import stat
import array
import math
import shutil
from ROOT import RooWorkspace, TCanvas , RooFit, TColor, kBlue, kRed, kGreen, RooRealVar, RooConstVar, gROOT
from subprocess import call

fEff = TFile.Open("fSignificance.root")
hTHQ = fEff.Get("THQ_SR_diphoMVA_0")
hTHW = fEff.Get("THW_SR_diphoMVA_0")
hTTH = fEff.Get("TTH_SR_diphoMVA_0")
hVH = fEff.Get("THQ_SR_diphoMVA_0").Clone("hVH")
hVH.Scale( 0.15/hVH.Integral() )

sumSignals = hTHQ.Clone("sumSignals")
sumSignals.Add( hTHW )
sumSignals.Add( hTTH )
sumSignals.Add( hVH  )

sumSignalsCumulative = sumSignals.GetCumulative(False)

def GetEff( h , bin_from ):
    integral_total = h.Integral()
    integral = h.Integral( bin_from , 100 )
    return integral/integral_total

def GetLimits( bin_from ):
    path = "./ctcv-1/higgsCombinePreselection%d.Asymptotic.mH125.root" % (bin_from)
    path = "./ctcv-1/higgsCombinePreselection%d.Asymptotic.mH125.cv1.ct-1.root" % (bin_from)
        
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
    val *= 75./66.
    print bin_from, val, val1sigmam, val1sigmap, val2sigmam, val2sigmap
    return val, val1sigmam, val1sigmap, val2sigmam, val2sigmap
        

x = array.array('d')
y = array.array('d')
ex = array.array('d')
ey1sigmap = array.array('d')
ey1sigman = array.array('d')
ey2sigmap = array.array('d')
ey2sigman = array.array('d')

ySignals = array.array('d')
yRatios = array.array('d')

for bin_id in range(7,21):
    cut = hTHQ.GetBinLowEdge( bin_id )
    all_signals = sumSignalsCumulative.GetBinContent( bin_id-1 )
    ySignals.append( all_signals )
    val, val1sigmam, val1sigmap, val2sigmam, val2sigmap = GetLimits( bin_id )
    ratio = val/all_signals
    yRatios.append( ratio )
    
    x.append( cut )
    y.append( val )
    ex.append(0)
    ey1sigmap.append( abs(val1sigmap-val) )
    ey1sigman.append( abs(val1sigmam-val) )
    ey2sigmap.append( abs(val2sigmap-val) )
    ey2sigman.append( abs(val2sigmam-val) )

Bin = "diPhoMVAOpt"    
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
 

graph_signals = TGraph( len(x) , x , ySignals )
graph_signals.SetName("GraphSignals")
graph_signals.SetTitle("Signal sum")
graph_signals.SetLineColor( kRed )
graph_signals.SetLineWidth( 2 )
graph_signals.SetLineStyle( 1 )
graph_signals.SetMarkerColor( kRed )
graph_signals.SetMarkerStyle( 20 ) 
graph_signals.Draw("lp X")        

graph_ratios = TGraph( len(x) , x , yRatios )
graph_ratios.SetName("GraphRatios")
graph_ratios.SetTitle("Ratios")
graph_ratios.SetLineColor( kRed )
graph_ratios.SetLineWidth( 2 )
graph_ratios.SetLineStyle( 1 )
graph_ratios.SetMarkerColor( kRed )
graph_ratios.SetMarkerStyle( 21 ) 
graph_ratios.Draw("lp X")        

