from ROOT import RooWorkspace, RooDataSet, RooPlot, RooRealVar, TFile, gSystem, RooFit, TH1D, TCanvas, RooExtendPdf, RooAbsPdf, RooFitResult, kRed, kGreen , RooFormulaVar, gROOT
from SignalFit import *

gROOT.SetBatch(True)
gSystem.Load("~/Desktop/tHq/HiggsAnalysis/CombinedLimit/lib/libHiggsAnalysisCombinedLimit.so")

# file = TFile.Open("outdir_THQAllMergedWVPre/CMS-HGG_sigfit_THQAllMergedWVPre.root")
# ws = file.Get("wsig_13TeV")
# dsMrg = ws.data("sig_mrg_mass_m125_THQLeptonicTag")
# dsGgh = ws.data("sig_gghpre_mass_m125_THQLeptonicTag")
# dsToLoop = Dataset( dsMrg , "Merged")
# MH = ws.var("MH")
# rvFrac = ws.function("hggpdfsmrel_13TeV_mrg_THQLeptonicTag_rvFrac")
# rvFrac.Print()
# MH.Print()
# MH.setVal(125.0)
# MH.Print()

DOFTest=False
DOSysts=True

WSDIR = "/home/hbakhshi/Downloads/tHq_Georgios/output/03_17_17/signals"
WSName = "tagsDumper/cms_hgg_13TeV"
DSName = "%s_125_13TeV_THQLeptonicTag"
WSFiles = {"thq":"WS_THQ_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1.root" ,"tth":"WS_ttHToGG_M125_13TeV_powheg_pythia8_v2.root" ,  "thw":"WS_THW_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1.root" }
#"ggh":"WS_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root" ,  "vbf":"WS_VBFHToGG_M-125_13TeV_powheg_pythia8.root"}
Datasets = {}
for wsf in WSFiles:
    f = TFile.Open( "%s/%s" % (WSDIR , WSFiles[wsf] ) )
    ws_= f.Get( WSName )
    ds_ = ws_.data( DSName % (wsf ) )
    dss_ = Dataset( ds_ , wsf , ws_ , DOSysts)
    print dss_.RVFraction
    Datasets[ wsf ] = [ dss_ , ds_, ws_ , f , 0 ]


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

for ds in Datasets:
    order = 0
    if ds == "tth":
        order = 3
    elif ds == "thw" :
        order = 3
    elif ds == "thq" :
        order = 3

    Datasets[ds][-1] = order

if DOSysts:
    signal = None
    allHiggs = []
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
        #fitres.Print()
        dsToLoop.Plot( mass_ )

    fullModel = FullModel( signal , allHiggs , 35.9 )
    fullModel.Write("out" , "testws")
    
    for sys in AllSystParams:
        print sys, "param" , "0.0" , "1.0"
    
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
