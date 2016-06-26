#!/usr/bin/env python
nFilesPerJob=20
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
for sample in MicroAOD76Samples:
    sample.MakeJobs( nFilesPerJob , "%s/%s" % (OutPath , prefix) )

GJet7640M80.XSection = GJet7640M80.XSection*1.5
GJet76M80_2040.XSection = GJet76M80_2040.XSection*0.7
GJet76M80_40.XSection = GJet76M80_40.XSection*0.6

QCDDoubleEM76_m80_pt3040.XSection = QCDDoubleEM76_m80_pt3040.XSection*0.8
QCDDoubleEM76_m80_pt40.XSection = QCDDoubleEM76_m80_pt40.XSection*0.8

from tHqAnalyzer.HaNaMiniAnalyzer.Plotter import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan, kBlue
dataSamples = SampleType("Data" , kBlack , [ DoubleEG76D , DoubleEG76C ] ) # the first item must be data
higgsSamples = SampleType("Higgs" , kRed , [ GluGluH76GG , VBFH76GG , VH76GG ] )
multigSamples = SampleType("multi-#gamma" , kOrange , [ DiGG76 , GJet7640M80 , GJet76M80_2040 , GJet76M80_40 , ZG2LG76 ] )
QCDSamples = SampleType("QCD" , kGreen+2 , [QCDDoubleEM76_m4080_pt30 , QCDDoubleEM76_m80_pt3040 , QCDDoubleEM76_m80_pt40 ] )
topSamples = SampleType("TOP" , kBlue , [TTGG76 , TTGJ76 , TGJ76 , ttH76GG ] )
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

