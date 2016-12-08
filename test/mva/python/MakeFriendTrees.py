#!/usr/bin/env python

from tHqAnalyzer.HaNaMiniAnalyzer.ExtendedSample import *
from ROOT import TSystem, gSystem, gROOT, TCanvas, TH1D, TDirectory, gDirectory
import sys
sys.path.append('../')

prefix = "tree"
nTuples = "/home/hbakhshi/Downloads/CERNBox/Personal/Projects/tHq/nTuples/FoxWolfram2/;/home/hbakhshi/Downloads/CERNBox/Personal/Projects/tHq/nTuples/OptimizationEle/"

gSystem.CompileMacro("MakeFriendTrees.C" , "k")
gSystem.Load("bin/MakeFriendTrees.so")
from ROOT import MakeFriendTrees

c = TCanvas()
histos = {}

from Samples80tHq.Samples import *
for s in MicroAOD80Samples:
    if False: # not s.IsData: #not s.Name == "ttH"
        print "Skipping sample %s" % s.Name
        continue
    else:
        print s.Name

    es = ExtendedSample( s )
    es.LoadJobs( nTuples )
    es.LoadTree("tHq/Trees/Events")

    MakeFriendTrees( es.Tree , "dataset/" + s.Name )
    continue
    
    fnew = TFile.Open( "4Dec/" + s.Name + ".root" )
    treeF = fnew.Get("friend")

    es.Tree.AddFriend( treeF )

    gROOT.cd()
    if es.Tree.Draw("BDT>>h%s(18,-0.3,0.3)" % (s.Name) , "LeptonType == 4" ) > 0 :
        name = s.Name
        if s.IsData :
            name = "Data"
        if name in histos.keys():
            histos[name].Add( gDirectory.Get( "h%s" % (s.Name) ).Clone( "hClone%s" % (s.Name) ) )
        else:
            histos[name] = gDirectory.Get( "h%s" % (s.Name) ).Clone( "hClone%s" % (s.Name) ) 
            
    fnew.Close()

opt = ""
for sample in histos :
    histos[sample].DrawNormalized(opt)
    opt = "SAMES"
