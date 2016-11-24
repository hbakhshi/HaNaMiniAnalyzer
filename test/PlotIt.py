#!/usr/bin/env python
from ROOT import gROOT, TLatex, TCanvas, TFile, gROOT, TColor, TSystem
import math
import sys

outfname = ""
normtodata = True

if len(sys.argv) < 2:
    raise RuntimeError("at least one parameter has to be given")

if sys.argv[1] == "lumi":
    outfname = "out_cft_normtolumi.root"
    normtodata = False
elif sys.argv[1] == "data":
    outfname = "out_cft_normtodata.root"
    normtodata = True
else :
    raise RuntimeError("the first argument must be either lumi or data to set the final normalization method of the histograms")
    
    
gROOT.SetBatch(True)

from Samples80tHq.Samples import *
samples = None
runOnOutsOfAnotherJob = True
if runOnOutsOfAnotherJob :
    samples = skimmedSamples1
else :
    samples = MicroAOD80Samples

def GetSample( s ):
    if runOnOutsOfAnotherJob:
        for ss in samples:
            if s.Name == ss.Name :
                return ss
        return None
    else:
        return s



# GetSample(GJet7640M80).XSection = GJet7640M80.XSection*1.5

# GetSample(DiGG76).XSection *= 0.5
# GetSample(DiGG_76).XSection *= 0.5
# GetSample(GJet76M80_2040).XSection = GJet76M80_2040.XSection*0.7
# GetSample(GJet76M80_40).XSection = GJet76M80_40.XSection*0.6

# GetSample(QCDDoubleEM76_m80_pt3040).XSection = QCDDoubleEM76_m80_pt3040.XSection*0.8
# GetSample(QCDDoubleEM76_m80_pt40).XSection = QCDDoubleEM76_m80_pt40.XSection*0.8

# GetSample(DiGG_76) ,    , GetSample(TTBar76_FGG)

#nTuples = "/home/hbakhshi/Downloads/CERNBox/Personal/Projects/tHq/nTuples/80_19Sept/"
nTuples = "/home/hbakhshi/Downloads/CERNBox/Personal/Projects/tHq/nTuples/FoxWolfram1/;/home/hbakhshi/Downloads/CERNBox/Personal/Projects/tHq/nTuples/OptimizationEle/"


from tHqAnalyzer.HaNaMiniAnalyzer.SampleType import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan, kBlue
# dataSamples = SampleType("Data" , kBlack , [ GetSample(DoubleEG76D) , GetSample(DoubleEG76C) ] , nTuples ) # the first item must be data
# multigSamples = SampleType("MultiGamma" , kOrange , [ GetSample(DiGG76) , GetSample(GJet7640M80) , GetSample(GJet76M80_2040) , GetSample(GJet76M80_40) ] , nTuples )
# QCDSamples = SampleType("QCD" , kGreen+2 , [ GetSample(QCDDoubleEM76_m4080_pt30) , GetSample(QCDDoubleEM76_m80_pt3040) , GetSample(QCDDoubleEM76_m80_pt40) ] , nTuples )
# ttH = SampleType("ttH" , kBlue , [ GetSample(ttH76GG) ] , nTuples )
# SM = SampleType("SM" , kCyan , [ GetSample(WZ76_FGG) , GetSample(ZZ76_FGG) , GetSample(WW76_FGG) , GetSample(DYee) , GetSample(ZG2LG76) , GetSample(WJetsMG76_FGG) , GetSample(WG76_FGG) ,GetSample(TTGG76) , GetSample(TTGJ76) , GetSample(TGJ76) ] , nTuples )
# Higgs = SampleType("Higgs" , kRed , [GetSample(GluGluH76GG) , GetSample(VBFH76GG) , GetSample(VH76GG) ] , nTuples )
dataSamples = SampleType("Data" , kBlack , [GetSample(s) for s in MicroAOD80Samples if s.IsData] , nTuples ) # the first item must be data
multigSamples = SampleType("MultiGamma" , kOrange , [ GetSample(DiG_80Box) , GetSample(DiG_40Box80) , GetSample(GJet80M80_2040)  , GetSample(GJet8040M80) , GetSample(DiG_Jets)] , nTuples ) #, GetSample(GJet80M80_40)
QCDSamples = SampleType("QCD" , kGreen+2 , [ GetSample(QCDDoubleEM80_m4080_pt30) , GetSample(QCDDoubleEM80_m80_pt3040) , GetSample(QCDDoubleEM80_m80_pt40) ] , nTuples )
ttH = SampleType("ttH" , kBlue , [ GetSample(ttH80GG) ] , nTuples )
SM = SampleType("SM" , kCyan , [GetSample(DYee),GetSample(ZG2LG80),GetSample(TTGG80),GetSample(TGJ80), GetSample(TTGJ80) ,GetSample(WZ80) , GetSample(ZZ80) , GetSample(WW80) , GetSample(WJetsMG80) , GetSample(WG80)] , nTuples )
#
Higgs = SampleType("Higgs" , kRed , [GetSample(GluGluH80GG) , GetSample(VBFH80GG) , GetSample(VH80GG) ] , nTuples )


fxsec = TFile.Open("/home/hbakhshi/Downloads/CERNBox/Personal/Projects/tHq/nTuples/signal_xsecs.root")
gROOT.cd()
hxsec = fxsec.Get("hXSecBr")

Kvs = [1.0 , 1.5 , 0.5]
KvKfs = {
    1.0:[-3. , -2. , -1.5 , -1.25 ,      -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ],
    1.5:[-3. , -2. , -1.5 , -1.25 , -1 , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ],
    .5: [-3. , -2. , -1.5 , -1.25 , -1 , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ]
}
def GetSignalIndex(KV,KF):
    if KV==1. and KF==-1. :
        return 0
    index = 1
    for i in Kvs:
        if i==KV :
            break
        else:
            index += len( KvKfs[i] )
    index += [i for i in range(0,len(KvKfs[KV])) if KvKfs[KV][i] == KF][0]
    return index

NColors = 60
Stops = [ 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000 ]
Red   = [ 243./255., 243./255., 240./255., 240./255., 241./255., 239./255., 186./255., 151./255., 129./255.]
Green = [  0./255.,  46./255.,  99./255., 149./255., 194./255., 220./255., 183./255., 166./255., 147./255. ]
Blue  = [  6./255.,   8./255.,  36./255.,  91./255., 169./255., 235./255., 246./255., 240./255., 233./255. ]
palette = []
for g in range(0, len(Red) ) :
    nColorsGradient = (math.floor(NColors*Stops[g]) - math.floor(NColors*Stops[g-1]))
    for c in range(0, int(nColorsGradient) ):
        color = TColor( 800+c ,
                        ( Red[g-1]   +  c * (Red[g]   - Red[g-1])  / nColorsGradient),
                        ( Green[g-1] +  c * (Green[g] - Green[g-1])/ nColorsGradient),
                        ( Blue[g-1]  +  c * (Blue[g]  - Blue[g-1]) / nColorsGradient) )
        palette.append(color)

signalColors = {(1.0,-1.0):kBlue , (1.0,-.5):kRed , (1.0, 0.0):kCyan , (1.0, 0.5):kGreen  ,  (1.0 , 1.0):kGray , (1.5 , -3):kOrange}
def GetXSecs():
    ret = {}
    ret[0] = [kRed,hxsec.GetBinContent(hxsec.FindBin( -1., 1. )) ,"cv=1.0,cf=-1.00"]
    for KV in Kvs:
        for KF in KvKfs[KV]:
            index = GetSignalIndex( KV, KF)
            xsec = hxsec.GetBinContent( hxsec.FindBin( KF, KV ) )
            title = "cv=%.1f,cf=%.2f" % (KV, KF)
            color = palette[ index ].GetNumber()
            if (KV,KF) in signalColors:
                color = signalColors[ (KV, KF) ]
                print "color set from list"

            ret[index] = [color, xsec , title ]

    return ret
signalXSecs=GetXSecs()
#print signalXSecs
fxsec.Close()
#Signal80.ParentSample = ExtendedSample( Signal80 )
#Signal80.ParentSample.LoadJobs( nTuples , "out_%s_myMicroAODOutputFile_1_20.root" )
signalPoints = [(1.0,-1.0)] #, (1.0 , 1.0) ,(1.0,-.5) , (1.0, 0.0) , (1.0, 0.5)  ,   (1.5 , -3)  ]
# # for KV in Kvs:
# #     for KF in KvKfs[KV]:
# #         signalPoints.append( (KV, KF) )
signalSample = SampleType( "Signal" ,{i:signalXSecs[i] for i in [GetSignalIndex(s[0],s[1]) for s in signalPoints]}  , [ GetSample(Signal80) ] , nTuples , True )

nTotals76 = { "GluGluH":546308 ,
            "VBFH":612352 ,
            "VHGG":162247 ,
            "DiPhoton_":58532906 ,
            "DiPhoton":58532906 ,
            "GJet7640M80":38557025 ,
            "GJet76M80_2040":24739909 ,
            "GJet76M80_40":71613298 ,
            "ZG2LG76":3027812 ,
            "QCDDoubleEM76_m4080_pt30":37835430 ,
            "QCDDoubleEM76_m80_pt3040":17831367 ,
            "QCDDoubleEM76_m80_pt40":19958876 ,
            "TTGG":798500 ,
            "TTGJ":1578840 ,
            "TGJ":55704 ,
            "ttH":52169 ,
            "WJetsMG_FGG":47161328,
            "TTbar_FGG":97994442,
            "ZZ_FGG":9660541,
            "WZ_FGG" :15560489,
            "WW_FGG":988418,
            "WG_FGG":47275,
            "dyEE":49653546
            }

nTotals = {}
            
from tHqAnalyzer.HaNaMiniAnalyzer.Plotter import *
plotter = Plotter()
allSTs = [dataSamples , ttH , SM , Higgs , signalSample , QCDSamples , multigSamples ]
allNonQCDSTs = [ ttH , SM , Higgs ]
QCDSTs = [ multigSamples , QCDSamples ]
for st in allSTs :
    plotter.AddSampleType( st )
    for s in st.Samples:
        s.SetFriendTreeInfo( "/home/hbakhshi/Desktop/tHq/Analyzer/test/mva/Samples07Nov/" , "friend" )
        if s.IsData :
            continue
        if s.Name in nTotals :
            s.SetNTotal( nTotals[s.Name] )
        else:
            print "total number for sample %s is not set" % s.Name

Cuts = {"DiG":"1",
        "atLeastTwoJets":"nJets>1" ,
        "atLeastThreeJets":"nJets>2" ,
        "OneMediumB":"nMbJets==1" ,
        "MuonChannel" : "(LeptonType == 1)" ,
        "ElecChannel" : "(LeptonType == 2)" ,
        "Leptons" : "(LeptonType == 1 || LeptonType == 2)" ,
        "InvMassCut" : "( (DiG.mass < 130 ) && (DiG.mass > 120 ) )" ,
        "CR1" : "(LeptonType == 4)",
        "nonIsoMu" : "nMuons == 100" ,
        "met" : "met > 30" }


# cDiGnopuw = CutInfo( "DiGSelectionNopu" , Cuts["DiG"] , "Weight.W%d * G1.w * G2.w/puWeight" )
# cDiGnopuw.AddHist( "nVerticesBeforePU" , "nVertices", 40 , 0. , 40. )
# plotter.AddTreePlots( cDiGnopuw )

cDiGLeptons = CutInfo( "Lepton" , Cuts["DiG"] + " && " + Cuts["Leptons"] , "(Weight.W%d) * G1.w * G2.w" )
cDiGLeptons.AddHist( "mGG",  "DiG.mass" , 10 , 92. , 152. )
cDiGLeptons.AddHist( "nJets" , "nJets" , 10 , 0. , 10. )
cDiGLeptons.AddHist( "LepPt" , "lepton.pt",  7 , 10. , 150. )
cDiGLeptons.AddHist( "nbJets" , "nMbJets" , 5 , 0. , 5. )
cDiGLeptons.AddHist( "met" , "met",  20 , 20. , 220. )
cDiGLeptons.AddHist( "jPt" , "nJets < 1 ? -1 : jetsPt[zeroB.leading]",  29 , 10. , 300. )
cDiGLeptons.AddHist( "jEta" , "nJets < 1 ? -1 : abs(jetsEta[zeroB.forward])",  15 , 0 , 5.0 )
plotter.AddTreePlots( cDiGLeptons )

cDiGEle = CutInfo( "Electron" , Cuts["DiG"] + " && " + Cuts["ElecChannel"] , "(Weight.W%d) * G1.w * G2.w" )
for h in cDiGLeptons.ListOfHists:
    cDiGEle.AddHist( h )
plotter.AddTreePlots( cDiGEle )

cDiGMu = CutInfo( "Muon" , Cuts["DiG"] + " && " + Cuts["MuonChannel"] , "(Weight.W%d) * G1.w * G2.w" )
for h in cDiGLeptons.ListOfHists:
    cDiGMu.AddHist( h )
plotter.AddTreePlots( cDiGMu )

cut2J1T = " && " + Cuts["atLeastTwoJets"] + " && " + Cuts["OneMediumB"]
cDiGLeptons2j1t = CutInfo( "Lepton2J1T" , Cuts["DiG"] + " && " + Cuts["Leptons"] + cut2J1T  , "(Weight.W%d) * G1.w * G2.w" )
cDiGLeptons2j1t.AddHist( "TopMass",  "Top.topM" , 40 , 100 , 300)
cDiGLeptons2j1t.AddHist( "tH_DPhi",  "THReco.THDPhi" , 10 , -3.15 , 3.15 )
cDiGLeptons2j1t.AddHist( "tH_CosTheta",  "Top.CosTheta" , 10 , -1 , 1 )
cDiGLeptons2j1t.AddHist( "tH_jpDPhi",  "Top.JPrime" , 10 , -1 , 1 )
cDiGLeptons2j1t.AddHist( "es_aplanarity",  "eventshapes.aplanarity" , 10 , 0 , 0.4 )
cDiGLeptons2j1t.AddHist( "es_isotropy",  "eventshapes.isotropy" , 10 , -1 , 1 )
cDiGLeptons2j1t.AddHist( "met" , "met",  20 , 20. , 220. )
cDiGLeptons2j1t.AddHist( "jprimeeta" , "abs(jetsEta[oneB.forward])" , 10 , 0 , 5 )
BDThist = cDiGLeptons2j1t.AddHist( "BDT",  "BDT" , 50 , -0.5 , 0.5 )
mGGhist = cDiGLeptons2j1t.AddHist( "mGG",  "DiG.mass" , 30 , 100. , 400. )
plotter.AddTreePlots( cDiGLeptons2j1t )

cDiGEle2j1t = CutInfo( "Electron2j1t" , Cuts["DiG"] + " && " + Cuts["ElecChannel"] + cut2J1T, "(Weight.W%d) * G1.w * G2.w" )
for h in cDiGLeptons2j1t.ListOfHists:
    cDiGEle2j1t.AddHist( h )
cDiGEle2j1t.AddHist( mGGhist, BDThist )
plotter.AddTreePlots( cDiGEle2j1t )

cDiGMu2j1t = CutInfo( "Muon2j1t" , Cuts["DiG"] + " && " + Cuts["MuonChannel"] + cut2J1T , "(Weight.W%d) * G1.w * G2.w" )
for h in cDiGLeptons2j1t.ListOfHists:
    cDiGMu2j1t.AddHist( h )
cDiGMu2j1t.AddHist( mGGhist, BDThist )
plotter.AddTreePlots( cDiGMu2j1t )

cDiGCR1 = CutInfo( "CR1" , Cuts["DiG"] + " && " + Cuts["CR1"]  , "Weight.W%d * G1.w * G2.w" )
for h in cDiGLeptons2j1t.ListOfHists:
    cDiGCR1.AddHist( h )
cDiGCR1.AddHist( mGGhist, BDThist )
plotter.AddTreePlots( cDiGCR1 )

cut3J1T = " && " + Cuts["atLeastThreeJets"] + " && " + Cuts["OneMediumB"]
cDiGCR12j1t = CutInfo( "CR12j1t" , Cuts["DiG"] + " && " + Cuts["CR1"] + cut3J1T , "Weight.W%d * G1.w * G2.w" )
for h in cDiGLeptons2j1t.ListOfHists:
    cDiGCR12j1t.AddHist( h )
cDiGCR12j1t.AddHist( mGGhist, BDThist)
plotter.AddTreePlots( cDiGCR12j1t )

cDiGLeptons2j1t.AddHist( mGGhist, BDThist )

plotter.LoadHistos( 12900 )

plotter.AddLabels( "CutFlowTable" , ["All" , "HLT" , "Vertex" , ">1Pair" , "LeadingPass" , "SubLeadingPass" , "PairCuts" , ">1Jets" , "//" , "//" , "--" , "--" , ">0#mu" , "1#mu" , "--" ] )

fout = TFile.Open( outfname , "recreate")
plotter.Write(fout, normtodata)

# for sel in ["MuSel"] : # , "Jet" , "bJet" , "2J" , "2J1T" , "bJetF1"  ]:
#     seldir = fout.mkdir( "res_" + sel )
#     #signaldir = seldir.mkdir("Signals")
#     for p in Plots:
#         #signaldir.cd()
#         #plotter.Props[ Plots[p][sel].Name ].GetSignalCanvas().Write()

#         seldir.cd()
        
#         canvas = TCanvas( p , p )
#         canvas.Divide( 3, 2)
    
#         templateDiG = plotter.Props[ Plots[p]["DiGSelection"].Name ]
#         templateNIso = plotter.Props[ Plots[p]["nonIsoMu"].Name ]
#         isoPlot = plotter.Props[ Plots[p][sel].Name ]

#         if Plots[p]["DiGSelection"].Name == "mGG":
#             templateNIso.Rebin([60,80,110,130,150])
#             templateDiG.Rebin([60,80,110,130,150])
#             isoPlot.Rebin([60,80,110,130,150])
#         if Plots[p]["DiGSelection"].Name == "g1pt":
#             newbins = [30,50,80,110,150]
#             templateNIso.Rebin(newbins)
#             templateDiG.Rebin(newbins)
#             isoPlot.Rebin(newbins)
#         if Plots[p]["DiGSelection"].Name == "g2pt":
#             newbins = [20,40,70,100]
#             templateNIso.Rebin(newbins)
#             templateDiG.Rebin(newbins)
#             isoPlot.Rebin(newbins)

            
#         isoTemDiGNormMC = isoPlot.Clone( p + sel + "_qcdfromDiG_normMC" )
#         nMC = isoTemDiGNormMC.GetBkgFromCR( templateDiG , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 1 )
#         canvas.cd(1)
#         isoTemDiGNormMC.Draw(1)
#         isoTemDiGNormMC.GetCanvas(0).Draw()
#         text = TLatex()
#         text.SetNDC()
#         text.SetTextSize(0.03)
#         isoTemDiGNormMC.GetCanvas(1)
#         text.DrawLatex(0.13,0.943, "%f (shape from DiG, norm from MC)" % (nMC) )

#         isoTemDiGNormDataMSM = isoPlot.Clone( p+sel + "_qcdfromDiG_normDataMSM")
#         nDataMSM = isoTemDiGNormDataMSM.GetBkgFromCR( templateDiG , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 2 )
#         canvas.cd(2)
#         isoTemDiGNormDataMSM.Draw(1)
#         isoTemDiGNormDataMSM.GetCanvas(0).Draw()
#         text = TLatex()
#         text.SetNDC()
#         text.SetTextSize(0.03)
#         isoTemDiGNormDataMSM.GetCanvas(1)
#         text.DrawLatex(0.13,0.943, "%f (shape from DiG, norm from data-MC)" % (nDataMSM) )

#         isoTemDiGNormFit = isoPlot.Clone( p+sel + "_qcdfromDiG_normFit")
#         nFitDiG = isoTemDiGNormFit.GetBkgFromCR( templateDiG , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 3 )
#         canvas.cd(3)
#         isoTemDiGNormFit.Draw(1)
#         isoTemDiGNormFit.GetCanvas(0).Draw()
#         text = TLatex()
#         text.SetNDC()
#         text.SetTextSize(0.03)
#         isoTemDiGNormFit.GetCanvas(1)
#         text.DrawLatex(0.13,0.943, "%f (shape from DiG, norm from Fit)" % (nFitDiG) )

#         isoTemNIsoNormMC = isoPlot.Clone( p + sel + "_qcdfromNIso_normMC" )
#         nMC = isoTemNIsoNormMC.GetBkgFromCR( templateNIso , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 1 )
#         canvas.cd(4)
#         isoTemNIsoNormMC.Draw(1)
#         isoTemNIsoNormMC.GetCanvas(0).Draw()
#         text = TLatex()
#         text.SetNDC()
#         text.SetTextSize(0.03)
#         isoTemNIsoNormMC.GetCanvas(1)
#         text.DrawLatex(0.13,0.943, "%f (shape NonIso, Norm MC)" % (nMC) )


#         isoTemNIsoNormDataMSM = isoPlot.Clone( p+sel + "_qcdfromNIso_normDataMSM")
#         nDataMSM = isoTemNIsoNormDataMSM.GetBkgFromCR( templateNIso , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 2 )
#         canvas.cd(5)
#         isoTemNIsoNormDataMSM.Draw(1)
#         isoTemNIsoNormDataMSM.GetCanvas(0).Draw()
#         text = TLatex()
#         text.SetNDC()
#         text.SetTextSize(0.03)
#         isoTemNIsoNormDataMSM.GetCanvas(1)
#         text.DrawLatex(0.13,0.943, "%f (shape NonIso, Norm Data-MC)" % (nDataMSM) )


#         isoTemNIsoNormFit = isoPlot.Clone( p+sel + "_qcdfromNIso_normFit")
#         nFitNIso = isoTemNIsoNormFit.GetBkgFromCR( templateNIso , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 3 )
#         canvas.cd(6)
#         isoTemNIsoNormFit.Draw(1)
#         isoTemNIsoNormFit.GetCanvas(0).Draw()
#         text = TLatex()
#         text.SetNDC()
#         text.SetTextSize(0.03)
#         isoTemNIsoNormFit.GetCanvas(1)
#         text.DrawLatex(0.13,0.943, "%f (shape NonIso, Norm Fit)" % (nFitNIso) )

#         canvas.Write()

    
fout.Close()
