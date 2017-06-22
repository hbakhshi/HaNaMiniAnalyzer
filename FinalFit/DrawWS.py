from ROOT import RooWorkspace, RooDataSet, RooPlot, RooRealVar, TFile, gSystem, RooFit, TH1D, TCanvas, RooExtendPdf, RooAbsPdf, RooFitResult, kRed, kGreen , RooFormulaVar, gROOT
from SignalFit import *

from ROOT import gStyle
gStyle.SetPaintTextFormat(".2f%%")

gROOT.SetBatch(True)
gSystem.Load("~/Desktop/tHq/HiggsAnalysis/CombinedLimit/lib/libHiggsAnalysisCombinedLimit.so")

import sys

MakeFinalModel = False
DOFTest=False
#WSDIR = "/home/hbakhshi/Downloads/tHq_Georgios/output/03_17_17/signals"
WSDIR = "/home/hbakhshi/Downloads/tHq_Georgios/output/24_04_17/signal"
WSName = "tagsDumper/cms_hgg_13TeV"
DSName = "%s_125_13TeV_THQLeptonicTag"
WSFiles = {}
if sys.argv[1] == "thq":
    WSFiles["thq"] ="WS_THQ.root"
    DOSysts = 3
elif sys.argv[1] == "thw":
    WSFiles["thw"] = "WS_THW.root"
    DOSysts = 0
elif sys.argv[1] == "tth":
    WSFiles["tth"] = "WS_TTH.root"
    DOSysts = 1
elif sys.argv[1] == "vbf":
    WSFiles["vbf"] = "WS_VBF.root"
    DOSysts = 1
elif sys.argv[1] == "ggh":
    WSFiles["ggh"] = "WS_GGH.root"
    DOSysts = 1
elif sys.argv[1] == "vh":
    WSFiles["vh"] = "WS_VH.root"
    DOSysts = 1
    
Datasets = {}
for wsf in WSFiles:
    f = TFile.Open( "%s/%s" % (WSDIR , WSFiles[wsf] ) )
    #f.ls()
    ws_= f.Get( WSName )
    ds_ = ws_.data( DSName % (wsf ) )

    TotalRatios = None
    if DOSysts > 1 :
        TotalRatios = CtCvCpInfo("TotalRatios_"+wsf)
        TotalRatios.FillFrom1DHisto( "signals/13May/All_%s.root" % (wsf) , "writer/hAll" )
        
    dss_ = Dataset( ds_ , wsf , ws_ , DOSysts , TotalRatios)
    print dss_.Print()
    dss_.DS.Print()
    Datasets[ wsf ] = [ dss_ , ds_, ws_ , f , 0 ]


# gROOT.SetBatch(False)
# print Datasets["thq"][0].EfficiencyCtCv.AllCtOverCVs
# g = Datasets["thq"][0].EfficiencyCtCv.GetCtOverCv()
# c = Datasets["thq"][0].EfficiencyCtCv.GetCanvas()
# a = Datasets["thq"][0].EfficiencyCtCv.CtOverCvHisto
# #b = RooDataHist("test" , "test" , Datasets["thq"][0].EfficiencyCtCv.ArgListCtOverCv , RooFit.Import(a) )
# exit()

# fout = TFile.Open("out.root", "recreate")
# ws = RooWorkspace("ws")

# for ds in Datasets:
#     for ds_ in Datasets[ds][0].CTCVDS :
#         getattr( ws , "import")( Datasets[ds][0].CTCVDS[ds_]["ds"] , RooFit.RecycleConflictNodes() )

# ws.Write()
# fout.Close()
# exit()

if DOFTest:
    allPlots = []
    for ds in Datasets:
        mass_ = Datasets[ds][2].var("CMS_hgg_mass")
        mass_.setRange( 115 , 135 )
        
        dsToLoop = Datasets[ds][0]
        
        ftest = FTest( 2 , 5 , 0, 1 , mass_ , dsToLoop )
        c = TCanvas( ds , ds )
        c.cd()
        ftest.DrawAll()
        c.SaveAs( "%s.pdf" % (ds) )
        allPlots.append( c )

    exit()
    
for ds in Datasets:
    order = 0
    if ds == "tth" or ds == "vbf" or ds == "ggh" or ds == "vh":
        order = 3
    elif ds == "thw" :
        order = 2
    elif ds == "thq" :
        order = 3

    Datasets[ds][-1] = order

signal = None
allHiggs = []
fOutName = "out_ctcv_%s_syst.root" % (sys.argv[1]) if DOSysts > 1 else "out_%s_syst.root" % (sys.argv[1])
wsName = "ctcv" if DOSysts > 1 else "cms_hgg_13TeV"

fout = TFile.Open(fOutName , "recreate")
ws = RooWorkspace(wsName)
for ds in Datasets:
    mass_ = Datasets[ds][2].var("CMS_hgg_mass")
    mass_.setRange( 115 , 135 )
        
    dsToLoop = Datasets[ds][0]
    order = Datasets[ds][-1]
    print ds, order
    
    if ds == "thq" :
        signal = dsToLoop
    else:
        allHiggs.append( dsToLoop )

    
    dsToLoop.fit( order , 0 , mass_ )
    dsToLoop.Plot( mass_ )

    dsToLoop.Write( ws , fout )

if MakeFinalModel :
    fullModel = FullModel( signal , allHiggs , 35.9 )
    fullModel.Write("out" , "testws")
    
fout.cd()
ws.Write()
fout.Close()
for sys in AllSystParams:
    print sys, "param" , "0.0" , "1.0"
    
gROOT.SetBatch(False)

# weight0 = RooRealVar("weight","weight",-100000,1000000)
# dZ_ = ws.var("dZ")
# hMass_WV = TH1D("hMass_WV" , "Mass(WV)" , 50 , 100 , 150 )
# hMass_RV = TH1D("hMass_RV" , "Mass(RV)" , 50 , 100 , 150 )

# for i in range(0 , dsToLoop.numEntries()):
#     mass = dsToLoop.get(i).getRealValue("CMS_hgg_mass")
#     weight = dsToLoop.weight()
#     dZ = dsToLoop.get(i).getRealValue("dZ")

#     #print mass, weight, dZ
#     if dZ > 1 :
#         hMass_WV.Fill( mass , weight )
#     else:
#         hMass_RV.Fill( mass , weight )
# c = TCanvas("C")
# hMass_WV.DrawNormalized()
# hMass_RV.DrawNormalized("SAMES")
