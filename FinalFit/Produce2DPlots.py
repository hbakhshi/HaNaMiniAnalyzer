import ROOT
from SignalFit import KappaFramework, CtCvCpInfo
kappa = KappaFramework()
LUMI = 35.9


class EfficiencyCalculator :
    def __init__(self, sample , tree , cuts , vars , color , outDir  ):
        if sample == "thq" or sample == "thw" :
            self.TotalRatios = CtCvCpInfo("TotalRatios_"+sample)
            self.TotalRatios.FillFrom1DHisto( "signals/13May/All_%s.root" % (sample) , "writer/hAll" )
        
        self.Cut = "%s*weight*((CMS_hgg_mass > 100 && CMS_hgg_mass < 180)&&(LeptonType == 1 || LeptonType == 2) && (diphoMVA > -0.4)&&(n_jets >= 2) &&(n_M_bjets==1)&&(MET > 30)  && %s)"
        self.Tree = tree

        self.Bins = cuts
        self.Vars = vars
        self.Color = color

        self.OutDir = outDir
        
        self.Sample = sample

        self.Results = {}
        self.NTot = CtCvCpInfo( "%s_%s" % (self.Sample  , "ntot") ) 
        for cut in self.Bins:
            self.Results[ cut ] = {"eff": CtCvCpInfo( "%s_%s_%s" % (self.Sample , cut , "eff") ) ,
                                   "yield": CtCvCpInfo( "%s_%s_%s" % (self.Sample , cut , "yield") ) }
        self.AllHists = {}
        self.AllEffs = {}
        self.Purity = {}
        
    def MakeCut( self, cut , Ct, Cv ):
        if hasattr( self, "TotalRatios"):
            totalN_factor = self.TotalRatios.ValuesCtCv[ ( -1 , 1 ) ]/self.TotalRatios.ValuesCtCv[ ( Ct , Cv ) ]
            xsecBr_factor = kappa.GetXSecBR( self.Sample , Ct, Cv )
            w_ctcv = "1" if (Ct == -1 and Cv ==1) else "ctcv_%d"%( self.NTot.AllCtCVs.index( (Cv , Ct ) ) )
        
            new_w = totalN_factor*xsecBr_factor*LUMI
            cut = self.Cut % ( "%f*%s" % (new_w , w_ctcv) , cut )
            return cut
        else :
            xsecBr_factor = kappa.GetXSecBR( self.Sample , Ct, Cv )
            new_w = xsecBr_factor*LUMI
            cut = self.Cut % ( "%f" % (new_w ) , cut )
            return cut
            
        
    def Count(self, cut , ct , cv ):
        cut = self.MakeCut( cut , ct , cv )

        ROOT.gROOT.cd()
        self.Tree.Draw("1>>h1(1 , 0 , 10 )" , cut )
        h1 = ROOT.gDirectory.Get("h1")
        return h1.Integral()

    def CalcPurities( self, Totals ):
        for bin in self.Bins :
            self.OutDir.cd()
            dir_ = self.OutDir.GetDirectory( bin )
            if dir_ == None:
                dir_ = self.OutDir.mkdir( bin )
            dir_.cd()
            
            self.Purity[ bin ] = self.Results[ bin ]["yield"].hCtCv.Clone( "%s_%s_purity" % (self.Sample , bin ) )
            self.Purity[ bin ].Divide( Totals[ bin ] )
            self.Purity[ bin ].Write()
            
    def CalcEffs(self, ct = -1 , cv = 1 ):
        nTotal = self.Count( "1==1" , ct , cv )
        w_id = -1 if (ct == -1 and cv ==1) else self.NTot.AllCtCVs.index( (cv , ct ) )
        self.NTot.SetValue( w_id , nTotal )
        for bin in self.Bins :
            nBin = self.Count( self.Bins[bin] , ct , cv )
            effBin = nBin/nTotal
            self.Results[ bin ]["eff"].SetValue( w_id , effBin )
            self.Results[ bin ]["yield"].SetValue( w_id , nBin )

    def CalcAllEffs( self ):
        self.CalcEffs(-1 , 1)
        for i in self.NTot.AllCtCVs :
            self.CalcEffs( i[1] , i[0] )

        self.OutDir.cd()
        self.NTot.GetCanvas().Write()
        
        for cut in self.Bins:
            dir_ = self.OutDir.GetDirectory( cut )
            if dir_ == None:
                dir_ = self.OutDir.mkdir( cut )
            dir_.cd()
            self.Results[cut]["eff"].GetCanvas().Write()
            self.Results[cut]["eff"].hCtCv.Write()
            self.Results[cut]["yield"].GetCanvas().Write()
            
    def MakePlots(self , AdditionalCutName):
        dir_ = self.OutDir.mkdir( AdditionalCutName )
        for var1 in self.Vars :
            var1f = self.Vars[var1][0]
            var1nBins = self.Vars[var1][1]
            var1Min = self.Vars[var1][2]
            var1Max = self.Vars[var1][3]

            hName = "h1_%s_%s_%s" % (self.Sample , var1 , AdditionalCutName)
            ROOT.gROOT.cd()
            self.Tree.Draw( "%s>>%s(%g,%g,%g)" % ( var1f , hName , var1nBins , var1Min , var1Max  ) , self.MakeCut( self.Bins[AdditionalCutName] , -1 , 1 ) ) 
            h1 = ROOT.gDirectory.Get( hName )
            h1.SetTitle( "%s;%s" % (self.Sample , var1 ) )
            h1.SetFillColor( self.Color )
            h1.SetFillStyle( 3005 )
            h1.SetLineColor( self.Color   )
            h1.SetLineWidth( 4   )
            dir_.cd()
            h1.Write()
            
            self.AllHists[ (AdditionalCutName, var1 ) ] = h1
            
            for var2 in self.Vars :
                if var1==var2 :
                    continue
            
                var2f = self.Vars[var2][0]
                var2nBins = self.Vars[var2][1]
                var2Min = self.Vars[var2][2]
                var2Max = self.Vars[var2][3]

                hName = "h2_%s_%s_%s_%s" % (self.Sample , var1 , var2 , AdditionalCutName)

                ROOT.gROOT.cd()
                self.Tree.Draw( "%s:%s>>%s(%g,%g,%g,%g,%g,%g)" % (var2f, var1f , hName , var1nBins , var1Min , var1Max , var2nBins , var2Min , var2Max ) , self.MakeCut( self.Bins[AdditionalCutName] , -1 , 1 )  )

                h2 = ROOT.gDirectory.Get( hName )
                h2.SetTitle( "%s;%s;%s" % (self.Sample , var1 , var2) )
                h2.SetFillColorAlpha( self.Color , 0.9  )
                h2.SetFillStyle( 0 )
                h2.SetLineColor( self.Color )
                h2.SetLineWidth( 4 )
                h2.SetMarkerColor( self.Color   )
                h2.SetMarkerStyle(7)
                dir_.cd()
                h2.Write()

                hEff, hYield , hEffR, hYieldR = self.Make2DEffPlot( h2 )
                hEff.Write()
                hYield.Write()
                hEffR.Write()
                hYieldR.Write()
            
                self.AllHists[ (AdditionalCutName , var1, var2 ) ] = h2
                self.AllEffs[ ( AdditionalCutName , var1, var2 ) ] = (hEff, hYield , hEffR, hYieldR)

    def Make2DEffPlot( self ,hIn ):
        hOut1 = hIn.Clone( hIn.GetName() + "_Eff" )
        hOut2 = hIn.Clone( hIn.GetName() + "_Integrals" )
        hOut3 = hIn.Clone( hIn.GetName() + "_EffR" )
        hOut4 = hIn.Clone( hIn.GetName() + "_IntegralsR" )

        nBinsX = hIn.GetNbinsX()
        nBinsY = hIn.GetNbinsY()
        totalBins = nBinsY*nBinsX + 1
        integral = hIn.Integral()
    
        for i in range( 1 , nBinsX + 1):
            for j in range( 1 , nBinsY + 1 ):
                bin = hIn.GetBin( i , j )
                #ii = hIn.Integral( i , nBinsX +1 , j , nBinsY+1 )
                ii = hIn.Integral( i , nBinsX +1 , 0 , j) 
                hOut1.SetBinContent( bin , ii/integral )
                hOut2.SetBinContent( bin , ii )
                ii = hIn.Integral( i+1 , nBinsX +1 , j+1 , nBinsY+1 )
                hOut3.SetBinContent( bin , 1.0 - (ii/integral) )
                hOut4.SetBinContent( bin , integral-ii )
            
        return hOut1, hOut2 , hOut3 , hOut4
            

class AllEfficiencies :
    def __init__(self , Cuts):
        self.TreeDIR = "/home/hbakhshi/Downloads/tHq_Georgios/output/24_04_17/signal/trees/"
        self.TreeName = "tagsDumper/trees/%s_125_13TeV_THQLeptonicTag"
        self.SampleFiles = { "thq":["THQ.root" , 2], 
                             "thw":["THW.root" , 3],
                             "tth":["TTH.root" , 4],
                             #"vbf":["VBF.root" , 5],
                             #"ggh":["GGH.root" , 6],
                             "vh":["VH.root" , 7] }
        self.Samples = ["thq", "tth" , "thw" , "vh" ]
        self.Vars = {"nJets":["n_jets" , 4 , 2 , 6] , "nLooseBjets":["n_L_bjets"  , 4 , 1 , 5 ] , "jPrimeEta":["abs(fwdjet1_eta)" , 24 , 0 , 4.8 ] }
        self.Cuts = Cuts
        
        self.fOut = ROOT.TFile.Open("2dPlots.root" , "recreate")

        for sample in self.SampleFiles:
            f = ROOT.TFile.Open(  self.TreeDIR + self.SampleFiles[sample][0] )
            self.SampleFiles[sample].append( f )
            
            color = self.SampleFiles[sample][1]
            tree = f.Get( self.TreeName % (sample) )
            self.SampleFiles[sample].append( tree )
            
            currentDir = self.fOut.mkdir( sample )
            currentDir.cd()
            ec = EfficiencyCalculator( sample , tree , self.Cuts , self.Vars , color , currentDir  )
            self.SampleFiles[sample].append( ec )
            

        
    def MakePlots(self):
        for sample in self.SampleFiles:
            ec = self.SampleFiles[sample][-1]
            for cut in self.Cuts :
                ec.MakePlots(cut)

        
        currentDir = self.fOut.mkdir( "Canvases" )
        currentDir.cd()

        for cut in self.Cuts :
            cutDir = currentDir.mkdir( cut )
            auxDir = cutDir.mkdir("Aux")
            for var1 in self.Vars :
                c = ROOT.TCanvas( "%s" % (var1) )
                l = ROOT.TLegend(0.65 , 0.1 , 0.9 , 0.4 )
                l.SetLineColor(0)
                l.SetFillStyle(0)
                l.SetName( "l_%s" % (var1) )
                option = " Hist "
                for sample in self.SampleFiles:
                    ec = self.SampleFiles[sample][-1]
                    h = ec.AllHists[ ( cut, var1 ) ]
                    h.DrawNormalized( option )

                    l.AddEntry( h , sample , "fl" )
                    if not "SAME" in option :
                        option += " SAME"

                l.Draw()
                auxDir.cd()
                l.Write()
                cutDir.cd()
                c.Write()

                for var2 in self.Vars :
                    if var1==var2 :
                        continue
                    c = ROOT.TCanvas( "%s_%s" % (var1, var2) )
                    l = ROOT.TLegend(0.65 , 0.1 , 0.9 , 0.4 )
                    l.SetName( "l_%s_%s" % (var1, var2) )
                    option = " box "
                    for sample in self.SampleFiles:
                        ec = self.SampleFiles[sample][-1]
                        h = ec.AllHists[ ( cut ,var1 , var2) ]
                        h.GetYaxis().SetRangeUser(0,1.)
                        h.Draw( option )
                        l.AddEntry( h , sample , "f" )
                        if not "SAME" in option :
                            option += " SAME"
                    l.Draw()
                    auxDir.cd()
                    l.Write()
                    cutDir.cd()
                    c.Write()

            for var1 in self.Vars :
                for var2 in self.Vars :
                    if var1==var2 :
                        continue
                    SumYields = None
                    SumYieldsR = None
                    for sample in self.SampleFiles:
                        ec = self.SampleFiles[sample][-1]
                        hEff, hYield, hEffR, hYieldR = ec.AllEffs[ ( cut , var1 , var2 ) ]
                        if SumYields == None:
                            SumYields = hYield.Clone("SumYields")
                        else:
                            SumYields.Add( hYield )
                        if SumYieldsR == None:
                            SumYieldsR = hYieldR.Clone("SumYieldsR")
                        else:
                            SumYieldsR.Add( hYieldR )

                    c = ROOT.TCanvas( "EffPurity_%s_%s" % (var1, var2) )
                    c.Divide( 4 , len( self.SampleFiles )  )
                    index = 1

                    for sample in self.Samples :
                        ec = self.SampleFiles[sample][-1]
                        hEff, hYield , hEffR, hYieldR = ec.AllEffs[ ( cut , var1 , var2 ) ]
                        c.cd(index)
                        hEff.SetTitle("%s efficiency" % (sample))
                        hEff.Draw("COLZ")

                        index += 1
                        c.cd( index )
                        hYield.Divide( SumYields )
                        hYield.SetTitle( "%s purity" % (sample) )
                        hYield.Draw("COLZ")

                        index += 1
                        c.cd(index)
                        hEffR.SetTitle("%s efficiency (R)" % (sample))
                        hEffR.Draw("COLZ")

                        index += 1
                        c.cd( index )
                        hYieldR.Divide( SumYieldsR )
                        hYieldR.SetTitle( "%s purity (R)" % (sample) )
                        hYieldR.Draw("COLZ")
                        index += 1

                    cutDir.cd()
                    c.Write()

    def Close(self):
        self.fOut.Close()
        for sample in self.SampleFiles:
            self.SampleFiles[sample][2].Close()

    def CalcEffsAndPurities(self):
        hSum = {}
        hPurities = {}
        for sample in self.Samples :
            ec = self.SampleFiles[sample][-1]
            ec.CalcAllEffs()

            for bin in self.Cuts :
                if bin in hSum.keys() :
                    hSum[bin].Add( ec.Results[bin]["yield"].hCtCv )
                else :
                    hSum[bin] = ec.Results[bin]["yield"].hCtCv.Clone("SumAllSignalsIn_%s" % (bin) )
        for sample in self.Samples :
            ec = self.SampleFiles[sample][-1]
            ec.CalcPurities( hSum )
        
        
allEffs = AllEfficiencies({"Preselection":"1==1" ,
                           "THQLeptonicTHQTag":"(n_jets == 2 && n_L_bjets == 1 && ( fwdjet1_eta > 2.5 || fwdjet1_eta < -2.5 ))",
                           "THQLeptonicTTHTag":"( (n_jets > 2 &&  abs(fwdjet1_eta)>2.5) || (abs(fwdjet1_eta)<=2.5) )",
                           "MVATHQ":  "MVA_Medium > 0" ,
                           "MVATTH":  "MVA_Medium <= 0",
                           "EtaNJetTTHTag":"!(n_jets == 2 && ( abs(fwdjet1_eta) >= 2.5 ) )",
                           "EtaNJetTHQTag":"(n_jets == 2 && ( abs(fwdjet1_eta) >= 2.5 ) )",
                           "EtaNbJetTTHTag":"!(n_L_bjets == 1 && ( abs(fwdjet1_eta) >= 2.5 ) )",
                           "EtaNbJetTHQTag":"(n_L_bjets == 1 && ( abs(fwdjet1_eta) >= 2.5 ) )",
                           "NJetNbJetTTHTag":"!(n_L_bjets == 1 && n_jets == 2)",
                           "NJetNbJetTHQTag":"(n_L_bjets == 1 && n_jets == 2 )"})
#allEffs.MakePlots()
allEffs.CalcEffsAndPurities()
allEffs.Close()

