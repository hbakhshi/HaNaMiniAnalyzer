from ROOT import TDirectory, TFile, TCanvas , TH1D , TH1 , THStack, TList, gROOT, TLegend, TPad, TLine, gStyle

import os
import sys
import Sample

class ExtendedSample: #extend the sample object to store histograms
    def __init__( self , sample ):
        self.Name = sample.Name 
        self.XSection = sample.XSection 
        self.LHEWeight = sample.LHEWeight 
        self.DSName = sample.DSName 
        self.Prefix = sample.Prefix
        self.IsData = sample.IsData
        
        self.Files = sample.Files
        self.Jobs = sample.Jobs

        if sample.ParentSample :
            self.ParentSample = ExtendedSample( sample.ParentSample )
        else :
            self.ParentSample = None

    def GetCFT(self):
        if not hasattr( self, "CutFlowTableName" ):
            return None
        if not self.CutFlowTableName in self.AllHists:
            return None
        return self.AllHists[self.CutFlowTableName] 
    
    def GetNTotal(self) :
        if self.ParentSample :
            if not self.ParentSample.GetCFT() :
                print "Loading parent sample"
                self.ParentSample.LoadHistos( self.DirName , self.CutFlowTableName , [self.CutFlowTableName] )
                print "Loaded"
            return self.ParentSample.GetNTotal()
        else :
            if not self.GetCFT() :
                return -1
            return self.GetCFT().GetBinContent( 1 )

    def NormalizeHistos(self, lumi):
        if self.IsData :
            return
        self.nTotal = self.GetNTotal()
        if self.nTotal == 0:
            print "Sample %s has no entries" % (self.Name)
            return
        self.XSFactor = lumi*self.XSection/self.nTotal
        #print "%s factor : (%.2f*%.2f)/%.0f = %.3f" % (sample , lumi , self.XSections[sample] , ntotal  , factor)
        for h in self.AllHists:
            self.AllHists[h].Scale(self.XSFactor)

    def LoadHistos(self , dirName = "tHq" , cftName = "CutFlowTable" , loadonly = []):
        self.CutFlowTableName = cftName
        self.DirName = dirName
        self.AllHists = {}
        for Job in self.Jobs :
            finame = Job.Output
            sys.stdout.write("\r%s : %d of %d" % (self.Name , Job.Index+1 , len(self.Jobs)))
            sys.stdout.flush()
            ff = None
            if os.path.isfile( finame ):
                ff = TFile.Open(finame)
            else:
                print "File %d of sample %s doesn't exist, skip it" % (Job.Index , self.Name)
                continue
            dir = ff.GetDirectory(dirName)
            if not dir :
                print "File %d of sample %s is not valid, skip it" % (Job.Index , self.Name)
                continue
            for dir__ in dir.GetListOfKeys() :
                if not dir__.IsFolder():
                    continue
                propname = dir__.GetName()
                if len(loadonly) > 0 and not propname in loadonly :
                    continue
                dir_ = dir.GetDirectory( propname )
                if propname in self.AllHists.keys() :
                    dircontents = dir_.GetListOfKeys()
                    firsthisto = dir_.Get( dircontents.At(0).GetName() )
                    self.AllHists[propname].Add( firsthisto )
                else :
                    dircontents = dir_.GetListOfKeys()
                    firsthisto = dir_.Get( dircontents.At(0).GetName() )
                    if not firsthisto.ClassName().startswith("TH"):
                        continue
                    gROOT.cd()
                    hnew = firsthisto.Clone("%s_%s" % ( propname , self.Name ) )
                    hnew.SetBit(TH1.kNoTitle)
                    #hnew.Reset()
                    setattr( self , propname , hnew )
                    hhh = getattr( self , propname )
                    hhh.SetLineColor( 1 )
                    hhh.SetLineWidth( 2 )
                    if not self.IsData :
                        #hhh.SetFillColor( self.Color )
                        hhh.SetFillStyle( 1001 )
                    else:
                        hhh.SetStats(0)

                    self.AllHists[propname] = hhh    
                    
            ff.Close()
        if len(self.AllHists)==0 :
            return False
        else:
            return True

class SampleType:
    def __init__(self , name , color , samples = [] , signal = False ):
        self.Name = name 
        self.Color = color
        self.Samples = [ExtendedSample(s) for s in samples]
        self.IsSignal = signal

    def IsData(self):
        if len(self.Samples) == 0 :
            return False
        return self.Samples[0].IsData

    def LoadHistos(self , lumi , dirName = "tHq" , cftName = "CutFlowTable"):
        self.AllHists = {}
        for s in self.Samples :
            if s.LoadHistos( dirName , cftName ):
                s.NormalizeHistos( lumi )
            print ""
            for propname in s.AllHists:
                if propname in self.AllHists.keys() :
                    self.AllHists[propname].Add(s.AllHists[propname])
                else :
                    gROOT.cd()
                    hnew = s.AllHists[propname].Clone("%s_%s" % ( propname , self.Name ) )
                    hnew.SetTitle( self.Name )
                    hnew.SetBit(TH1.kNoTitle) 
                    setattr( self , propname , hnew )
                    hhh = getattr( self , propname )
                    hhh.SetLineColor( 1 )
                    hhh.SetLineWidth( 2 )
                    if not self.IsData() :
                        hhh.SetFillColor( self.Color )
                        hhh.SetFillStyle( 1001 )
                    else:
                        hhh.SetStats(0)

                    self.AllHists[propname] = hhh    


class Plotter:
    def __init__(self):
        self.Samples = []
        self.Props = []

    def AddSampleType(self , st):
        self.Samples.append(st)

    @staticmethod
    def addLabels(histo , labels):
        for i in range(1, histo.GetNbinsX()+1 ):
            if not i > len(labels) :
                histo.GetXaxis().SetBinLabel( i , labels[i-1] )

    def AddLabels(self , hist , labels ):
        if labels :
            for st in self.Samples:
                Plotter.addLabels( st.AllHists[hist] , labels )
                for s in st.Samples :
                    Plotter.addLabels( s.AllHists[hist] , labels )

 
    def GetStack(self, propname):
        stackname = "%s_stack" % (propname)
        if not hasattr(self , stackname):
            #print stackname
            setattr( self, stackname , THStack( stackname , propname ) )
            for st in self.Samples:
                if not st.IsData() and not st.IsSignal:
                    getattr( self, stackname ).Add( st.AllHists[propname] )

        return getattr(self , stackname)

    def GetData(self, propname):
        for st in self.Samples:
            if st.IsData():
                return st.AllHists[propname]
        return None

    def GetCanvas(self, propname , padid):
        canvasname = "%s_canvas" % (propname)
        pad1name = "%s_pad1" % (propname)
        pad2name = "%s_pad2" % (propname)
        if not hasattr(self , canvasname):
            #print canvasname
            setattr( self, canvasname , TCanvas( canvasname ) )
            setattr( self, pad1name  ,  TPad(pad1name ,pad1name,0,0.25,1,1) )
            getattr( self, pad1name).SetBottomMargin(0.1)
            getattr( self, pad1name).Draw()

            getattr( self, canvasname).cd()

            setattr( self, pad2name , TPad( pad2name,pad2name,0,0,1,0.24) )
            getattr( self, pad2name).SetTopMargin(0.1)
            getattr( self, pad2name).SetBottomMargin(0.1)
            getattr( self, pad2name).Draw()

        if padid == 0:
            getattr( self, canvasname).cd()
        elif padid == 1:
            getattr( self, pad1name).cd()
        if padid == 2:
            getattr( self, pad2name).cd()

        return getattr(self , canvasname)

    def GetLegend(self , propname ):
        legendname = "%s_legend" % (propname)
        if not hasattr(self , legendname):
            setattr( self , legendname , TLegend(0.7,0.6,0.9,0.9,"","brNDC") )
            getattr( self , legendname).SetName( legendname )
            getattr( self , legendname).AddEntry( self.GetData(propname) , "Data" , "lp" )
            for st in reversed( self.Samples ):
                if not st.IsData() and not st.IsSignal:
                    getattr( self , legendname).AddEntry( st.AllHists[propname] , st.Name , "f" )
        return getattr( self , legendname)

    def GetRatioPlot(self, propname):
        rationame = "%s_Ratio" % (propname)
        if not hasattr(self, rationame):
            setattr( self, rationame , self.GetData(propname).Clone( rationame ) )
            getattr( self, rationame).SetStats(0)
            getattr( self, rationame).Divide( self.GetStack(propname).GetStack().Last() )
            Plotter.addLabels( getattr( self, rationame) , [ "" for ii in range(0 , self.GetData(propname).GetNbinsX()+1 ) ] )
            getattr( self, rationame).SetMarkerStyle(20)
            getattr( self, rationame).GetYaxis().SetRangeUser(0,2)
            getattr( self, rationame).GetXaxis().SetLabelSize( 0.)
            getattr( self, rationame).GetYaxis().SetTitle("Data / MC")
            getattr( self, rationame).GetXaxis().SetTitleSize(0.2) 
            getattr( self, rationame).GetXaxis().SetTitleOffset(0.25)
            getattr( self, rationame).GetYaxis().SetLabelSize(0.1)
            getattr( self, rationame).GetXaxis().SetTickLength(0.09)
            getattr( self, rationame).GetYaxis().SetTitleSize(0.18)
            getattr( self, rationame).GetYaxis().SetNdivisions(509)
            getattr( self, rationame).GetYaxis().SetTitleOffset(0.25)
            getattr( self, rationame).SetFillStyle(3001)
            
        return getattr( self, rationame)

    def GetRatioUnc(self, propname):
        rationame = "%s_RatioUncert" % (propname)
        if not hasattr(self, rationame):
            mc = self.GetStack(propname).GetStack().Last()
            setattr( self, rationame , mc.Clone( rationame ) )
            getattr( self, rationame).SetStats(0)
            getattr( self, rationame).Divide(mc)
            Plotter.addLabels( getattr( self, rationame) , [ "" for ii in range(0 , self.GetData(propname).GetNbinsX()+1 ) ] )
            #getattr( self, rationame).SetMarkerStyle(20)
            getattr( self, rationame).GetYaxis().SetRangeUser(0,2)
            #getattr( self, rationame).GetXaxis().SetLabelSize( 0.)
            getattr( self, rationame).GetYaxis().SetTitle("Data / MC")
            getattr( self, rationame).GetXaxis().SetTitleSize(0.2) 
            getattr( self, rationame).GetXaxis().SetTitleOffset(0.25)
            getattr( self, rationame).GetYaxis().SetLabelSize(0.1)
            getattr( self, rationame).GetXaxis().SetTickLength(0.09)
            getattr( self, rationame).GetYaxis().SetTitleSize(0.18)
            getattr( self, rationame).GetYaxis().SetNdivisions(509)
            getattr( self, rationame).GetYaxis().SetTitleOffset(0.25)
            getattr( self, rationame).SetFillStyle(3001)
            getattr( self, rationame).SetFillColor(1)
            
        return getattr( self, rationame)


    def GetLineOne(self, propname):
        linename = "%s_lineone" % (propname)
        if not hasattr(self, linename):
            setattr( self , linename , TLine(self.GetRatioPlot(propname).GetXaxis().GetXmin(), 1.00, self.GetRatioPlot(propname).GetXaxis().GetXmax(), 1.00) )
            getattr( self , linename).SetLineWidth(2)
            getattr( self , linename).SetLineStyle(7)

        return getattr(self, linename)


    def LoadHistos(self  , lumi , dirName = "tHq" , cftName = "CutFlowTable"):
        for st in self.Samples :
            st.LoadHistos( lumi , dirName , cftName )
            for prop in st.AllHists:
                if not prop in self.Props:
                    self.Props.append( prop )

    def DrawAll(self ):
        gStyle.SetOptTitle(0)

       
        for prop in self.Props :
        
            self.GetCanvas( prop , 1 )
            self.GetData(prop).Draw("E")
            self.GetStack(prop).Draw("HIST SAME")
            self.GetData(prop).Draw("E SAME P")
            self.GetLegend(prop).Draw()
            
            self.GetCanvas( prop , 2 )
            self.GetRatioUnc( prop ).Draw("E2")
            self.GetRatioPlot(prop).Draw("ep same")
            self.GetLineOne(prop).Draw()

    def Write(self, fout ):
        for propname in self.Props :
            propdir = fout.mkdir( propname )
            propdir.cd()
            sampledir = propdir.mkdir( "samples" )
            catdir = propdir.mkdir( "cats" )
            
            for sample in self.Samples :
                catdir.cd()
                sample.AllHists[propname].Write()
                self.GetStack(propname).GetStack().Last().Write("SumMC")
                sampledir.cd()
                for ss in sample.Samples:
                    ss.AllHists[propname].Write()
                propdir.cd()
                self.GetCanvas(propname , 0).Write()
            fout.cd()
