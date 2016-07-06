#!/usr/bin/env python
runOnOutsOfAnotherJob = True

nFilesPerJob=3
prefix = "out"
import sys
import os
user=""
if len(sys.argv) > 2 :
    user = sys.argv[2]
else:
    import getpass
    user = getpass.getuser()
OutPath = "eos/cms/store/user/%s/%s/" % (user, sys.argv[1] )

from ROOT import TFile, TDirectory, gDirectory, gROOT
gROOT.SetBatch(True)

from Samples76tHq.Samples import *
samples = None
if runOnOutsOfAnotherJob :
    samples = samples24june
else :
    samples = MicroAOD76Samples


OutPath24June = "eos/cms/store/user/%s/thq26june/" % (user)

for sample in samples:
    if sample.Name in [s.Name for s in sampleswith24juneonly]:
        #job is already created : sample.MakeJobs( 20 , "%s/%s" % (OutPath24June , prefix) )
        print sample.Name 
    else:
        sample.MakeJobs( nFilesPerJob , "%s/%s" % (OutPath , prefix) )

def GetSample( s ):
    if runOnOutsOfAnotherJob:
        for ss in samples:
            if s.Name == ss.Name :
                return ss
        return None
    else:
        return sample

# GetSample(GJet7640M80).XSection = GJet7640M80.XSection*1.5
# GetSample(GJet76M80_2040).XSection = GJet76M80_2040.XSection*0.7
# GetSample(GJet76M80_40).XSection = GJet76M80_40.XSection*0.6

# GetSample(QCDDoubleEM76_m80_pt3040).XSection = QCDDoubleEM76_m80_pt3040.XSection*0.8
# GetSample(QCDDoubleEM76_m80_pt40).XSection = QCDDoubleEM76_m80_pt40.XSection*0.8


from tHqAnalyzer.HaNaMiniAnalyzer.Plotter import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan, kBlue
dataSamples = SampleType("Data" , kBlack , [ GetSample(DoubleEG76D) , GetSample(DoubleEG76C) ] ) # the first item must be data
higgsSamples = SampleType("Higgs" , kRed , [ GetSample(GluGluH76GG) , GetSample(VBFH76GG) , GetSample(VH76GG) ] )
multigSamples = SampleType("multi-#gamma" , kOrange , [GetSample(DiGG_76) , GetSample(DiGG76) , GetSample(GJet7640M80) , GetSample(GJet76M80_2040) , GetSample(GJet76M80_40) , GetSample(ZG2LG76) ] )
QCDSamples = SampleType("QCD" , kGreen+2 , [ GetSample(QCDDoubleEM76_m4080_pt30) , GetSample(QCDDoubleEM76_m80_pt3040) , GetSample(QCDDoubleEM76_m80_pt40) ] )
topSamples = SampleType("TOP" , kBlue , [ GetSample(TTGG76) , GetSample(TTGJ76) , GetSample(TGJ76) , GetSample(ttH76GG) ] )
#signalSample= SampleType( "Signal" , kCyan , [ Signal76 ] , True )
SMSamples = [ DYee , WJetsMG76_FGG,  ZZ76_FGG, WZ76_FGG , WW76_FGG ]
WJets = SampleType("W" , kGray , [WJetsMG76_FGG] )
DY = SampleType("DY" , kGray+1 , [DYee] )
ttbar = SampleType("ttbar" , kGray+3 , [TTBar76_FGG] )
multiBoson = SampleType("multi-bosons" , kGray+2 , [WZ76_FGG , ZZ76_FGG , WW76_FGG] )
#TTBar76_FGG,

for st in [ WJets.Samples , DY.Samples, multiBoson.Samples , ttbar.Samples ]:
    for s in st:
        if s.Name == "WJetsMG_FGG":
            s.SetNTotal( 47161328 )
        elif s.Name == "TTbar_FGG":
            s.SetNTotal( 97994442 )
        elif s.Name == "ZZ_FGG":
            s.SetNTotal( 9660541 )
        elif s.Name == "WZ_FGG" :
            s.SetNTotal( 15560489 )
        elif s.Name == "WW_FGG":
            s.SetNTotal(988418)
            
        print "nTotal for sample %s is set to %d" % (s.Name , s.GetNTotal() )


plotter = Plotter()
for st in [dataSamples , higgsSamples , multigSamples , QCDSamples , topSamples , WJets, DY, multiBoson , ttbar ]:
    plotter.AddSampleType( st )


plotter.LoadHistos( 2200 )

plotter.AddLabels( "CutFlowTable" , ["All" , "HLT" , "Vertex" , "#gamma pair" , "p_{T}^{#gamma_{0}}" , "p_{T}^{#gamma_{1}}" , "#gamma ID" , "MVA", "inv mass" ,"#mu selection" , "extra #mu veto", "2jets" , "1bjets" , "MET" ] )

plotter.DrawAll()

fout = TFile.Open("out.root", "recreate")
plotter.Write(fout)
fout.Close()

