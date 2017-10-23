from tHqAnalyzer.HaNaMiniAnalyzer.Property import *
from ROOT import TFile, TH1

fSignal = TFile.Open("out_allTopSamples_mvaonly.root")
hsignal_name = "SR/PlottedVars/GGmva/samples/%s_SR_GGmva_0"
signal_ = fSignal.Get( hsignal_name % ("THQ") )
signal_.SetName("Signal")
THQ = fSignal.Get( hsignal_name % ("THQ") )
THQ.Scale( 26.3081480775493 )
THW = fSignal.Get( hsignal_name % ("THW") )
THW.Scale( 21.7407292684282 )
signal_.Add(THQ, THW  )
TTH = fSignal.Get( hsignal_name % ("TTH") )
TTH.Scale( 2.30328734701009 )
signal_.Add( TTH )
VH = fSignal.Get( hsignal_name % ("VH") )
VH.Scale( 2.30328734701009 )
signal_.Add( VH )

fBkg = TFile.Open("out_plots_fakeprompts.root")
hBkg = fBkg.Get("diphoMVA/NormMG_GG")

prop = Property("digamma_id" , [hBkg] , None , [signal_] , [] , MCOnly = True )
soverb = prop.Significance( signal_ , hBkg , 1 )
sosqrtb = prop.Significance( signal_ , hBkg , 2 )
sosqrtbdb2 = prop.Significance( signal_ , hBkg , 3 )
lnsosqrtb = prop.Significance( signal_ , hBkg , 4 )
bregsigs = {}
for breg in range(1, 50 , 4 ):
    bregsigs[ breg ] = prop.Significance( signal_ , hBkg , 6 , breg )
    
fSig = TFile.Open("fSignificance.root" , "recreate")
soverb.Write()
sosqrtbdb2.Write()
sosqrtb.Write()
lnsosqrtb.Write()
signal_.Write()
hBkg.Write()
THQ.Write()
THW.Write()
TTH.Write()
VH.Write()
for breg in bregsigs:
    bregsigs[breg].Write()
    
fSig.Close()
