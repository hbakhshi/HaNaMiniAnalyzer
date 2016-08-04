#!/usr/bin/env python
from ROOT import gROOT, TLatex, TCanvas, TFile, gROOT, TColor
import math

gROOT.SetBatch(True)

from Samples76tHq.Samples import *
samples = None
runOnOutsOfAnotherJob = True
if runOnOutsOfAnotherJob :
    samples = samples24june
    samples += sampleswith24juneonly
else :
    samples = MicroAOD76Samples

def GetSample( s ):
    if runOnOutsOfAnotherJob:
        for ss in samples:
            if s.Name == ss.Name :
                return ss
        return None
    else:
        return sample



# GetSample(GJet7640M80).XSection = GJet7640M80.XSection*1.5

# GetSample(DiGG76).XSection *= 0.5
# GetSample(DiGG_76).XSection *= 0.5
# GetSample(GJet76M80_2040).XSection = GJet76M80_2040.XSection*0.7
# GetSample(GJet76M80_40).XSection = GJet76M80_40.XSection*0.6

# GetSample(QCDDoubleEM76_m80_pt3040).XSection = QCDDoubleEM76_m80_pt3040.XSection*0.8
# GetSample(QCDDoubleEM76_m80_pt40).XSection = QCDDoubleEM76_m80_pt40.XSection*0.8

# GetSample(DiGG_76) ,    , GetSample(TTBar76_FGG)
    
from tHqAnalyzer.HaNaMiniAnalyzer.SampleType import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan, kBlue
dataSamples = SampleType("Data" , kBlack , [ GetSample(DoubleEG76D) , GetSample(DoubleEG76C) ] , "/home/hbakhshi/Desktop/thq" ) # the first item must be data
multigSamples = SampleType("MultiGamma" , kOrange , [ GetSample(DiGG76) , GetSample(GJet7640M80) , GetSample(GJet76M80_2040) , GetSample(GJet76M80_40) ] , "/home/hbakhshi/Desktop/thq" )
QCDSamples = SampleType("QCD" , kGreen+2 , [ GetSample(QCDDoubleEM76_m4080_pt30) , GetSample(QCDDoubleEM76_m80_pt3040) , GetSample(QCDDoubleEM76_m80_pt40) ] , "/home/hbakhshi/Desktop/thq" )
ttH = SampleType("ttH" , kBlue , [ GetSample(ttH76GG) ] , "/home/hbakhshi/Desktop/thq" )
SM = SampleType("SM" , kCyan , [GetSample(GluGluH76GG) , GetSample(VBFH76GG) , GetSample(VH76GG) , GetSample(WZ76_FGG) , GetSample(ZZ76_FGG) , GetSample(WW76_FGG) , GetSample(DYee) , GetSample(ZG2LG76) , GetSample(WJetsMG76_FGG) , GetSample(WG76_FGG) ,GetSample(TTGG76) , GetSample(TTGJ76) , GetSample(TGJ76) ] , "/home/hbakhshi/Desktop/thq" )

fxsec = TFile.Open("/home/hbakhshi/Desktop/thq/xsec.root")
gROOT.cd()
hxsec = fxsec.Get("hXSecBr")

Kvs = [1.0 , 1.5 , 0.5]
KvKfs = {
    1.0:[-3. , -2. , -1.5 , -1.25 , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 , 1 , 1.25 , 1.5 , 2. , 3. ],
    1.5:[-3. , -2. , -1.5 , -1.25 , -1 , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ],
    .5:[-3. , -2. , -1.5 , -1.25 , -1 , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ]
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
print signalXSecs
fxsec.Close()
Signal76.ParentSample = ExtendedSample( Signal76 )
Signal76.ParentSample.LoadJobs( "/home/hbakhshi/Desktop/thq" , "out_%s_myMicroAODOutputFile_1_20.root" )
signalPoints = [(1.0,-1.0) , (1.0,-.5) , (1.0, 0.0) , (1.0, 0.5)  ,  (1.0 , 1.0) , (1.5 , -3)  ]
signalSample = SampleType( "Signal" ,{i:signalXSecs[i] for i in [GetSignalIndex(s[0],s[1]) for s in signalPoints]}  , [ Signal76 ] , "/home/hbakhshi/Desktop/thq" , True )

nTotals = { "GluGluH":546308 ,
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
            

from tHqAnalyzer.HaNaMiniAnalyzer.Plotter import *
plotter = Plotter()
allSTs = [dataSamples ,multigSamples , QCDSamples , ttH , SM , signalSample ]  #higgsSamples , multigSamples , QCDSamples , topSamples , WJets, DY, multiBoson , ttbar ]
allNonQCDSTs = [ ttH , SM ]
QCDSTs = [ multigSamples , QCDSamples ]
for st in allSTs :
    plotter.AddSampleType( st )
    for s in st.Samples:
        if s.IsData :
            continue
        if s.Name in nTotals :
            s.SetNTotal( nTotals[s.Name] )
        else:
            print "total number for sample %s is not set" % s.Name


def enum(**enums):
    return type('Enum', (), enums)
tHqSelStatuses = enum(All = 0,
                      HLT = 1,
                      Vertex = 2,
                      gamma_pair = 3,
                      pt_g1 = 4,
                      pt_g2  = 5,
                      gamma_ID = 6,
                      MVA = 7,
                      inv_mass = 8,
                      mu_selection = 9,
                      extra_mu_veto = 10,
                      jets = 11,
                      bjets =12,
                      MET = 13
                      )

class Plots_(dict):
    def __init__(self):
        pass
    def __getitem__(self, key):
        return dict.__getitem__(self,key)
    def __setitem__(self, key, value):
        dict.__setitem__(self,key,value)
    def append(self, x):
        if x.Name in self.keys() :
            self[x.Name][x.SelName] = x
        else:
            self[x.Name] = {x.SelName:x}

    def Append(self, name , x):
        self[name][x.SelName] = x
        
Plots = Plots_()
# plotter.AddTreePlot( "nVerticesBeforePU" , "nVertices" , tHqSelStatuses.inv_mass  , 40 , 0 , 40 , "DiG.other>60", "DiGSelection" ).SetWeight( "(Weight.W%d/puWeight)" )
# plotter.AddTreePlot( "nVerticesAfterPU" , "nVertices" , tHqSelStatuses.inv_mass  , 40 , 0 , 40 , "DiG.other>60", "DiGSelection" )

# Plots.append( plotter.AddTreePlot( "nGPairs" , "nGPairs" , tHqSelStatuses.inv_mass  , 10 , 0 , 10 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "nSelGPairs" , "nSelGPairs" , tHqSelStatuses.inv_mass  , 10 , 0 , 10 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "ptGG" , "DiG.pt" , tHqSelStatuses.inv_mass  , 8 , 10 , 250 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "etaGG" , "abs(DiG.eta)" , tHqSelStatuses.inv_mass  , 12, 0 , 4.8 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "phiGG" , "DiG.phi" , tHqSelStatuses.inv_mass  , 8, -3.2 , 3.2 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "mGG" , "DiG.other" , tHqSelStatuses.inv_mass  , 30 , 50 , 200 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "g1pt" , "G1.pt" , tHqSelStatuses.inv_mass  , 20 , 20 , 220 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "g2pt" , "G2.pt" , tHqSelStatuses.inv_mass  , 20 , 20 , 220 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "g1eta" , "abs(G1.eta)" , tHqSelStatuses.inv_mass  , 4 , 0 , 2.4 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "g2eta" , "abs(G2.eta)" , tHqSelStatuses.inv_mass  , 4 , 0 , 2.4 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "g1phi" , "G1.phi" , tHqSelStatuses.inv_mass  , 8 , -3.2 , 3.2 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "g2phi" , "G2.phi" , tHqSelStatuses.inv_mass  , 8 , -3.2 , 3.2 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "g1mva" , "G1.other" , tHqSelStatuses.inv_mass  , 10 , -1 , 1 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "g2mva" , "G2.other" , tHqSelStatuses.inv_mass  , 10 , -1 , 1 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "digMVA" , "diGMVA" , tHqSelStatuses.inv_mass  , 10 , -1 , 1 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "nMus" , "nMuons == 100 ? 6 : nMuons" , tHqSelStatuses.inv_mass  , 10 , 0 , 10 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "muPt" , "mu.pt" , tHqSelStatuses.inv_mass  , 7 , 10 , 150 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "muEta" , "abs(mu.eta)" , tHqSelStatuses.inv_mass  , 4 , 0 , 2.8 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "muPhi" , "mu.phi" , tHqSelStatuses.inv_mass  , 8 , -3.2 , 3.2 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "nJets" , "(nJets+nbJets)" , tHqSelStatuses.inv_mass  , 10 , 0 , 10 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "jPt" , "forwardJ.pt" , tHqSelStatuses.inv_mass  , 29 , 10 , 300 , "DiG.other>60", "DiGSelection" ) )
Plots.append( plotter.AddTreePlot( "jEta" , "abs(forwardJ.eta)" , tHqSelStatuses.inv_mass  , 15 , 0 , 5.0 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "jPhi" , "forwardJ.phi" , tHqSelStatuses.inv_mass  , 16 , -3.2 , 3.2 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "nbJets" , "nbJets" , tHqSelStatuses.inv_mass  , 3 , 0 , 3 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "bjPt" , "bJ.pt" , tHqSelStatuses.inv_mass  , 9 , 20 , 200 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "bjEta" , "abs(bJ.eta)" , tHqSelStatuses.inv_mass  , 4 , 0 , 2.8 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "bjPhi" , "bJ.phi" , tHqSelStatuses.inv_mass  , 4 , -3.2 , 3.2 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "met" , "met" , tHqSelStatuses.inv_mass  , 20 , 20 , 220 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "metPhi" , "metPhi" , tHqSelStatuses.inv_mass  , 16 , -3.2 , 3.2 , "DiG.other>60", "DiGSelection" ) )
# Plots.append( plotter.AddTreePlot( "met" , "met" , tHqSelStatuses.inv_mass  , 20 , 20 , 220 , "DiG.other>60", "DiGSelection" ) )

for p in Plots.keys():
    dig = Plots[p]["DiGSelection"]
    Plots.Append(p , plotter.AddTreePlot( dig.Name + "_nonIsoMu" , dig.VarName , tHqSelStatuses.inv_mass  , dig.nBins, dig.From , dig.To , "(nMuons==100) && " + dig.Cut , "nonIsoMu" ) )
    Plots.Append(p , plotter.AddTreePlot( dig.Name + "_MuSel" , dig.VarName , tHqSelStatuses.extra_mu_veto , dig.nBins, dig.From , dig.To , dig.Cut , "MuSel" ) )
    Plots.Append(p , plotter.AddTreePlot( dig.Name + "_Jet" , dig.VarName , tHqSelStatuses.jets , dig.nBins, dig.From , dig.To , dig.Cut , "Jet" ) )
    Plots.Append(p , plotter.AddTreePlot( dig.Name + "_bJet" , dig.VarName , tHqSelStatuses.bjets , dig.nBins, dig.From , dig.To , dig.Cut , "bJet" ) )

plotter.LoadHistos( 2200 )

plotter.AddLabels( "CutFlowTable" , ["All" , "HLT" , "Vertex" , "#gamma pair" , "p_{T}^{#gamma_{0}}" , "p_{T}^{#gamma_{1}}" , "#gamma ID" , "MVA", "inv mass" ,"#mu selection" , "extra #mu veto", "2jets" , "1bjets" , "MET" ] )
fout = TFile.Open("out_jeta.root", "recreate")
plotter.Write(fout)

for sel in ["MuSel" , "Jet" , "bJet" ]:
    seldir = fout.mkdir( "res_" + sel )
    signaldir = seldir.mkdir("Signals")
    for p in Plots:
        signaldir.cd()
        plotter.Props[ Plots[p][sel].Name ].GetSignalCanvas().Write()

        seldir.cd()
        
        canvas = TCanvas( p , p )
        canvas.Divide( 3, 2)
    
        templateDiG = plotter.Props[ Plots[p]["DiGSelection"].Name ]
        templateNIso = plotter.Props[ Plots[p]["nonIsoMu"].Name ]
        isoPlot = plotter.Props[ Plots[p][sel].Name ]

        if Plots[p]["DiGSelection"].Name == "mGG":
            templateNIso.Rebin([60,80,110,130,150])
            templateDiG.Rebin([60,80,110,130,150])
            isoPlot.Rebin([60,80,110,130,150])
        if Plots[p]["DiGSelection"].Name == "g1pt":
            newbins = [30,50,80,110,150]
            templateNIso.Rebin(newbins)
            templateDiG.Rebin(newbins)
            isoPlot.Rebin(newbins)
        if Plots[p]["DiGSelection"].Name == "g2pt":
            newbins = [20,40,70,100]
            templateNIso.Rebin(newbins)
            templateDiG.Rebin(newbins)
            isoPlot.Rebin(newbins)

            
        isoTemDiGNormMC = isoPlot.Clone( p + sel + "_qcdfromDiG_normMC" )
        nMC = isoTemDiGNormMC.GetBkgFromCR( templateDiG , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 1 )
        canvas.cd(1)
        isoTemDiGNormMC.Draw(1)
        isoTemDiGNormMC.GetCanvas(0).Draw()
        text = TLatex()
        text.SetNDC()
        text.SetTextSize(0.03)
        isoTemDiGNormMC.GetCanvas(1)
        text.DrawLatex(0.13,0.943, "%f (shape from DiG, norm from MC)" % (nMC) )

        isoTemDiGNormDataMSM = isoPlot.Clone( p+sel + "_qcdfromDiG_normDataMSM")
        nDataMSM = isoTemDiGNormDataMSM.GetBkgFromCR( templateDiG , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 2 )
        canvas.cd(2)
        isoTemDiGNormDataMSM.Draw(1)
        isoTemDiGNormDataMSM.GetCanvas(0).Draw()
        text = TLatex()
        text.SetNDC()
        text.SetTextSize(0.03)
        isoTemDiGNormDataMSM.GetCanvas(1)
        text.DrawLatex(0.13,0.943, "%f (shape from DiG, norm from data-MC)" % (nDataMSM) )

        isoTemDiGNormFit = isoPlot.Clone( p+sel + "_qcdfromDiG_normFit")
        nFitDiG = isoTemDiGNormFit.GetBkgFromCR( templateDiG , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 3 )
        canvas.cd(3)
        isoTemDiGNormFit.Draw(1)
        isoTemDiGNormFit.GetCanvas(0).Draw()
        text = TLatex()
        text.SetNDC()
        text.SetTextSize(0.03)
        isoTemDiGNormFit.GetCanvas(1)
        text.DrawLatex(0.13,0.943, "%f (shape from DiG, norm from Fit)" % (nFitDiG) )

        isoTemNIsoNormMC = isoPlot.Clone( p + sel + "_qcdfromNIso_normMC" )
        nMC = isoTemNIsoNormMC.GetBkgFromCR( templateNIso , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 1 )
        canvas.cd(4)
        isoTemNIsoNormMC.Draw(1)
        isoTemNIsoNormMC.GetCanvas(0).Draw()
        text = TLatex()
        text.SetNDC()
        text.SetTextSize(0.03)
        isoTemNIsoNormMC.GetCanvas(1)
        text.DrawLatex(0.13,0.943, "%f (shape NonIso, Norm MC)" % (nMC) )


        isoTemNIsoNormDataMSM = isoPlot.Clone( p+sel + "_qcdfromNIso_normDataMSM")
        nDataMSM = isoTemNIsoNormDataMSM.GetBkgFromCR( templateNIso , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 2 )
        canvas.cd(5)
        isoTemNIsoNormDataMSM.Draw(1)
        isoTemNIsoNormDataMSM.GetCanvas(0).Draw()
        text = TLatex()
        text.SetNDC()
        text.SetTextSize(0.03)
        isoTemNIsoNormDataMSM.GetCanvas(1)
        text.DrawLatex(0.13,0.943, "%f (shape NonIso, Norm Data-MC)" % (nDataMSM) )


        isoTemNIsoNormFit = isoPlot.Clone( p+sel + "_qcdfromNIso_normFit")
        nFitNIso = isoTemNIsoNormFit.GetBkgFromCR( templateNIso , [s.Name for s in QCDSTs] , ["QCD" , kGreen+2] , 3 )
        canvas.cd(6)
        isoTemNIsoNormFit.Draw(1)
        isoTemNIsoNormFit.GetCanvas(0).Draw()
        text = TLatex()
        text.SetNDC()
        text.SetTextSize(0.03)
        isoTemNIsoNormFit.GetCanvas(1)
        text.DrawLatex(0.13,0.943, "%f (shape NonIso, Norm Fit)" % (nFitNIso) )

        canvas.Write()

    
fout.Close()
