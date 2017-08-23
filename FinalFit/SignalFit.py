from ROOT import RooWorkspace, RooDataSet, RooPlot, RooRealVar, RooFit, RooExtendPdf, RooAbsPdf, RooFitResult, RooFormulaVar , RooGaussian, RooArgList, RooAddPdf, RooConstVar , RooArgSet ,  Roo2DMomentMorphFunction, RooDataHist, RooHistFunc
from ROOT import TFile, gSystem, TH1D, TCanvas,  kRed, kGreen, kBlack , TMath , TLegend, TGraphErrors, kBlue, kGray, TMatrixD, TH2D, gROOT, TPaveText
import re
import sys
from math import sqrt
from array import array
import numpy as np

AllSystParams = []
LUMI = 35.9

class KappaFramework:
    def __init__(self):
        self.BR_CoeffsVals= {"kb":0.57 , "kw":0.22  , "kg":0.09 , "ktau":0.06 , "kz":0.03 , "kc":0.03 , "kzg":0.0016 , "ks":0.0001 , "kmu":0.00022 }
        self.BR_Coeffs_List = []
        self.BR_Coeffs = RooArgList()
        for br_coeff in self.BR_CoeffsVals:
            coeff = RooConstVar( "kappa_br_coeff_%s" % (br_coeff) , br_coeff , self.BR_CoeffsVals[br_coeff] )
            self.BR_Coeffs_List.append( coeff )
            self.BR_Coeffs.add( coeff )

        self.CV = RooRealVar("CV" , "CV" , 1 , 0.5 , 2 )
        self.CtOverCv = RooRealVar( "CtOverCv", "Ct/Cv" , -1 , -8 , 8 )
        self.CArgs = RooArgList( self.CtOverCv, self.CV)
        self.CT = RooFormulaVar("CT" ,  "@0*@1" , self.CArgs )
        
        self.KGamma2 = RooFormulaVar( "KGamma2" , "KGamma2" , "1.59*@0*@0+0.07*@1*@1-0.66*@0*@1" , RooArgList(  self.CV , self.CT ) )
        self.TotalWidth = RooFormulaVar("TotalWidth" , "TotalWidth" , "0.57+0.22*@0*@0+0.09+0.06+0.03+0.03+0.0016+0.0001+0.00022+0.0023*@1" , RooArgList( self.CV , self.KGamma2 ) )

        self.BRGammaGamma = RooFormulaVar("BRGammaGamma" , "H -> #gamma #gamma " , "@0/@1" , RooArgList( self.KGamma2 , self.TotalWidth ) )

        self.tHqXSection = RooFormulaVar( "tHqXSection" , "tHqXSection" , "2.633*@0*@0+3.578*@1*@1-5.211*@0*@1" , RooArgList( self.CT , self.CV ) )
        self.tHWXSection = RooFormulaVar( "tHWXSection" , "tHWXSection" , "2.909*@0*@0+2.31*@1*@1-4.22*@0*@1" , RooArgList( self.CT , self.CV ) )

        self.tHqXSectionTimesBR = RooFormulaVar( "tHqXSectionTimesBR" , "tHqXSectionTimesBR" , "@0*@1" , RooArgList( self.tHqXSection , self.BRGammaGamma ) )
        self.tHWXSectionTimesBR = RooFormulaVar( "tHWXSectionTimesBR" , "tHWXSectionTimesBR" , "@0*@1" , RooArgList( self.tHWXSection , self.BRGammaGamma ) )

        self.SMtHqXSec = RooRealVar("SMtHqXSec" , "SMtHqXSec" , 0.07425 )
        self.SMtHWXSec = RooRealVar("SMtHWXSec" , "SMtHWXSec" , 0.01517 )
        self.SMHggBR   = RooRealVar("SMHggBR"   , "SMHggBR"   , 0.00227 )
        self.SMttHXSec = RooRealVar("SMttHXSec" , "SMttHXSec" , 0.5071 )
        self.SMvHXSec = RooRealVar("SMvHXSec" , "SMvHXSec"   , 2.2569 )
        
        self.LUMI = RooRealVar("Luminosity" , "Luminosity" , LUMI)

        self.BRGammaGammaValue = RooFormulaVar( "BRGammaGammaValue" , "BRGammaGammaValue" , "@0*@1" , RooArgList(self.BRGammaGamma , self.SMHggBR) )
        self.tHqXSecValue = RooFormulaVar( "tHqXSecValue" , "tHqXSecValue" , "@0*@1" , RooArgList(self.SMtHqXSec , self.tHqXSection ) )
        self.tHWXSecValue = RooFormulaVar( "tHWXSecValue" , "tHWXSecValue" , "@0*@1" , RooArgList(self.SMtHWXSec , self.tHWXSection ) )
        self.ttHXSecValue = RooFormulaVar( "ttHXSecValue" , "ttHXSecValue" , "@0*@0*@1" , RooArgList(self.CT , self.SMttHXSec ) )
        self.vHXSecValue = RooFormulaVar( "vHXSecValue" , "vHXSecValue" , "@0*@0*@1" , RooArgList(self.CV , self.SMvHXSec ) )
        
        self.SumXSections = RooFormulaVar( "SumXSections" , "SumXSections" , "@0*(@1+@2+@3+@4)" , RooArgList( self.BRGammaGammaValue , self.tHqXSecValue , self.tHWXSecValue , self.ttHXSecValue , self.vHXSecValue )  )
        
    def SetCtCv(self, ct, cv ):
        self.CV.setVal( cv )
        if cv == 0 :
            print ct,cv
            cv = 0.0001
        self.CtOverCv.setVal( ct/cv )

    def Print(self):
        print "CT : " , self.CT.getVal()
        print "CV : " , self.CV.getVal()
        print "KGamma2 : " , self.KGamma2.getVal()
        print "TotalWidth : " , self.TotalWidth.getVal()
        print "BRGammaGamma : " , self.BRGammaGamma.getVal()
        print "tHqXSection : " , self.tHqXSection.getVal()
        print "tHwXSection : " , self.tHWXSection.getVal()

    def GetThqGGXSecBR(self, ct , cv ):
        self.SetCtCv( ct , cv )
        return self.tHqXSectionTimesBR.getVal()

    def GetThWGGXSecBR(self, ct , cv ):
        self.SetCtCv( ct , cv )
        return self.tHWXSectionTimesBR.getVal()

    def GetXSecBR(self, process , ct , cv , ratio = True ):
        if "thq" in process:
            sm = 1 if ratio else (self.SMtHqXSec.getVal()*self.SMHggBR.getVal())
            return self.GetThqGGXSecBR( ct , cv )*sm
        elif "thw" in process:
            sm = 1 if ratio else (self.SMtHWXSec.getVal()*self.SMHggBR.getVal())
            return self.GetThWGGXSecBR( ct , cv )*sm
        elif "tth" in process:
            sm = 1 if ratio else ( self.SMHggBR.getVal()*self.SMttHXSec.getVal() )
            self.SetCtCv( ct, cv )
            return ct*ct*self.BRGammaGamma.getVal()*sm
        elif "vh" in process :
            sm = 1 if ratio else (self.SMHggBR.getVal()*self.SMvHXSec.getVal() )
            self.SetCtCv( ct, cv )
            return cv*cv*self.BRGammaGamma.getVal()*sm
        elif "vbf" in process or "ggh" in process :
            sm = 1 if ratio else self.SMHggBR.getVal()
            self.SetCtCv( ct, cv )
            return self.BRGammaGamma.getVal()*sm
        else :
            print "GetXSecBR : Error in the process name"
            return 1.0
    
    def PlotIt(self):
        self.FrameCV = self.CV.frame( RooFit.Title("CV") , RooFit.Name("CVPlot") )
        self.TotalWidth.plotOn(self.FrameCV , RooFit.LineColor( kBlack) )
        self.KGamma2.plotOn( self.FrameCV , RooFit.LineColor( kGray ) )
        self.BRGammaGamma.plotOn(self.FrameCV , RooFit.LineColor( kRed ) )
        self.tHqXSectionTimesBR.plotOn(self.FrameCV , RooFit.LineColor( kGreen ) )
        self.tHWXSectionTimesBR.plotOn(self.FrameCV , RooFit.LineColor( kBlue ) )

        self.FrameCT = self.CT.frame( RooFit.Title("CT") , RooFit.Name("CTPlot") )
        self.TotalWidth.plotOn(self.FrameCT , RooFit.LineColor( kBlack) )
        self.KGamma2.plotOn( self.FrameCT , RooFit.LineColor( kGray ) )
        self.BRGammaGamma.plotOn(self.FrameCT , RooFit.LineColor( kRed ) )
        self.tHqXSectionTimesBR.plotOn(self.FrameCT , RooFit.LineColor( kGreen ) )
        self.tHWXSectionTimesBR.plotOn(self.FrameCT , RooFit.LineColor( kBlue ) )

        self.Canvas = TCanvas("test" , "test")
        self.Canvas.Divide(1,2)
        self.Canvas.cd(1)
        self.FrameCT.Draw()

        self.Canvas.cd(2)
        self.FrameCV.Draw()

    def Write(self, ws ):
        getattr( ws , "import")( self.tHWXSectionTimesBR , RooFit.RecycleConflictNodes() )
        getattr( ws , "import")( self.tHqXSectionTimesBR , RooFit.RecycleConflictNodes() )
        getattr( ws , "import")( self.SumXSections , RooFit.RecycleConflictNodes() )

class CtCvCpInfo :
    def Print(self):
        print self.Name
        for i in range(0 , len( self.AllCtCVs ) ):
            print i, self.AllCtCVs[i]
        
    def __init__(self , name):
        self.Name = name
        
        self.Kvs = [1.0 , 1.5 , 0.5]
        # self.KvKfs = {
        #     1.0:[3. , 2. , 1.5 , 1.25 ,  1.0, .75 , .5 , .25 , 0.0 , -0.25 , -0.5 , -0.75     , -1.25 , -1.5 , -2. , -3. ],
        #     1.5:[3. , 2. , 1.5 , 1.25 ,  1.0, .75 , .5 , .25 , 0.0 , -0.25 , -0.5 , -0.75 ,-1 , -1.25 , -1.5 , -2. , -3. ],
        #     .5:[3. , 2. , 1.5 , 1.25 ,  1.0, .75 , .5 , .25 , 0.0 , -0.25 , -0.5 , -0.75 ,-1 , -1.25 , -1.5 , -2. , -3. ]
        # }
        self.KvKfs = {
            1.0:[ -3. , -2. , -1.5 , -1.25        , -.75 , -.5 , -.25 , 0.000 , 0.25 , 0.5 , 0.75 ,1    , 1.25 , 1.5 , 2. , 3. ],
            1.5:[ -3. , -2. , -1.5 , -1.25 ,  -1.0, -.75 , -.5 , -.25 , 0.000 , 0.25 , 0.5 , 0.75 ,1, 1.25 , 1.5 , 2. , 3. ],
            0.5:[ -3. , -2. , -1.5 , -1.25 ,  -1.0, -.75 , -.5 , -.25 , 0.000 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ]
        }

        self.AllCtCVs = []
        for Kv in self.Kvs:
            for Kf in self.KvKfs[Kv]:
                self.AllCtCVs.append( (Kv, Kf) )

        self.AllCtOverCVs = {}
        for Kv in self.Kvs:
            for Kf in self.KvKfs[Kv]:
                r = Kf/Kv
                if r in self.AllCtOverCVs.keys() :
                    self.AllCtOverCVs[r][Kv] = 0.0
                else :
                    self.AllCtOverCVs[r] = {Kv:0.0}
                
        self.AllCpVals = [ l/10. for l in range(-9 , 10 ) ]

        self.CvVar = RooRealVar("CV" , "CV" , 1 , 0.5 , 2 )
        self.CtOverCv = RooRealVar( "CtOverCv", "Ct/Cv" , -1 , -8 , 8 )
        self.CArgs = RooArgList( self.CtOverCv, self.CvVar)
        self.CtVar = RooFormulaVar("CT" ,  "@0*@1" , self.CArgs )
        
        self.CpVar = RooRealVar("CP" , "CP" , 0 , -1 , 1 )

        self.CtBins = array( 'd' ,  [-3. , -2. , -1.5 , -1.25 , -1.0 , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1.0 , 1.25 , 1.5 , 2. , 3. , 4. ] )

        self.hCtCv = TH2D( "h%s_CtCv" % (name) , "CtCv " + name , 3 , 0.5 , 2.0 , len(self.CtBins)-1 , self.CtBins )
        self.hCp = TH1D("h%s_Cp" % (name)  , "Cp " + name , 19 , -.9 , 1 )

        self.ValuesCtCv = {}
        self.ValuesCp = {}
        self.mCtCv = TMatrixD( 95 , 3 )        
        

    def GetCanvas( self ):
        if not hasattr( self , "Canvas" ):
            self.Canvas = TCanvas( "Canvas_" + self.Name )
            self.Canvas.Divide( 2 , 1 )
            self.Canvas.cd(1)
            self.hCtCv.Draw("COLZ TEXT")
            self.Canvas.cd(2)
            self.GetCtOverCv().Draw("AP")
        return self.Canvas
        
    def GetCValues(self, weight_id):
        Ct = 0
        Cv = 0
        Cp = -2

        if weight_id == -1 :
            Ct = -1
            Cv =  1
        elif weight_id < 50 :
            Ct = self.AllCtCVs[ weight_id ][1]
            Cv = self.AllCtCVs[ weight_id ][0]
        elif weight_id < 69 :
            cpbin = weight_id-50
            Cp = self.AllCpVals[cpbin]
        else :
            Cp = -3

        return Ct,Cv,Cp
    
    def GetValue(self, weight_id):
        Ct, Cv, Cp = self.GetCValues(weight_id)
        if Cp == -2 :
            return self.ValuesCtCv[(Ct,Cv)]
        elif Cp == -3 :
            return -100
        else :
            return self.ValuesCp[ Cp ]
    
    def SetValue(self, weight_id , value):
        Ct, Cv, Cp = self.GetCValues(weight_id)
        if weight_id == -1:
            weight_id = 50
            
        if Cp == -2 :
            self.AllCtOverCVs[ Ct/Cv ][Cv] = value
            self.ValuesCtCv[( Ct , Cv ) ] = value
            self.hCtCv.SetBinContent( self.hCtCv.FindBin( Cv, Ct ) , value )
            #self.mCtCv[ weight_id ][ 0 ] = Cv
            #self.mCtCv[ weight_id ][ 1 ] = Ct
            #self.mCtCv[ weight_id ][ 2 ] = value
        elif Cp > -2 :
            self.ValuesCp[ Cp ] = value
            self.hCp.SetBinContent( self.hCp.FindBin( Cp +0.001)  , value )
        else :
            print weight_id, "is not set"
            
    def FillFrom1DHisto(self, fname, hname ):
        file_ = TFile.Open(fname)
        gROOT.cd()
        self.Histo = file_.Get(hname).Clone("hAll_%s" % self.Name)
        file_.Close()

        nTotal_Orig = self.Histo.GetBinContent( 2 )
        Bin = 2
        self.SetValue( -1 , nTotal_Orig )


        for b in range(3 , self.Histo.GetNbinsX()+1 ):
            self.SetValue( b-3 , self.Histo.GetBinContent( b ) ) #/nTotal_Orig 

    def FillFrom2DHisto(self , h2 ):
        self.SetValue( -1 , h2.GetBinContent( h2.FindBin( 1.+0.0001 , -1.+0.0001 ) ) )
        for Kv in self.Kvs:
            for Kf in self.KvKfs[Kv]:
                value = h2.GetBinContent( h2.FindBin( Kv+0.001 , Kf+0.001 ) )
                index = self.AllCtCVs.index( (Kv, Kf) )
                self.SetValue( index , value )

    def Make2dMomentMorphFunction(self):
        #print self.Name, self.ValuesCtCv
        
        bin = 51
        for cv in [0 , 2 ]:
            near_cv = 0.5 if cv==0 else 1.5
            for ct in self.KvKfs[.5] :
                self.mCtCv[ bin ][0] = cv
                self.mCtCv[ bin ][1] = ct
                self.mCtCv[ bin ][2] = self.ValuesCtCv[ (ct , near_cv ) ]
                bin += 1
        for ct in [-4 , 4]:
            near_ct = -3. if ct == -4 else 3.
            for cv in [0.5,1.,1.5]:
                self.mCtCv[bin][0] = cv
                self.mCtCv[bin][1] = ct
                self.mCtCv[bin][2] = self.ValuesCtCv[ (near_ct , cv ) ]
                bin += 1
            for cv in [0,2]:
                near_cv = 0.5 if cv==0 else 1.5
                self.mCtCv[bin][0] = cv
                self.mCtCv[bin][1] = ct
                self.mCtCv[bin][2] = self.ValuesCtCv[ (near_ct , near_cv ) ]
                bin += 1

        self.FuncCtCv = Roo2DMomentMorphFunction( "FuncCtCv_%s" % (self.Name) , "FuncCtCv" , self.CvVar , self.CtVar , self.mCtCv )
        self.FuncCtCv.setMode( Roo2DMomentMorphFunction.Linear ) #LinearPosFractions

        return self.FuncCtCv

    def Validate1(self):
        self.FuncCtCv.Summary()
        self.hCtCv2 = TH2D( "hCtCvTemp" , "hCtCvTemp" , 3 , 0.5 , 2.0 , len(self.CtBins)-1 , self.CtBins )
        self.Comp = {}
        for CvValue in self.Kvs :
            self.CvVar.setVal( CvValue )
            kfs = self.KvKfs[CvValue]
            if CvValue == 1.0:
                kfs.append( -1 )
            for CtValue in kfs:
                self.CtVar.setVal( CtValue )

                val =  self.FuncCtCv.getVal(RooArgSet(self.CvVar , self.CtVar) ) #self.ValuesCtCv[ (CtValue , CvValue) ]
                self.hCtCv2.Fill( CvValue , CtValue , val )
                self.Comp[ (CtValue , CvValue) ] = val #(self.ValuesCtCv[ (CtValue , CvValue) ]-val)/val
                print CtValue, CvValue, val, self.ValuesCtCv[ (CtValue , CvValue) ]

        self.hCom = self.hCtCv2.Clone("hCompare")
        self.hCom.Add( self.hCtCv , -1 )
        self.hCom.Divide( self.hCtCv )
    
    def GetCtOverCv(self , color = kRed , style = 20 , dx = 0.0 , cv = -1 , IgnoreNegatives = False):
        if hasattr( self , "CtOverCvGraph"):
            return self.CtOverCvGraph
        
        ctOcvs = sorted(self.AllCtOverCVs.keys())

        x = array( 'd' )
        y = array( 'd' )
        ex = array( 'd' )
        ey = array( 'd' )
        
        for ctOcv in ctOcvs :
            vals = sorted([ self.AllCtOverCVs[ctOcv][kv] for kv in self.AllCtOverCVs[ctOcv] ])
            if IgnoreNegatives :
                vals_ = []
                for v in vals:
                    if v > 0. :
                        vals_.append( v )
                vals = vals_
                if len( vals ) == 0 :
                    continue
            # print ctOcv,self.AllCtOverCVs[ctOcv].keys()
            # if 0.5 in self.AllCtOverCVs[ctOcv].keys() :
            #     vals = [ self.AllCtOverCVs[ctOcv][0.5] ]
            # else :
            #     vals = [ self.AllCtOverCVs[ctOcv][self.AllCtOverCVs[ctOcv].keys()[0]] ]
            # vals = [ vals[0] ]
            # if len(vals) == 3 :
            #     if abs(vals[2]-vals[1])/vals[1] > 0.02 :
            #         print ctOcv, self.AllCtOverCVs[ctOcv]
            #         vals = [ vals[0] , vals[1] ]
            #     if abs(vals[0]-vals[1])/vals[1] > 0.02 :
            #         print ctOcv, self.AllCtOverCVs[ctOcv]
            #         vals = vals[1:]

            # if len(vals)==2 :
            #     if abs(vals[0]-vals[1])/vals[0] > 0.02 :
            #         print ctOcv, self.AllCtOverCVs[ctOcv]
            #         vals = [ (vals[0]+vals[1])/2 ]
            avg = 0
            for val in vals:
                avg += val
            avg /= len(vals)
            std = 0
            for val in vals :
                std += (val - avg)**2
            std /= len(vals)
            std = sqrt( std )
            
            x.append( ctOcv + dx )
            y.append( avg   )
            ex.append( 0 )
            ey.append( std )

            
        self.CtOverCvGraph = TGraphErrors( len(x) , x , y , ex , ey )
        self.CtOverCvGraph.SetName( "CtOverCvGraph_" + self.Name )
        self.CtOverCvGraph.SetTitle( self.Name )

        self.CtOverCvGraph.SetLineColor( color )        
        self.CtOverCvGraph.SetMarkerStyle(style)
        self.CtOverCvGraph.SetMarkerColor( color )

        x.append( x[-1]+0.5 )
        self.CtOverCvHisto = TH1D( "CtOverCvHistoBasic_" + self.Name  , self.Name , len(x)-1 , x )
        for b in range( 0, len(x)-1 ):
            self.CtOverCvHisto.SetBinContent( b+1 , y[b]  )
            self.CtOverCvHisto.SetBinError(   b+1 , ey[b] )
        #self.CtOverCvHisto.Print("ALL")
        #print x

        self.ArgListCtOverCv = RooArgList(self.CtOverCv)
        self.ArgSetCtOverCv = RooArgSet(self.CtOverCv)
        self.CtOverCvDataHist = RooDataHist("CtOverCvDataHist_" + self.Name  , self.Name , self.ArgListCtOverCv , self.CtOverCvHisto)
        self.CtOverCvDataHistFunc = RooHistFunc("CtOverCvDataHistFunc_" + self.Name  , self.Name , self.ArgSetCtOverCv , self.CtOverCvDataHist )
        
        return self.CtOverCvGraph
            
    def Write(self, ws ):
        if not hasattr( self, "FuncCtCv" ):
            self.Make2dMomentMorphFunction()
        if not hasattr( self, "CtOverCvDataHistFunc" ):
            self.GetCtOverCv()
            
        getattr( ws , "import")( self.FuncCtCv , RooFit.RecycleConflictNodes() )
        getattr( ws , "import")( self.CtOverCvDataHistFunc , RooFit.RecycleConflictNodes() )
        

class Variable2D:
    def GetCanvas( self ):
        return self.Central.GetCanvas()

    def Draw(self):
        return self.Central.GetCanvas()
    
    def __init__(self, name   ,title = None):
        self.Name = name
        self.Central = CtCvCpInfo( self.Name + "_Central")
        self.Stat = CtCvCpInfo( self.Name + "_StatUncert")
        self.Systs = {}
        self.Title = title if title else name

    def SetValue(self, weight_id, value , stat):
        if weight_id == -1 :
            self.ReferenceValue = value
            self.ReferenceError = stat if stat != 0 else 0.01*value
            self.ReferenceUncert = self.ReferenceError/value
            
        self.Central.SetValue( weight_id , value )
        self.Stat.SetValue( weight_id , stat )

        #if weight_id == -1 :
        #    self.SetSyst( "STAT" , None , value+stat , value-stat )
            
    def SetSyst(self , systname , nuisancename , valueup, valuedown ):    
        central = self.ReferenceValue
        up = abs(valueup-central)/central
        down = abs(valuedown-central)/central
        Max = max(up , down )
        if Max > 0.01 : #(self.ReferenceUncert/2) :
            self.Systs[systname] = {}
            self.Systs[systname]["value"] = CtCvCpInfo( self.Name + "_value_" + systname)
            self.Systs[systname]["nuisancename"] = nuisancename
            for weight_id in range(-1 , 50):
                self.Systs[systname]["value"].SetValue( weight_id , Max )
            self.Systs[systname]["val"] = Max
            
    def Write(self, ws):
        self.Central.Write(ws)
        self.Stat.Write(ws)
        for syst in self.Systs:
            self.Systs[syst]["value"].Write(ws)

    def MakeVariable( self, finalname = None , lowerlimit = -99999. , cv = -1 ):
        formulaText = "(@0)*(1"
        self.Central.GetCtOverCv()
        self.ListOfVarsRatio = RooArgList( self.Central.CtOverCvDataHistFunc )

        varindex = 1
        for syst in self.Systs :
            if self.Systs[syst]["nuisancename"] :
                self.Systs[syst]["nuisance"] = RooRealVar( self.Systs[syst]["nuisancename"] , self.Title , 0 , -10 , 10 )
            else:
                self.Systs[syst]["nuisance"] = RooRealVar( "nuisance_" + self.Name + "_" + syst , self.Title , 0 , -10 , 10 )
            
            self.ListOfVarsRatio.add( self.Systs[syst]["nuisance"] )
            #self.ListOfVars.add( self.Systs[syst]["value"].Make2dMomentMorphFunction() )
            formulaText += "+%.3f*@%d"%( self.Systs[syst]["val"] , varindex )
            varindex += 1
            if not self.Systs[syst]["nuisance"].GetName() in AllSystParams :
                AllSystParams.append(self.Systs[syst]["nuisance"].GetName())
        formulaText += ")"

        name = finalname if finalname else "formulaCtOverCv_" + self.Name
        self.FormulaRatio = RooFormulaVar( name , self.Title , formulaText , self.ListOfVarsRatio )
        return self.FormulaRatio
        
    
    def MakeVariable2D(self,finalname = None , lowerlimit = -99999.):
        formulaText = "(@0)*(1"
        varindex = 1
        self.ListOfVars = RooArgList(self.Central.Make2dMomentMorphFunction())
        for syst in self.Systs :
            if self.Systs[syst]["nuisancename"] :
                self.Systs[syst]["nuisance"] = RooRealVar( self.Systs[syst]["nuisancename"] , self.Title , 0 , -1 , 1 )
            else:
                self.Systs[syst]["nuisance"] = RooRealVar( "nuisance_" + self.Name + "_" + syst , self.Title , 0 , -1 , 1 )
            
            self.ListOfVars.add( self.Systs[syst]["nuisance"] )
            self.ListOfVars.add( self.Systs[syst]["value"].Make2dMomentMorphFunction() )
            formulaText += "+@%d@%d"%(varindex , varindex+1)
            varindex += 2
            if not self.Systs[syst]["nuisance"].GetName() in AllSystParams :
                AllSystParams.append(self.Systs[syst]["nuisance"].GetName())
        formulaText += ")"

        name = finalname if finalname else "formula_" + self.Name
        self.Formula = RooFormulaVar( name , self.Title , formulaText , self.ListOfVars )
        return self.Formula


        
    
class Uncertainty:
    def __init__(self, name , valueUp , central ,  valueDown , Type , nuisancename = None , title = None):
        self.Name = name
        self.Value = max( abs(valueUp-central) , abs(valueDown-central) )/central
        if self.Value < 0.01:
            self.Value = 0
        self.Type = Type
        self.Title = title if title else name
        self.NuisanceName = nuisancename

        self.Central = central
        self.ValUp = valueUp
        self.ValDown = valueDown

    def getUncert2(self):
        val = self.Value*self.Central
        return val*val
        
    def MakeUncert(self):
        if self.Value == 0:
            return None
        
        self.ConstVar = RooConstVar( "const_" + self.Name , self.Title , self.Value )
        if self.NuisanceName :
            self.Var = RooRealVar( self.NuisanceName , self.Title , 0 , -1 , 1 )
        else:
            self.Var = RooRealVar( "nuisance_" + self.Name , self.Title , 0 , -1 , 1 )
        self.ListOfVars = RooArgList( self.ConstVar , self.Var )
        self.Formula = RooFormulaVar("formula_" + self.Name , self.Title , "@0*@1" , self.ListOfVars )

        return self.Formula
        
class Variable:
    def __init__( self, name , value , statuncert , systuncert , title = None ):
        self.Name = name
        self.Value = value
        self.Systs = systuncert
        self.Stat = statuncert
        self.Title = title if title else name


    def MakeSimpleVariable(self , finalname , lowerlimit = -99999. ):
        totaluncert = self.Stat*self.Stat
        for syst in self.Systs :
            totaluncert+= syst.getUncert2()

        totaluncert = sqrt( totaluncert )
        min_ = self.Value - totaluncert
        lowerlimit = self.Value*lowerlimit
        self.SimpleVar = RooConstVar( finalname , self.Title , self.Value ) # , lowerlimit if min_ < lowerlimit else min_  , self.Value+totaluncert)
        return self.SimpleVar
    
    def MakeVariable(self , finalname = None , lowerlimit = -99999.):
        if self.Stat == 0:
            self.Var = RooConstVar( self.Name , self.Title , self.Value )
        else:
            min_ = self.Value-self.Stat
            self.Var = RooRealVar( self.Name , self.Title , self.Value ) # , lowerlimit if min_ < lowerlimit else min_  , self.Value+self.Stat )

        formulaText = "(@0)*(1"
        varindex = 1
        self.ListOfVars = RooArgList(self.Var)
        for syst in self.Systs :
            var = syst.MakeUncert()
            if var :
                self.ListOfVars.add( var )
                formulaText += "+@%d"%(varindex)
                varindex += 1
                if not syst.NuisanceName in AllSystParams :
                    AllSystParams.append(syst.NuisanceName)
        formulaText += ")"

        name = finalname if finalname else "formula_" + self.Name
        self.Formula = RooFormulaVar( name , self.Title , formulaText , self.ListOfVars )
        return self.Formula

    def Draw(self):
        nPoints = len( self.Systs )
        param = self.Name
        cname = "Canvas_" + param
        c = TCanvas( cname , cname )
        self.Canvas = c
        #setattr( self , cname , c )

        gname = "GraphSyst_" + param
        self.gSystem = TGraphErrors( nPoints )
        self.gSystem.SetName( gname )
        self.gSystem.SetTitle( param )

        gname = "GraphCentral_" + param
        self.gCentral = TGraphErrors( nPoints )
        self.gCentral.SetName( gname )
        self.gCentral.SetTitle( param )

        centralval = self.Value
        #centralErr = self.Central.FitParams[param].getAsymErrorHi()
        centralErr = self.Stat
        counter = 0
        labels = []
        for syst in self.Systs :
            systUp = syst.ValUp
            systLo = syst.ValDown
            mean = (systUp+systLo)/2.0
            err = abs( systUp - systLo ) /2.0
            self.gSystem.SetPoint( counter , counter , mean )
            self.gSystem.SetPointError( counter , 0.5 , err )

            self.gCentral.SetPoint( counter , counter , centralval )
            self.gCentral.SetPointError( counter , 0.5 , centralErr )
            systName = syst.Name.replace( param , "")
            labels.append( systName )
            counter += 1

        c.cd()
        self.gCentral.SetFillColor( kGreen )
        self.gCentral.SetFillStyle( 3005 )
        self.gCentral.Draw("A3*")
        xax = self.gCentral.GetHistogram().GetXaxis()
        minXax = xax.GetBinLowEdge(1)
        maxXax = xax.GetBinUpEdge( xax.GetNbins() )
        xax.Set( len(labels) , minXax , maxXax )
        i = 1
        for lbl in labels:
            xax.SetBinLabel(i, lbl)
            i+=1

        self.gSystem.SetLineWidth( 2 )
        self.gSystem.Draw("P")
        return self.Canvas
    
class nGaussians :
    def MakeName(self, var = "" , rank = -1 ):
        Name = ""
        if not var :
            Name = "%s_mh%d" % (self.Name,self.mh )
        elif rank == -1:
            Name = "%s_%s_mh%d" % (self.Name, var,self.mh )
        else:
            Name = "%s_%s_mh%d_g%d" % (self.Name, var,self.mh,rank )
        VarName = "%s%s"%(Name, "_"+self.SystName if self.SystName else "" )
        return Name, VarName

    def GetParam(self, names , value , from_ , to ):
        if self.Params and names[0] in self.Params :
            return self.Params[ names[0] ].MakeVariable()

        if from_ == to :
            return RooRealVar( names[1] , names[1] , value )
        else :
            return RooRealVar( names[1] , names[1] , value , from_ , to )
        
    def __init__( self, n , name , massVar, systname = "" , mh = 125 , params = None ):
        self.N = n
        self.Name = name
        self.SystName = systname
        self.MH = RooRealVar( "MH" , "MH" , mh )
        self.mh = mh
        self.mass = massVar

        self.Params = params
        
        self.FitParams = {}
        self.FitUtils = {}
        self.Gaussians = {}

        self.gaussians = RooArgList()
        self.coeffs = RooArgList()
        
        for g in range(0,n):
            dmRangeP = 2.*(g+2) if g != (n-1) else 0
            dmRangeN = -2.*(g+2) if g != (n-1) else -25.*(g+2)
            dmCentral = 0 #if g != (n-1) else -900
            if "tth" in self.Name :
                if g == 0 :
                    dmRangeN , dmRangeP , dmCentral = -0.5 , 0.5 , 0
                elif g == 1 :
                    dmRangeN , dmRangeP , dmCentral = -4. , 0 , -2.5
                elif g == 2 :
                    dmRangeN , dmRangeP , dmCentral = -15 , 0 , -10
            elif "thq" in self.Name :
                if g == 0 :
                    dmRangeN , dmRangeP , dmCentral = -0.5 , 0.2 , -0.2
                elif g == 1 :
                    dmRangeN , dmRangeP , dmCentral = -5 , -1.5 , -2
                elif g == 2 :
                    dmRangeN , dmRangeP , dmCentral = -105 , -95 , -100
            elif "thw" in self.Name :
                if g == 0 :
                    dmRangeN , dmRangeP , dmCentral = -0.5 , 0.2 , -0.2
                elif g == 1 :
                    dmRangeN , dmRangeP , dmCentral = -5 , -1.5 , -2
                elif g == 2 :
                    dmRangeN , dmRangeP , dmCentral = -105 , -95 , -100
            elif "thw2" in self.Name :
                if g == 0 :
                    dmRangeN , dmRangeP , dmCentral = -.17 , -.17 , -.17 
                elif g == 1 :
                    dmRangeN , dmRangeP , dmCentral = -3 , -3 , -3
                elif g == 2 :
                    dmRangeN , dmRangeP , dmCentral = -100 , -100 , -100
            dmNames = self.MakeName( "dm" , g )
            dm = self.GetParam( dmNames ,dmCentral,dmRangeN,dmRangeP)
                        
            meanNames = self.MakeName( "mean" , g )
            mean = RooFormulaVar( meanNames[1] , meanNames[1] ,"@0+@1",RooArgList(self.MH,dm))

            sigmaNames = self.MakeName( "sigma" , g )
            #max_sigma = 3*(g+1) if g != (n-1) else 10*(g+1)
            #min_sigma = 0.5*(g+1) if g != (n-1) else 3*(g+1)
            #sigma_central = 1.*(g+1) if g != (n-1) else 20
            if "tth" in self.Name :
                if g == 0 :
                    max_sigma , min_sigma , sigma_central = 2 , 1 , 1.5
                elif g == 1 :
                    max_sigma , min_sigma , sigma_central = 2 , 1 , 1.5
                elif g == 2 :
                    max_sigma , min_sigma , sigma_central = 25 , 15 , 20
            elif "thq" in self.Name :
                if g == 0 :
                    max_sigma , min_sigma , sigma_central = 1.6 , 0.6 , 1.2
                elif g == 1 :
                    max_sigma , min_sigma , sigma_central = 2 , 0.8 , 1.6
                elif g == 2 :
                    max_sigma , min_sigma , sigma_central = 50 , 25 , 35
            elif "thw" in self.Name :
                if g == 0 :
                    max_sigma , min_sigma , sigma_central = 1.6 , 0.6 , 1.2
                elif g == 1 :
                    max_sigma , min_sigma , sigma_central = 2 , 0.8 , 1.6
                elif g == 2 :
                    max_sigma , min_sigma , sigma_central = 50 , 25 , 35
            elif "thw2" in self.Name :
                if g == 0 :
                    max_sigma , min_sigma , sigma_central = 1.43, 1.43 , 1.43
                elif g == 1 :
                    max_sigma , min_sigma , sigma_central = 1.6 , 1.6 , 1.6
                elif g == 2 :
                    max_sigma , min_sigma , sigma_central = 30 , 30 , 30
                    
            sigma = self.GetParam( sigmaNames,sigma_central ,min_sigma, max_sigma )
                
            gausNames = self.MakeName( "gaus" , g )
            gaus = RooGaussian( gausNames[1] , gausNames[1] , self.mass,mean,sigma)
            setattr( self, dmNames[0] ,  dm )
            setattr( self, sigmaNames[0] , sigma)
            setattr( self, meanNames[0] ,mean)
            setattr( self, gausNames[0] , gaus)
            self.FitParams[dmNames[0]] = dm 
            self.FitParams[sigmaNames[0]] = sigma
            self.FitUtils[ meanNames[0] ] = mean
            self.Gaussians[ gausNames[0] ] = gaus
            self.gaussians.add(gaus)
            if g<n-1:
                fracNames = self.MakeName("frac" , g)
                frac = self.GetParam( fracNames ,0.1,0.001,0.999)
                setattr( self, fracNames[0] , frac )
                self.FitParams[fracNames[0]] = frac
                self.coeffs.add(frac)
            # else :
            #     formula="1."
            #     for i in range(0 , n-1):
            #         formula += "-@%d"%(i)

            #     fracNames = self.MakeName("frac" , g)
            #     recFrac = RooFormulaVar( fracNames[1] , fracNames[1] , formula,self.coeffs)
            #     setattr( self, fracNames[0] ,  recFrac)
            #     self.FitUtils[ fracNames[0] ] = recFrac
            #     #self.coeffs.add(recFrac)


        sumNames = self.MakeName()
        self.BarePDFName = sumNames[0]
        self.SumOfGaussians = RooAddPdf( sumNames[1] , sumNames[1], self.gaussians,self.coeffs,True)

    def Print(self):
        for param in self.FitParams:
            self.FitParams[param].Print()

class SignalModel:
    def __init__(self, nrv , nwv , name , mass , color ,  systname = "" , variables=None ):
        self.NRV = nrv
        self.NWV = nwv

        self.Variables = variables
        
        self.Color = color
        if self.Color in [10,0,1] :
            self.Color = 49
        if systname :
            self.Title = systname
        else :
            self.Title = "rv(%d), wv(%d)" % (nrv, nwv)
            
        self.Name = name
        self.SystName = systname
        self.Mass = mass
        self.RV_ = nGaussians( nrv , "RV"+name , mass , systname , params = self.Variables)
        self.RV = self.RV_.SumOfGaussians
            
    def fitTo( self, DS , DSRV , DSWV , RVFraction , DSName , Print = False , verbose = -1 , doFit = True ):
        self.DSRV = DSRV
        self.DSWV = DSWV
        self.DS = DS
        print self.DS
        self.DSName = DSName
        if self.NWV == 0 :
            sumEntries = DS.sumEntries()
            coeffNames = self.RV_.MakeName( "signalNorm" )
            self.CoeffNorm = self.RV_.GetParam( coeffNames, sumEntries , sumEntries*0.5 , sumEntries*1.5 )

            #shapename = self.RV_.MakeName("SignalModelExtended")
            self.Signal = self.RV #RooExtendPdf(shapename[1] , shapename[1] , self.RV , self.CoeffNorm )
            self.FitParams = self.RV_.FitParams
            #self.FitParams[ coeffNames[0] ] = self.CoeffNorm
        else:
            self.WV_ = nGaussians( self.NWV , "WV"+self.Name , self.Mass , self.SystName , params = self.Variables )
            self.WV = self.WV_.SumOfGaussians

            
            rvfracnames = self.RV_.MakeName("RVFrac")
            self.Coeff = self.RV_.GetParam( rvfracnames , RVFraction , 0.8*RVFraction , 1.0)
            self.Signal = RooAddPdf( "SignalModel_" + self.Name , "SignalModel " + self.Name , self.RV, self.WV, self.Coeff )

            self.FitParams = self.RV_.FitParams
            for fpwv in self.WV_.FitParams:
                self.FitParams[ fpwv ] = self.WV_.FitParams[ fpwv ]
            self.FitParams[ rvfracnames[0] ] = self.Coeff

        if doFit :
            if self.NWV == 0 :
                DS.Print()
                #initial_stdout = sys.stdout
                #initial_stderr = sys.stderr
                #sys.stdout = open( '%s_%s' % (self.Name, self.SystName) , 'w')
                #sys.stderr = sys.stdout
                self.Res = self.Signal.fitTo( DS , RooFit.Minimizer("Minuit","minimize"),RooFit.SumW2Error(True),RooFit.Save(True) ,RooFit.PrintLevel(verbose) )
                #sys.stdout.close()
                #sys.stdout = initial_stdout
                #sys.stderr = initial_stderr
                allParamNames = self.FitParams.keys()
                self.All2DFitResults = []
                for p1 in range(0, len(self.FitParams) ):
                    P1 = self.FitParams[ allParamNames[p1] ]
                    for p2 in range(p1+1  , len(self.FitParams) ):
                        P2 = self.FitParams[ allParamNames[p2] ]

                        plot = RooPlot( P1 , P2 )
                        plot = self.Res.plotOn( plot , P1 , P2 , "ME12VHB" )
                        if plot :
                            ccc = TCanvas()
                            ccc.SetName( "bestFit_%s_%s_%s" % (self.Name , P1.GetName() , P2.GetName() ) )
                            ccc.cd()
                            plot.Draw()
                            self.All2DFitResults.append( ccc )
                        else :
                            print "2d plot for %s vs. %s is null" % (p1 , p2) 
                
                print self.Res
            else :
                self.ResRV = self.RV.fitTo( DSRV , RooFit.Minimizer("Minuit","minimize"),RooFit.SumW2Error(True),RooFit.Save(True), RooFit.PrintLevel(verbose) )
                self.ResWV = self.WV.fitTo( DSWV , RooFit.Minimizer("Minuit","minimize"),RooFit.SumW2Error(True),RooFit.Save(True), RooFit.PrintLevel(verbose) )

                # self.Res = self.Signal.fitTo( DS , RooFit.Minimizer("Minuit","minimize"),RooFit.SumW2Error(True),RooFit.Save(True), RooFit.PrintLevel(verbose) )
            #self.NLL = self.Res.minNll()

        if Print:
            for param_ in self.FitParams:
                param = self.FitParams[param_]
                print "%s = %.2f + %.2f - %.2f" % (param_ , param.getVal() , param.getAsymErrorHi() , param.getAsymErrorLo() )
            for i in range(0,5):
                print "========================================================="
                print ""

    def DrawRvWv( self ):
        self.PlotRvWv = TCanvas("PlotRvWv")
        self.PlotRvWv.Divide( 2, 1 )

        self.PlotRvWv.cd(1)
        self.FrameRv = self.Mass.frame( RooFit.Title(self.DSName + ", RV" ) , RooFit.Name(self.DSName + "_RV") , RooFit.Bins(50) )
        self.DSRV.plotOn( self.FrameRv , RooFit.Name(self.DSName + ", RV") )
        self.RV.plotOn( self.FrameRv , RooFit.LineColor( self.Color ) , RooFit.Name(self.DSName + ", RV Fitted")  )
        self.FrameRv.Draw()
        
        self.PlotRvWv.cd(2)
        self.FrameWv = self.Mass.frame( RooFit.Title(self.DSName + ", WV" ) , RooFit.Name(self.DSName + "_WV") , RooFit.Bins(50) )
        self.DSWV.plotOn( self.FrameWv , RooFit.Name(self.DSName + ", WV") )
        self.WV.plotOn( self.FrameWv , RooFit.LineColor( self.Color ) , RooFit.Name(self.DSName + ", WV Fitted")  )
        self.FrameWv.Draw()
        
    def Draw( self, plot = None  ):
        oldLL = 0.
        if plot == None :
            self.Plot = self.Mass.frame( RooFit.Title(self.DSName) , RooFit.Name(self.DSName) , RooFit.Bins(50) )
            self.DS.plotOn( self.Plot , RooFit.Name("Data") )
        else:
            self.Plot = plot
            oldLL = self.Plot.chiSquare()
        name = self.SystName if self.SystName else self.Name
        self.Signal.plotOn( self.Plot , RooFit.LineColor( self.Color ) , RooFit.Name(name)  )
        self.Chi2_2 = self.Plot.chiSquare()
        order = 3*(self.NRV+ self.NWV)-1
        self.Chi2_Norm = self.Chi2_2 / (50+order)
        self.Prob2 = TMath.Prob(self.Chi2_2,order )
        self.Prob3 = TMath.Prob( oldLL - self.Chi2_2  , 3 )
        self.Prob4 = TMath.Prob( ( oldLL/(order-3) ) - (self.Chi2_2/order)  , 3 )
        return self.Plot

    def SetDetails(self, prob , chi2 , nll ):
        self.Prob = prob
        self.Chi2 = chi2
        self.NLL = nll

    def GetDetails( self ):
        return (self.NRV, self.NWV , self.Prob, self.Chi2, self.NLL )

    def GetTitle(self):
        return "%s,%.2f,%.2f" % (self.Title, 100*self.Prob3 , self.Chi2_Norm)

    def Write(self, ws ):
        print self.Signal
        for p in self.FitParams:
            self.FitParams[p].Print()
        self.Signal.Print()
        getattr( ws , "import")( self.Signal , RooFit.RecycleConflictNodes() )

    
class Dataset :
    def Write(self, ws , dir_):
        self.FinalSignal.Write( ws )
        if self.CTCVRW :
            if self.DoCtCvFits:
                getattr(ws , "import")( self.CTCVRWParams["norm"].MakeVariable( self.FinalSignal.Signal.GetName() + "_norm" , 0.5  ) , RooFit.RecycleConflictNodes() )
                print "norm is imported"
            else :
                self.EfficiencyCtCv.GetCtOverCv()
                if "thq" in self.Name :
                    self.NormFromEff_List = RooArgList( self.EfficiencyCtCv.CtOverCvDataHistFunc , self.KappaFW.tHqXSectionTimesBR , self.KappaFW.SMtHqXSec , self.KappaFW.SMHggBR , self.KappaFW.LUMI  )
                elif "thw" in self.Name :
                    self.NormFromEff_List = RooArgList( self.EfficiencyCtCv.CtOverCvDataHistFunc , self.KappaFW.tHWXSectionTimesBR , self.KappaFW.SMtHWXSec , self.KappaFW.SMHggBR , self.KappaFW.LUMI  )
                self.NormFromEff_Formula = RooFormulaVar( self.FinalSignal.Signal.GetName() + "_norm" , self.Name + " Norm formula" ,  "1000.*@0*@1*@2*@3*@4/100." , self.NormFromEff_List )

                self.CTVariables = RooArgList( self.EfficiencyCtCv.CtOverCv , self.KappaFW.CV )
                self.CTVariable = RooFormulaVar("CT", "CT=ctovercv*CV" , "@0*@1" , self.CTVariables )
                getattr( ws, "import")( self.CTVariable , RooFit.RecycleConflictNodes() )
                getattr( ws, "import")( self.NormFromEff_Formula , RooFit.RecycleConflictNodes() )
        elif self.DOSysts :
            
            self.NormHggBRFormulaList = RooArgList( self.Norm.MakeSimpleVariable( self.FinalSignal.Signal.GetName() + "_norm_base" , 0.5  ) , self.KappaFW.BRGammaGamma ,
                                                    self.KappaFW.CT if "tth" in self.Name else self.KappaFW.CV )
            self.NormHggBRFormula = RooFormulaVar( self.FinalSignal.Signal.GetName() + "_norm" , self.Name + " Norm formula" , "@0*@1*@2*@2" , self.NormHggBRFormulaList )
            getattr(ws , "import")( self.NormHggBRFormula , RooFit.RecycleConflictNodes() )

        for ds in self.CTCVDS:
            getattr( ws, "import")( self.CTCVDS[ds]["ds"] )
        
        dir_.mkdir( self.Name ).cd()
        for c in self.Canvases:
            c.Write()
        dir_.cd()

    def AddCtCvCpDS(self, index , name = None , ds__ = None , additionalWeight = None , morevars = [] ):
        #mass = RooRealVar("CMS_hgg_mass" , "CMS_hgg_mass" , 0 , 0 , 1000 )
        #dZ = RooRealVar("dZ" , "dZ" , 0 , -1000 , 1000 )
        morevars_ = [var for var in morevars]
        morevars_.extend( ["CMS_hgg_mass" , "dZ" ] )
        print "new dataset index=" , index , "sample=" , self.Name , "name=" , name , "add_weight=", additionalWeight , "vars=" , morevars_
        
        Ct, Cv, Cp = -1 , 1 , -2
        if index != -1 :
            Ct, Cv, Cp = self.SumOfWeights.GetCValues(index)

        if Cp != -2 :
            return -1
        if index == -1:
            index = 50
        xsecBr_factor = self.KappaFW.GetXSecBR( self.Name , Ct, Cv )
        totalN_factor = 1 if index == 50 else self.TotalRatios.ValuesCtCv[ ( -1 , 1 ) ]/self.TotalRatios.ValuesCtCv[ ( Ct , Cv ) ]

        NewName = name if name else str(index)
        newWeight = RooRealVar("neww_"+NewName,"neww", 1.0 , -10 , 10 ) #"@0*@1", RooArgList(weight , var ) ) 
        varsToKeep = RooArgSet( newWeight )
        for var in morevars_ :
            varsToKeep.add( self.WS.var( var ) )
        DS__ = self.DS if not ds__ else ds__
        
        self.CTCVDS[ index if not name else name ] = {"ds":RooDataSet( DS__.GetName() + "_" + NewName , DS__.GetName() + "_" + NewName , varsToKeep ,  newWeight.GetName() ),
                                                      "CtCvCp":(Ct,Cv,Cp),
                                                      "name":NewName}

        for jj in range(0 , DS__.numEntries()):
            vals = DS__.get( jj )
            weight = DS__.weight()
            
            w_ctcv = 1 if index == 50 else vals["ctcv_%d"%(index)].getValV()

            additional_w = 1.0
            if additionalWeight :
                #print additionalWeight, vals
                additional_w = vals[ additionalWeight ].getValV()
            
            neww = w_ctcv*weight*xsecBr_factor*totalN_factor*LUMI*additional_w
            newWeight.setVal( neww )
            vals.add( newWeight )
            self.CTCVDS[ index if not name else name ]["ds"].add( vals , neww )

        return self.KappaFW.GetXSecBR( self.Name , Ct, Cv , False )*LUMI*1000.0

    def Print(self):
        print self.Name, self.DSRV.numEntries()+ self.DSWV.numEntries() , self.RVFraction, self.DSRV.sumEntries() , self.DSRV.numEntries() , self.DSWV.sumEntries() , self.DSWV.numEntries() 
    
    def __init__(self, ds, name , ws , whatToDo , TotalRatios = None , morevarstokeep = [] ): #whatToDo 0:nothing, 1:syst , 2:ct_cv
        self.Name = name
        self.DS = ds
        self.WS = ws

        self.DSWV = self.DS.reduce( RooFit.Cut("dZ > 1.0") )
        self.DSRV = self.DS.reduce( RooFit.Cut("dZ < 1.0") )
        dsrv = self.DSRV.sumEntries()
        dswv = self.DSWV.sumEntries()
        self.RVFraction = dsrv / (dsrv + dswv )
        #self.DS.Print()
        self.KappaFW = KappaFramework()

        self.DOSysts = (whatToDo == 1 or whatToDo == 3 or whatToDo == 4)
        self.CTCVRW = (whatToDo == 2 or whatToDo == 3 or whatToDo == 4)
        self.DoCtCvFits = (whatToDo  == 2 or whatToDo == 3)
        print whatToDo, self.DOSysts, self.CTCVRW
        self.CTCVDS = {}
        if self.CTCVRW :
            self.TotalRatios = TotalRatios

            format_=r'^ctcv_'  "(\d*)"
            allvars = ws.allVars()
            iter_ = allvars.iterator()
            var = iter_.Next()

            self.SumOfWeights = CtCvCpInfo("SumOfWeights_" + self.Name)
            self.TotalLumiWeighted = CtCvCpInfo("TotalLumiWeighted_" + self.Name)
            self.EfficiencyCtCv = CtCvCpInfo("Efficiency_" + self.Name )
            
            for i in range(0 , ws.allVars().getSize() ):
                matchObj= re.match( format_ ,  var.GetName() , re.M|re.I)
                if matchObj and len( matchObj.groups() ) == 1 and matchObj.groups()[0].isdigit() :
                    index = int( matchObj.groups()[0] )

                    #if not index in [18, 39 , 11] :
                    #    continue
                    
                    total_lumiw = self.AddCtCvCpDS( index , morevars = morevarstokeep )
                    if total_lumiw < 0 :
                        continue
                    
                    self.TotalLumiWeighted.SetValue( index , total_lumiw )
                    
                    #self.CTCVDS[ index ]["ds"].Print()
                    #print var.GetName(), index, self.CTCVDS[index]["CtCvCp"] , matchObj.groups()[0], self.CTCVDS[ index ]["ds"].sumEntries()
                    passed_weighted = self.CTCVDS[ index ]["ds"].sumEntries() 
                    self.SumOfWeights.SetValue( index , passed_weighted )
                    self.EfficiencyCtCv.SetValue( index ,100.* passed_weighted/total_lumiw )
                    
                var = iter_.Next()


            total_lumiw = self.AddCtCvCpDS(-1  , morevars = morevarstokeep)
            self.TotalLumiWeighted.SetValue( -1 , total_lumiw)
            self.DS = self.CTCVDS[50]["ds"] #self.DS.reduce( RooFit.SelectVars( selectedvarstokeep ) )
            passed_weighted = self.DS.sumEntries() 
            self.SumOfWeights.SetValue( -1 , passed_weighted)
            self.EfficiencyCtCv.SetValue( -1 , 100.*passed_weighted/total_lumiw )
            #self.DS.Print()

        
        self.SystDS = {}
        if self.DOSysts:
            format_=r'^'+ ds.GetName() + "_(.*)(Up|Down)(.*)"
            for ds_ in ws.allData():
                matchObj = re.match(format_ , ds_.GetName() , re.M|re.I)
                if matchObj:
                    #if not matchObj.group(1) in ["MCSmearLowR9EEPhi", "MCSmearHighR9EERho"] :
                    #    continue
                    #print matchObj.group(1), matchObj.group(2), matchObj.group(3)
                    if not matchObj.group(1) in self.SystDS:
                        self.SystDS[ matchObj.group(1) ] = {}
                    self.SystDS[ matchObj.group(1) ][ matchObj.group(2) ] = { "dsname":ds_.GetName() }
                    ds = self.WS.data(ds_.GetName())
                    if self.CTCVRW :
                        self.AddCtCvCpDS( -1 , matchObj.group(1)+ "_" + matchObj.group(2) , ds  , morevars = morevarstokeep )
                        self.SystDS[ matchObj.group(1) ][ matchObj.group(2) ]["ds"] = self.CTCVDS[ matchObj.group(1)+ "_" + matchObj.group(2) ]["ds"]
                    else:
                        self.SystDS[ matchObj.group(1) ][ matchObj.group(2) ]["ds"] = ds
                        
    def Plot(self, var):
        self.Canvases = self.All2DFitResults
        self.Canvases.append( self.CorrelationMatrix )
        
        self.Plot = var.frame( RooFit.Title(self.Name) , RooFit.Name(self.Name) , RooFit.Bins(20) )
        self.DS.plotOn( self.Plot , RooFit.Name("Data") )

        self.Central.Draw( self.Plot ) #, RooFit.LineColor( self.Central.Color )  RooFit.Name("Central") )

        self.CentralChi2 = self.Plot.chiSquare()
        self.InfoBox = TPaveText(0.6, 0.55, 0.9, 0.8,"BRNDC")
        self.InfoBox.SetFillColor(10)
        self.InfoBox.SetBorderSize(1)
        self.InfoBox.SetTextAlign(12)
        self.InfoBox.SetTextSize(0.04)
        self.InfoBox.SetFillStyle(1001)
        self.InfoBox.SetFillColor(10)
        self.InfoBox.AddText( "#chi^{2} = %.4f " % ( self.CentralChi2 ) )
        self.InfoBox.AddText( "MinNLL = %.4f " % ( 1000*self.CentralMinNLL ) )
        self.Plot.addObject( self.InfoBox)
        
        if self.DOSysts:
            for syst in self.SystDS :
                for variation in {"Up", "Down"}:
                    self.SystDS[syst][variation]["signal"].Draw( self.Plot ) # , RooFit.LineColor( kBlack ) , RooFit.Name( syst + variation ) )

        if self.DoCtCvFits:
            for i in self.CTCVDS:
                self.CTCVDS[i]["signal"].Draw( self.Plot ) # , RooFit.LineColor( kBlack ) , RooFit.Name( syst + variation ) )
            
                    
        c = TCanvas( self.Name + "Canvas_All" )
        setattr(self, "Canvas_All" , c )
        c.cd()
        self.Canvases.append( c )
        self.Plot.Draw()

        self.Legend = TLegend(0.75,0.2,0.95,0.85)
        self.Legend.SetName("legend_%s" % (self.Name) )
        self.Legend.AddEntry( "Data" , "Simulation" , "l" )
        self.Legend.AddEntry( "Central" , self.Central.GetTitle() , "l" )

        for i in self.CTCVDS:
            name = "ctcv" + str(i)
            self.Legend.AddEntry( name , str(i) , "l" )
            
        for syst in self.SystDS :
            name = "%sUp" % ( syst )
            self.Legend.AddEntry( name , syst , "l" )
            
        self.Legend.Draw()


        if self.DOSysts :
            for param in self.Params :
                self.Canvases.append( self.Params[param].Draw() )
        if  self.CTCVRW:
            if self.DoCtCvFits:
                for param in self.Params :
                    self.Canvases.append( self.CTCVRWParams[param].GetCanvas() )
            self.Canvases.append( self.SumOfWeights.GetCanvas() )
            self.Canvases.append( self.TotalLumiWeighted.GetCanvas() )
            self.Canvases.append( self.EfficiencyCtCv.GetCanvas() )
            self.Canvases.append( self.TotalRatios.GetCanvas() )
            
    def fit(self, rv , wv , mass):
        normcentral = LUMI*self.DS.sumEntries()
        print normcentral
        print self.DS
        self.CorrelationMatrix = None
        self.Central = SignalModel( rv , wv , self.Name  , mass , kBlack ,  "Central" )
        self.Central.fitTo( self.DS , self.DSRV , self.DSWV, self.RVFraction , "Central" , False , -1 , True )
        self.CorrelationMatrix = self.Central.Res.correlationHist()
        self.All2DFitResults = self.Central.All2DFitResults
        self.CentralMinNLL = self.Central.Res.minNll()
        self.Central.Signal.Print()
        self.CorrelationMatrix.Print("ALL")

        self.Norm = Variable( self.Central.Signal.GetName() +  "_norm" , normcentral , 10*normcentral , [] )
        
        self.Params = {}
        for param in self.Central.FitParams :
            var = self.Central.FitParams[ param ]
            self.Params[ param ] = Variable( param , var.getVal() , (abs(var.getErrorLo())+abs(var.getErrorHi()))/2 , [] )

        if self.DoCtCvFits:
            color = 1
            self.CTCVRWParams = {}
            self.CTCVRWParams["norm"] = Variable2D( "Norm_%s" % (self.Name) ) #CtCvCpInfo
            self.CTCVRWParams["norm"].SetValue( -1 , normcentral , 0.01*normcentral )
            for param in self.Central.FitParams :
                var = self.Central.FitParams[ param ]
                self.CTCVRWParams[ param  ] = Variable2D( param + "_%s" % (self.Name) ) #CtCvCpInfo
                self.CTCVRWParams[ param  ].SetValue( -1 , var.getVal() , (abs(var.getErrorLo())+abs(var.getErrorHi()))/2 )
                
            for i in self.CTCVDS:
                color += 1
                ds = self.CTCVDS[i]["ds"]
                self.CTCVDS[i]["signal"] = SignalModel( rv , wv , self.Name , mass ,  color ,  "ctcv" + str(i) )
                signal = self.CTCVDS[i]["signal"]
                signal.fitTo( ds , self.DSRV , self.DSWV , self.RVFraction , "ctcv" + str(i)  , False , -1 , True)
                #signal.Signal.Print()

                norm = ds.sumEntries()
                
                self.CTCVRWParams[ "norm" ].SetValue( -1 if i==50 else i , norm , 0 )
                
                print self.Name, i, signal
                
                for param in signal.FitParams :
                    var = signal.FitParams[ param ]
                    val = var.getVal()
                    self.CTCVRWParams[ param ].SetValue( -1 if i==50 else i , val , (abs(var.getErrorLo())+abs(var.getErrorHi()))/2 )
                    
       
        if self.DOSysts:
            color = 1
            for syst in self.SystDS :
                color += 1
                up = {}
                low = {}
                normup = 0
                normlow = 0
                for variation in ["Up", "Down"]:
                    #ds = self.WS.data( self.SystDS[syst][variation]["dsname"] )
                    ds = self.SystDS[syst][variation]["ds"]
                    self.SystDS[syst][variation]["signal"] = SignalModel( rv , wv , self.Name , mass ,  color ,  syst + variation )
                    self.SystDS[syst][variation]["signal"].fitTo( ds , self.DSRV , self.DSWV , self.RVFraction , syst + variation , False , -1 , True)
                    #self.SystDS[syst][variation]["signal"].Signal.Print()
                    
                    for param in self.SystDS[syst][variation]["signal"].FitParams :
                        var = self.SystDS[syst][variation]["signal"].FitParams[ param ]
                        if variation == "Up" :
                            up[ param ] = var.getVal()
                            normup = ds.sumEntries()
                        else :
                            low[ param ] = var.getVal()
                            normlow = ds.sumEntries()

                
                nuisancename = "CMS_hgg_nuisance_%s_13TeV"%(syst)
                if self.DoCtCvFits :
                    self.CTCVRWParams[ "norm" ].SetSyst( syst , nuisancename , normup , normlow )
                    for param_ in up :
                        param = self.CTCVRWParams[param_]
                        param.SetSyst( syst , nuisancename , up[param_] , low[param_] )
                
                self.Norm.Systs.append( Uncertainty( "norm"+syst+"_"+self.Name , normup , normcentral , normlow , 0 , nuisancename ) )
                for param_ in up :
                    param = self.Params[ param_ ]
                    param.Systs.append( Uncertainty( param_+syst , up[param_] , param.Value , low[param_] , 0 , nuisancename ) )


        if self.DoCtCvFits:
            self.FinalSignal = SignalModel( rv , wv , self.Name  , mass , kBlack ,  "" , self.CTCVRWParams )
            self.FinalSignal.fitTo( self.DS , self.DSRV , self.DSWV, self.RVFraction , "Final" , False , -1 , False )
            self.Params["norm"] = self.CTCVRWParams["norm"]
            return self.FinalSignal.Signal
        else :
            self.FinalSignal = SignalModel( rv , wv , self.Name  , mass , kBlack ,  "" , self.Params )
            self.FinalSignal.fitTo( self.DS , self.DSRV , self.DSWV, self.RVFraction , "Final" , False , -1 , False )
            self.Params["norm"] = self.Norm
            return self.FinalSignal.Signal
            
    def makeScaledPDF(self, lumi , uncert = 0.02):
        self.CoeffLumiCoefff = RooRealVar("Lumi"+self.Name , "Lumi"+self.Name , lumi , lumi*(1-uncert) , lumi*(1+uncert) )

        name = self.FinalSignal.Signal.GetName() + "_LumiScaledPlot"
        self.LumiScaled = RooExtendPdf( name , name , self.FinalSignal.Signal , self.CoeffLumiCoefff )
        #self.LumiScaled = self.FinalSignal.Signal #self.Central.Signal
        return self.LumiScaled
    
class FullModel:
    def __init__(self , signal , higgs , lumi):
        self.Signal = signal
        self.OtherHiggses = higgs
        self.Lumi = lumi

    def Write(self, filename , wsname ):
        self.FOut = TFile.Open( filename + ".root" , "RECREATE")
        self.WSOut = RooWorkspace(wsname)

        weight = RooRealVar("weight", "weight", 1.0 , -1000 , 1000 )
        mass = RooRealVar("CMS_hgg_mass" , "CMS_hgg_mass" , 0 , 0 , 1000 )
        dZ = RooRealVar("dZ" , "dZ" , 0 , -1000 , 1000 )
        varsToKeep = RooArgSet( mass , dZ , weight )

        self.AllDataset = self.Signal.DS.emptyClone("AllDatasets").reduce( RooFit.SelectVars(varsToKeep) )
        self.AllDataset.append( self.Signal.DS )

        AllPDFsList = RooArgSet(self.Signal.makeScaledPDF(self.Lumi) )
        
        for higgs in self.OtherHiggses:
            self.AllDataset.append( higgs.DS )
            AllPDFsList.add( higgs.makeScaledPDF(self.Lumi) )

        # if len(AllPDFsList) == 1 :
        #     self.AllPDFs = AllPDFsList.first()
        # else :
        #     self.AllPDFs = RooAddPdf( "AllPDFs" , "All PDFs" , AllPDFsList )

        self.FOut.cd()
        
        self.FinalCanvas = TCanvas("FinalCanvas")
        self.FinalPlot = self.Signal.Central.Mass.frame( RooFit.Title("Final Plot") , RooFit.Name("FinalPlot") , RooFit.Bins(50) )

        #self.AllPDFs.plotOn( self.FinalPlot , RooFit.LineColor( kBlack ) , RooFit.Normalization(self.Lumi) )
        # for pdf in AllPDFsList:
        #     pdf.plotOn( self.FinalPlot , RooFit.LineColor( kBlack ) , RooFit.Normalization(self.Lumi) , RooFit.Components( pdf.GetName() ) )
        self.AllDataset.plotOn( self.FinalPlot , RooFit.RefreshNorm() ,RooFit.Rescale( self.Lumi ) , RooFit.Components( AllPDFsList ) )

        #self.AllPDFs.Print()
        self.FinalPlot.Draw()
        self.FinalCanvas.Write()

        # print self.AllPDFs
        # getattr( self.WSOut , 'import')( self.AllPDFs , RooFit.RecycleConflictNodes() )
        print self.AllDataset
        getattr( self.WSOut , 'import')( self.AllDataset , RooFit.RecycleConflictNodes() )

        self.Signal.Write( self.WSOut , self.FOut )
        for higgs in self.OtherHiggses:
            higgs.Write( self.WSOut , self.FOut )
            
        self.WSOut.Write()
        self.FOut.Close()
        
                    
class FTest :
    def __init__( self, nrv_From , nrv_To , nwv_From , nwv_To , mass , ds ):
        self.Ranges = (nrv_From , nrv_To , nwv_From , nwv_To )
        self.Signals = {}
        self.Sample = ds.Name
        for nrv in range( nrv_From , nrv_To ):
            self.prevNll = 0
            for nwv in range ( nwv_From , nwv_To ):
                name = "%s_model_%d_%d" % (ds.Name ,  nrv , nwv )
                print "Start fitting for ", name
                color = (nrv-1)*8 + nwv + 1
                signal = SignalModel( nrv , nwv , name , mass , color )

                signal.fitTo( ds.DS , ds.DSRV , ds.DSWV , ds.RVFraction , ds.Name , True , 0)
                thisNll = signal.NLL
                chi2 = 2.*(self.prevNll-thisNll)
                diffInDof = 3
                prob = TMath.Prob(chi2,diffInDof)
                self.prevNll = thisNll
                signal.SetDetails( prob, chi2 , thisNll  )
                self.Signals[ name ] = signal


        for signal in self.Signals:
            print self.Signals[signal].GetDetails()



    def DrawAll(self):
        plot = None
        for nrv in range( self.Ranges[0] , self.Ranges[1] ):
            for nwv in range ( self.Ranges[2] , self.Ranges[3] ):
                name = "%s_model_%d_%d" % ( self.Sample , nrv , nwv )
                plot = self.Signals[name].Draw( plot )

        plot.Draw()

        
        self.Legend = TLegend(0.75,0.2,0.95,0.85)
        self.Legend.SetName("legend_%s" % (self.Sample) )
        self.Legend.AddEntry( "Data" , "Simulation" , "l" )
        for nrv in range( self.Ranges[0] , self.Ranges[1] ):
            for nwv in range ( self.Ranges[2] , self.Ranges[3] ):
                name = "%s_model_%d_%d" % ( self.Sample , nrv , nwv )
                self.Legend.AddEntry( name, self.Signals[name].GetTitle() , "l" )
        self.Legend.Draw()
