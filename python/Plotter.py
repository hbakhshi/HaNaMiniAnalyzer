from ROOT import TDirectory, TFile, TCanvas , TH1D , TH1 , THStack, TList, gROOT, TLegend, TPad, TLine, gStyle, TTree , TObject , gDirectory

import os
import sys
import Sample
from array import array

from ExtendedSample import *
from SampleType import *
from Property import *

class HistInfo:
    def __init__(self , name , varname , selStep , nbins , _from , to , additionalcut , selname = "" ):
        self.Name = name
        self.VarName = varname
        self.SelectionStep = selStep

        self.nBins = nbins
        self.From = _from
        self.To = to

        self.Cut = additionalcut
        if selname == "":
            self.SelName = "SelStep%d" % (self.SelectionStep)
        else:
            self.SelName = selname

    def SetWeight(self, w):
        self.Weight = w
        
    def Weights(self, index = 0):
        if hasattr( self , "Weight"):
            return (self.Weight  % (index) )
        else:
            return ("Weight.W%d" % (index) )

    def MakeName(self , sName , index = 0 ):
        return "%s_%s_%d" % (sName , self.Name , index )

    def MakeCut(self , index = 0):
        addcut = ""
        if not self.Cut == "":
            addcut = (" && " + self.Cut)
        return "%s*(SelectionStep>%d%s)" % ( self.Weights(index) , self.SelectionStep , addcut)

class Plotter:
    def __init__(self):
        TH1.SetDefaultSumw2(True)
        self.Samples = []
        self.Props = {}
        self.TreePlots = []

    def AddTreePlot( self , name , varname , selStep , nbins , _from , to , addcut = "" , selname = "" ):
        self.TreePlots.append( HistInfo( name , varname , selStep , nbins , _from , to , addcut , selname ) )
        return self.TreePlots[-1]
        
    def AddSampleType(self , st):
        self.Samples.append(st)

               
    def AddLabels(self , hist , labels ):
        if labels :
            self.Props[hist].SetLabels(labels)

    def Rebin(self , hist , newbins):
        self.Props[hist].Rebin( newbins )
                        
    def GetData(self, propname):
        for st in self.Samples:
            if st.IsData():
                return st.AllHists[propname]
        return None


    def LoadHistos(self  , lumi , dirName = "tHq" , cftName = "CutFlowTable"):
        for st in self.Samples :
            st.LoadHistos( lumi , dirName , cftName , self.TreePlots )
            for prop in st.AllHists:
                if not prop in self.Props:
                    self.Props[prop] = Property( prop , {} , None, None , [] )
                self.Props[prop].Samples += [ s.AllHists[prop][0] for s in st.Samples ]
                if st.IsData():
                    self.Props[prop].Data = st.AllHists[prop]
                elif st.IsSignal:
                    self.Props[prop].Signal = st.AllOtherHists[prop].values()
                else :
                    self.Props[prop].Bkg[st.Name] = st.AllHists[prop]

    def DrawAll(self ):
        gStyle.SetOptTitle(0)
        for prop in self.Props :
            self.Props[prop].Draw()

    def GetProperty(self , propname):
        return self.Props[propname]
    
    def Write(self, fout ):
        for propname in self.Props :
            propdir = None
            for t in self.TreePlots:
                if t.Name == propname :
                    seldirname = t.SelName
                    seldir = fout.GetDirectory(seldirname)
                    if not seldir:
                        seldir = fout.mkdir( seldirname )
                    propdirname = propname
                    if len(propname.split("_")) > 1 :
                        propdirname = "_".join(propname.split("_")[0:-1])
                    propdir = seldir.mkdir( propdirname )
            if not propdir :
                propdir = fout.mkdir( propname )
            self.Props[propname].Write(propdir)
            fout.cd()
