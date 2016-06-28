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

for sample in samples:
    sample.MakeJobs( nFilesPerJob , "%s/%s" % (OutPath , prefix) )

def GetSample( s ):
    if runOnOutsOfAnotherJob:
        for ss in samples:
            if s.Name == ss.Name :
                return ss
        return None
    else:
        return sample

GetSample(GJet7640M80).XSection = GJet7640M80.XSection*1.5
GetSample(GJet76M80_2040).XSection = GJet76M80_2040.XSection*0.7
GetSample(GJet76M80_40).XSection = GJet76M80_40.XSection*0.6

GetSample(QCDDoubleEM76_m80_pt3040).XSection = QCDDoubleEM76_m80_pt3040.XSection*0.8
GetSample(QCDDoubleEM76_m80_pt40).XSection = QCDDoubleEM76_m80_pt40.XSection*0.8

from tHqAnalyzer.HaNaMiniAnalyzer.Plotter import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan, kBlue
dataSamples = SampleType("Data" , kBlack , [ GetSample(DoubleEG76D) , GetSample(DoubleEG76C) ] ) # the first item must be data
higgsSamples = SampleType("Higgs" , kRed , [ GetSample(GluGluH76GG) , GetSample(VBFH76GG) , GetSample(VH76GG) ] )
multigSamples = SampleType("multi-#gamma" , kOrange , [ GetSample(DiGG76) , GetSample(GJet7640M80) , GetSample(GJet76M80_2040) , GetSample(GJet76M80_40) , GetSample(ZG2LG76) ] )
QCDSamples = SampleType("QCD" , kGreen+2 , [ GetSample(QCDDoubleEM76_m4080_pt30) , GetSample(QCDDoubleEM76_m80_pt3040) , GetSample(QCDDoubleEM76_m80_pt40) ] )
topSamples = SampleType("TOP" , kBlue , [ GetSample(TTGG76) , GetSample(TTGJ76) , GetSample(TGJ76) , GetSample(ttH76GG) ] )
#signalSample= SampleType( "Signal" , kCyan , [ Signal76 ] , True )

plotter = Plotter()
for st in [dataSamples , higgsSamples , multigSamples , QCDSamples , topSamples  ]:
    plotter.AddSampleType( st )


plotter.LoadHistos( 2200 )

plotter.AddLabels( "CutFlowTable" , ["All" , "HLT" , "Vertex" , "#gamma pair" , "p_{T}^{#gamma_{0}}" , "p_{T}^{#gamma_{1}}" , "#gamma ID" , "MVA", "inv mass" ,"#mu selection" , "extra #mu veto", "2jets" , "1bjets" , "MET" ] )

plotter.DrawAll()

fout = TFile.Open("out.root", "recreate")
plotter.Write(fout)
fout.Close()

