from ROOT import TDirectory, TFile, TCanvas , TH1D , TH1 , THStack, TList, gROOT, TLegend, TPad, TLine, gStyle

class Histogram:
    def __init__(self, Samples , directory):
        self.PropName = directory.GetName()
        
        dircontents = directory.GetListOfKeys()
        firsthisto = directory.Get( dircontents.At(0).GetName() )
        #firsthisto.Print("ALL")
        self.ForLegend = {}
        self.XSections = {}
        self.AllSampleHistos = {}

        for sample in Samples:
            if sample.IsData:
                self.DataSName = sample.HistoCat


            # h_in_dir = directory.Get( "%s_%s" % ( self.PropName , sample.Name ) )
            # if h_in_dir :
            #     h_in_dir.reset()
            #     setattr( self , sample.Name , h_in_dir )
            # else:
            gROOT.cd()
            hnew = firsthisto.Clone("%s_%s" % ( self.PropName , sample.Name ) )
            hnew.Reset()
            setattr( self , sample.Name , hnew )
                
            hhh = getattr( self , sample.Name )
            hhh.SetLineColor( 1 )
            hhh.SetLineWidth( 2 )
            if not sample.IsData :
                hhh.SetFillColor( sample.Color )
                hhh.SetFillStyle( 1001 )
            else:
                hhh.SetStats(0)

            self.AllSampleHistos[sample.Name] = hhh    
                
            if( self.ForLegend.get(sample.HistoCat) ):
                self.ForLegend[sample.HistoCat].append( sample.Name )
            else:
                self.ForLegend[sample.HistoCat] = [ sample.Name ]

            self.XSections[sample.Name] = sample.XSection

    def AddFile(self , directory):
        ##find all relevant histograms in the file and add them to your histos
        for sample in self.AllSampleHistos:
            h_in_dir = directory.Get( "%s/%s_%s" % ( self.PropName , self.PropName , sample ) )
            if h_in_dir :
                self.AllSampleHistos[sample].Add( h_in_dir )
                

    def Write(self, fout ):
        fout.mkdir( self.PropName ).cd()
        for sample in self.AllSampleHistos:
            self.AllSampleHistos[sample].Write()
        if hasattr( self, "Canvas" ):
            self.Canvas.Write()
            for leg in self.FinalHistos:
                self.FinalHistos[leg].Write()
            self.Stack.GetStack().Last().Write("SumMC")
        fout.cd()
        

    @staticmethod
    def AddLabels( histo , labels ):
        if labels :
            for i in range(1, histo.GetNbinsX()+1 ):
                if not i > len(labels) :
                    histo.GetXaxis().SetBinLabel( i , labels[i-1] )

    def Draw(self , lumi , cft , labels = None ):
        gStyle.SetOptTitle(0)
        self.FinalHistos={}
        for sample in self.AllSampleHistos:
            Histogram.AddLabels( self.AllSampleHistos[sample] , labels )
            self.AllSampleHistos[sample].SetBit(TH1.kNoTitle); 
            if sample in self.ForLegend[ self.DataSName ] :
                continue
            ntotal = getattr( cft , sample ).GetBinContent( 1 )
            if ntotal == 0:
                print "Sample %s has no entries" % (sample)
                continue
            factor = lumi*self.XSections[sample]/ntotal
            #print "%s factor : (%.2f*%.2f)/%.0f = %.3f" % (sample , lumi , self.XSections[sample] , ntotal  , factor)
            self.AllSampleHistos[sample].Scale(factor)

        self.Stack = THStack("%s_stack" % (self.PropName) , self.PropName )
        #Histogram.AddLabels( self.Stack.GetHistogram() , labels )
        for finalh in self.ForLegend:
            for hname in self.ForLegend[finalh]:
                #print "Adding %s to %s" % ( hname , finalh )
                if self.FinalHistos.get(finalh) :
                    self.FinalHistos[finalh].Add( self.AllSampleHistos[hname] )
                else:
                    self.FinalHistos[finalh] = self.AllSampleHistos[hname].Clone( "_%s_%s" % (self.PropName , finalh) )
                    Histogram.AddLabels( self.FinalHistos[finalh] , labels )
                    self.FinalHistos[finalh].SetBit(TH1.kNoTitle); 
                    #self.FinalHistos[finalh].SetLineColor( 0 )
                    self.FinalHistos[finalh].SetTitle( finalh )

            if finalh == self.DataSName :
                self.DataHisto = self.FinalHistos[finalh]
            else :
                self.Stack.Add( self.FinalHistos[finalh] )
        

        self.Canvas = TCanvas("%s_C" % (self.PropName) )
        self.Pad1 = TPad("pad1","pad1",0,0.25,1,1)
        self.Pad1.SetBottomMargin(0.1)
        self.Pad1.Draw()
        self.Pad1.cd()

        self.DataHisto.Draw("E")
        #getattr( self , self.DataSName ).Draw("E")
        self.Stack.Draw("HIST SAME")
        self.DataHisto.Draw("E SAME P")
        #getattr( self , self.DataSName ).Draw("E SAME")

        self.Legend = TLegend(0.7,0.6,0.9,0.9,"","brNDC")
        entry=self.Legend.AddEntry( self.DataHisto , "Data" , "lp" )
        for finalh in reversed( self.ForLegend.keys() ):
            if finalh == self.DataSName :
                continue
            self.Legend.AddEntry( self.FinalHistos[finalh] , finalh , "f" )
        self.Legend.Draw()


        self.Canvas.cd()
        self.Pad2 = TPad("pad2","pad2",0,0,1,0.24)
        self.Pad2.SetTopMargin(0.1)
        self.Pad2.SetBottomMargin(0.1)
        self.Pad2.Draw()
        self.Pad2.cd()

        self.Ratio = self.DataHisto.Clone("Ratio_%s" % (self.PropName) )
        self.Ratio.SetStats(0)
        self.Ratio.Divide( self.Stack.GetStack().Last() )
        if labels :
            Histogram.AddLabels( self.Ratio , [ "" for s in labels ] ) 
        self.Ratio.SetMarkerStyle(20)
        self.Ratio.GetYaxis().SetRangeUser(0,2)
        self.Ratio.GetXaxis().SetLabelSize( 0.)
        self.Ratio.GetYaxis().SetTitle("Data / MC")
        #self.Ratio.GetXaxis().SetTitle(xtitle) 
        self.Ratio.GetXaxis().SetTitleSize(0.2) 
        self.Ratio.GetXaxis().SetTitleOffset(0.25)
        self.Ratio.GetYaxis().SetLabelSize(0.1)
        self.Ratio.GetXaxis().SetTickLength(0.09)
        self.Ratio.GetYaxis().SetTitleSize(0.18)
        self.Ratio.GetYaxis().SetNdivisions(509)
        self.Ratio.GetYaxis().SetTitleOffset(0.25)
        self.Ratio.SetFillStyle(3001)
        self.Ratio.Draw("ep")

        self.LineOne = TLine(self.Ratio.GetXaxis().GetXmin(), 1.00, self.Ratio.GetXaxis().GetXmax(), 1.00)
        self.LineOne.SetLineWidth(2)
        self.LineOne.SetLineStyle(7)
        self.LineOne.Draw()
