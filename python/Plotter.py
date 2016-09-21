from ROOT import TDirectory, TFile, TCanvas , TH1D , TH1 , THStack, TList, gROOT, TLegend, TPad, TLine, gStyle, TTree , TObject , gDirectory, TEntryList

import os
import sys
import Sample
from array import array

from ExtendedSample import *
from SampleType import *
from Property import *

class HistInfo:
    def __init__(self , name , varname = None , nbins = None , _from = None , to = None ):
        if isinstance(name, HistInfo) and type(varname) == str and nbins == None and _from == None and to == None :
            s = name.Name
            if len(name.Name.split("_")) > 1 :
                s = name.Name.split("_")[-1]
            self.Name = varname + "_" + s
            self.VarName = name.VarName
            
            self.nBins = name.nBins
            self.From = name.From
            self.To = name.To

        elif type(name) == str and type(varname) == str and type(nbins) == int and ( type(_from) or type(_from) == int ) and ( type(to) == float or type(to) == int ) :
       
            self.Name = name
            self.VarName = varname

            self.nBins = nbins
            self.From = float(_from)
            self.To = float(to)

        else:
            print "Initiate histinfo correctly, the given parameters are not allowd"
      
    def MakeName(self , sName , index = 0 ):
        return "%s_%s_%d" % (sName , self.Name , index )

class CutInfo:
    def __init__(self, name , cut , weight):
        self.Name = name
        self.Cut = cut
        self.Weight = weight

        self.ListOfEvents = {}
        self.ListOfHists = []
        self.AllTH1s = {}

    def AddHist(self, name , varname = None , nbins = None , _from = None , to = None ):
        if isinstance(name , HistInfo) and varname == None and nbins == None and _from == None and to == None :
            self.ListOfHists.append( HistInfo(name , self.Name) )
        elif type(name) == str and type(varname) == str and type(nbins) == int and ( type(_from) == float or type(_from) == int ) and ( type(to) == float or type(to) == int ) :
            self.ListOfHists.append( HistInfo( self.Name + "_" + name , varname , nbins , _from , to) )
        else:
            print "Initiate histinfo correctly, the given parameters to AddHists are not allowd(%s=%s,%s=%s,%s=%s,%s=%s,%s=%s)" % (type(name),name,type(varname),varname,type(nbins),nbins,type(_from),_from,type(to),to)
        
    def SetWeight(self, w):
        self.Weight = w
        
    def Weights(self, index = 0):
        if hasattr( self , "Weight"):
            #print self.Weight
            return (self.Weight  % (index) )
        else:
            return ("Weight.W%d" % (index) )

    def LoadHistos( self , samplename , isdata , tree , indices=[0] ):
        tree.SetEntryList( None )
        nLoaded = tree.Draw( ">>list_%s_%s"%(samplename, self.Name) , self.Cut , "entrylist" )
        #gDirectory.ls()
        lst = gDirectory.Get( "list_%s_%s"%(samplename, self.Name) )
        print "\t\tEvents from tree are loaded (%s , %s), %d" % (self.Name , self.Cut , nLoaded)
        print "\t\tHistograms from tree are being created"
        if nLoaded < 0:
            print "Error in loading events with cut (%s) from dataset (%s), nLoaded = %d" % (self.Cut,samplename , nLoaded)
        if nLoaded < 1 :
            self.ListOfEvents[samplename] = TEntryList( "list_%s" % (samplename) , self.Cut , tree )
        else:
            self.ListOfEvents[samplename] = lst

        #print self.ListOfEvents[samplename]
        #self.ListOfEvents[samplename].Print()
        tree.SetEntryList( self.ListOfEvents[samplename] )
        
        ret = {}
        for hist in self.ListOfHists:
            ret[hist.Name] = {}
            for n in indices:
                hname =  hist.MakeName(samplename , n)
                gROOT.cd()
                
                tocheck = ["jPt","jEta" , "jPhi","bjPt" ]
                for sss in tocheck:
                    if sss in hist.Name:
                        print "%s : %d , %.2f , %.2f" % (hist.Name , hist.nBins , hist.From , hist.To)

                if nLoaded > 0:
                    tree.Draw( "%s>>cloned_%s(%d,%.1f,%.1f)" % ( hist.VarName , hname , hist.nBins , hist.From , hist.To ) ,
                                    self.Weights( n ) )
                    setattr( self , hname , gDirectory.Get( "cloned_"+hname ).Clone( hname ) )
                else :
                    hcloned_empty = TH1D( "%s" % (hname) , "" ,  hist.nBins , hist.From , hist.To )
                    setattr( self , hname , hcloned_empty )
                hhh = getattr( self , hname )
                print "\t\t\tHisto %s[%d] created ([%d,%.1f,%1f] and integral=%.2f, average=%.2f)" % ( hist.Name , n , hhh.GetNbinsX() , hhh.GetBinLowEdge(1) , hhh.GetBinLowEdge( hhh.GetNbinsX() ) + hhh.GetBinWidth( hhh.GetNbinsX() )  , hhh.Integral() , hhh.GetMean() )
                hhh.SetBit(TH1.kNoTitle)
                hhh.SetLineColor( 1 )
                hhh.SetLineWidth( 2 )
                if not isdata :
                    hhh.SetFillStyle( 1001 )
                else:
                    hhh.SetStats(0)

                ret[hist.Name][n] = hhh

        return ret
        
class Plotter:
    def __init__(self):
        TH1.SetDefaultSumw2(True)
        self.Samples = []
        self.Props = {}
        self.TreePlots = []


    def AddTreePlots( self , selection ):
        self.TreePlots.append( selection )
        
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
            print "Creating histos for : %s" % (st.Name)
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

    def DrawAll(self , normtodata ):
        gStyle.SetOptTitle(0)
        for prop in self.Props :
            self.Props[prop].Draw(normtodata)

    def GetProperty(self , propname):
        return self.Props[propname]
    
    def Write(self, fout , normtodata ):
        print "Starter writing the plots to the output file..."
        for propname in self.Props :
            propdir = None
            for selection in self.TreePlots:
                for t in selection.ListOfHists:
                    if t.Name == propname :
                        seldirname = selection.Name
                        seldir = fout.GetDirectory(seldirname)
                        if not seldir:
                            seldir = fout.mkdir( seldirname )
                        propdirname = propname
                        if len(propname.split("_")) > 1 :
                            propdirname = propname.split("_")[-1]
                        propdir = seldir.mkdir( propdirname )
            if not propdir :
                propdir = fout.mkdir( propname )
            self.Props[propname].Write(propdir, normtodata)
            fout.cd()
