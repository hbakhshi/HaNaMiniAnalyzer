from ROOT import TDirectory, TFile, TCanvas , TH1D , TH1 , TH2D , THStack, TList, gROOT, TLegend, TPad, TLine, gStyle, TTree , TObject , gDirectory, TEntryList, TEventList

import os
import sys
import Sample
from array import array
from collections import OrderedDict
from ExtendedSample import *
from SampleType import *
from Property import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class HistInfo:
    def __init__(self , name , varname = None , nbins = None , _from = None , to = None , title = "" ):
        self.Title = title
        self.TwoD = False
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
        elif isinstance(name, HistInfo) and isinstance(varname, HistInfo) and type(nbins) == str  and _from == None and to == None : #2d
            s = name.Name
            if len(name.Name.split("_")) > 1 :
                s = name.Name.split("_")[-1]
                
            s2 = varname.Name
            if len(s2.split("_")) > 1 :
                s2 = s2.split("_")[-1]

            self.Name = nbins + "_" + s + "vs" + s2
            self.VarName = name.VarName + ":" + varname.VarName

            self.H1 = name
            self.H2 = varname
            self.TwoD = True
        else:
            print "Initiate histinfo correctly, the given parameters are not allowd"

    def MakeEmptyHist(self , sName , index = 0):
        hname = self.MakeName( sName , index )
        if hasattr(self, "emptyhist" ):
            return self.emptyhist
        elif self.TwoD:
            self.emptyhist = TH2D( hname , self.Title , self.H2.nBins , self.H2.From , self.H2.To , self.H1.nBins , self.H1.From , self.H1.To )
        else:
            self.emptyhist = TH1D( hname , self.Title , self.nBins , self.From , self.To)

        return self.emptyhist
        
    def Bins(self):
        if self.TwoD:
            return "%s,%s" % (self.H2.Bins() , self.H1.Bins())
        else:
            return "%d,%.2f,%.2f" % (self.nBins , self.From , self.To)
            
    def MakeName(self , sName , index = 0 ):
        return "%s_%s_%d" % (sName , self.Name , index )

class CutInfo:
    def __init__(self, name , cut , weight , title = ""):
        self.Name = name
        self.Cut = cut
        self.Weight = weight

        self.ListOfEvents = {}
        self.ListOfHists = []
        self.AllTH1s = {}

        self.Title = name if title == "" else title
        
    def AddHist(self, name , varname = None , nbins = None , _from = None , to = None , Title = "" ):
        if isinstance(name , HistInfo) and varname == None and nbins == None and _from == None and to == None :
            self.ListOfHists.append( HistInfo(name , self.Name , title = Title ) )
        elif type(name) == str and type(varname) == str and type(nbins) == int and ( type(_from) == float or type(_from) == int ) and ( type(to) == float or type(to) == int ) :
            self.ListOfHists.append( HistInfo( self.Name + "_" + name , varname , nbins , _from , to , title = Title ) )
        elif isinstance(name , HistInfo) and isinstance(varname , HistInfo) and nbins == None and _from == None and to == None : #2d histogram
            self.ListOfHists.append( HistInfo(name , varname , self.Name , title = Title) )
        else:
            print "Initiate histinfo correctly, the given parameters to AddHists are not allowd(%s=%s,%s=%s,%s=%s,%s=%s,%s=%s)" % (type(name),name,type(varname),varname,type(nbins),nbins,type(_from),_from,type(to),to)

        return self.ListOfHists[-1]
        
    def SetWeight(self, w):
        self.Weight = w
        
    def Weights(self, index = 0):
        if hasattr( self , "Weight"):
            #print self.Weight
            return (self.Weight  % (index) )
        else:
            return ("Weight.W%d" % (index) )

    def LoadHistos( self , samplename , isdata , tree , indices=[0] ):
        tree.SetEventList( None )
        nLoaded = tree.Draw( ">>list_%s_%s"%(samplename, self.Name) , self.Cut ) # , "entrylist" )
        #gDirectory.ls()
        lst = gDirectory.Get( "list_%s_%s"%(samplename, self.Name) )
        print "%s\t\tEvents from tree are loaded (%s , %s), %d" % (bcolors.UNDERLINE, self.Name , self.Cut , nLoaded )
        print "\t\tHistograms from tree are being created" + bcolors.ENDC
        if nLoaded < 0:
            print "Error in loading events with cut (%s) from dataset (%s), nLoaded = %d" % (self.Cut,samplename , nLoaded)
        if nLoaded < 1 :
            self.ListOfEvents[samplename] = TEventList( "list_%s" % (samplename) , self.Cut ) # , tree ) #TEntryList(
        else:
            self.ListOfEvents[samplename] = lst

        #print self.ListOfEvents[samplename]
        #self.ListOfEvents[samplename].Print()
        #self.ListOfEvents[samplename].SetTreeName( tree.GetName() )
        tree.SetEventList( self.ListOfEvents[samplename] )

            
        ret = {}
        for hist in self.ListOfHists:
            ret[hist.Name] = {}
            for n in indices:
                hname =  hist.MakeName(samplename , n)
                gROOT.cd()
                
                tocheck = [] #"jPt","jEta" , "jPhi","bjPt" ]
                for sss in tocheck:
                    if sss in hist.Name:
                        print "%s : %d , %.2f , %.2f" % (hist.Name , hist.nBins , hist.From , hist.To)

                if nLoaded > 0:
                    tree.Draw( "%s>>cloned_%s(%s)" % ( hist.VarName , hname , hist.Bins() ) ,
                               "" if isdata else self.Weights( n ) )
                    setattr( self , hname , gDirectory.Get( "cloned_"+hname ).Clone( hname ) )
                else :
                    hcloned_empty = hist.MakeEmptyHist( samplename , n )
                    setattr( self , hname , hcloned_empty )
                hhh = getattr( self , hname )
                hhh.SetTitle( hist.Title )
                hhh.SetTitle( self.Title )
                rebined = False
                correct = True
                color = bcolors.OKBLUE
                if not hist.TwoD :
                    if not hhh.GetNbinsX() == hist.nBins :
                        if hhh.GetNbinsX()%hist.nBins == 0:
                            hhh.Rebin( hhh.GetNbinsX()/hist.nBins )
                            rebined = True
                            color = bcolors.WARNING
                        else:
                            correct = False
                            color = bcolors.FAIL
                        
                print "%s\t\t\tHisto %s[%d] created ([%d,%.1f,%1f] and integral=%.2f, average=%.2f)%s" % (color, hist.Name , n , hhh.GetXaxis().GetNbins() , hhh.GetXaxis().GetBinLowEdge(1) , hhh.GetXaxis().GetBinLowEdge( hhh.GetXaxis().GetNbins() ) + hhh.GetXaxis().GetBinWidth( hhh.GetXaxis().GetNbins() ) , hhh.Integral() , hhh.GetMean() , bcolors.ENDC )
                        
                    
                hhh.SetLineColor( 1 )
                hhh.SetLineWidth( 2 )
                hhh.SetBit(TH1.kNoTitle)
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
            print "%sCreating histos for : %s%s" % (bcolors.OKGREEN , st.Name , bcolors.ENDC)
            st.LoadHistos( lumi , dirName , cftName , self.TreePlots )
            for prop in st.AllHists:
                if not prop in self.Props:
                    self.Props[prop] = Property( prop , OrderedDict() , None, None , [] )
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
        print "%sStarted writing the plots to the output file (%s)...%s" % (bcolors.BOLD, fout.GetPath() , bcolors.ENDC)
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
