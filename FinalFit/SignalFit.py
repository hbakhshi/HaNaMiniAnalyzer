from ROOT import RooWorkspace, RooDataSet, RooPlot, RooRealVar, RooFit, RooExtendPdf, RooAbsPdf, RooFitResult, RooFormulaVar , RooGaussian, RooArgList, RooAddPdf, RooConstVar , RooArgSet
from ROOT import TFile, gSystem, TH1D, TCanvas,  kRed, kGreen, kBlack , TMath , TLegend, TGraphErrors, kBlue, kGray 
import re
from math import sqrt

AllSystParams = []

class KappaFramework:
    def __init__(self):
        self.BR_CoeffsVals= {"kb":0.57 , "kw":0.22  , "kg":0.09 , "ktau":0.06 , "kz":0.03 , "kc":0.03 , "kzg":0.0016 , "ks":0.0001 , "kmu":0.00022 }
        self.BR_Coeffs_List = []
        self.BR_Coeffs = RooArgList()
        for br_coeff in self.BR_CoeffsVals:
            coeff = RooConstVar( "kappa_br_coeff_%s" % (br_coeff) , br_coeff , self.BR_CoeffsVals[br_coeff] )
            self.BR_Coeffs_List.append( coeff )
            self.BR_Coeffs.add( coeff )

        self.CV = RooRealVar("CV" , "CV" , 1 , -2 , 2 )
        self.CT = RooRealVar("CT" , "CT" , 1 , -2 , 2 )
        
        self.KGamma2 = RooFormulaVar( "KGamma2" , "KGamma2" , "1.59*@0*@0+0.07*@1*@1-0.66*@0*@1" , RooArgList(  self.CV , self.CT ) )
        self.TotalWidth = RooFormulaVar("TotalWidth" , "TotalWidth" , "0.57+0.22*@0*@0+0.09+0.06+0.03+0.03+0.0016+0.0001+0.00022+0.0023*@1" , RooArgList( self.CV , self.KGamma2 ) )

        self.BRGammaGamma = RooFormulaVar("BRGammaGamma" , "H -> #gamma #gamma " , "@0/@1" , RooArgList( self.KGamma2 , self.TotalWidth ) )

        self.tHqXSection = RooFormulaVar( "tHqXSection" , "tHqXSection" , "2.633*@0*@0+3.578*@1*@1-5.211*@0*@1" , RooArgList( self.CT , self.CV ) )
        self.tHWXSection = RooFormulaVar( "tHWXSection" , "tHWXSection" , "2.909*@0*@0+2.31*@1*@1-4.22*@0*@1" , RooArgList( self.CT , self.CV ) )

        self.tHqXSectionTimesBR = RooFormulaVar( "tHqXSectionTimesBR" , "tHqXSectionTimesBR" , "@0*@1" , RooArgList( self.tHqXSection , self.BRGammaGamma ) )
        self.tHWXSectionTimesBR = RooFormulaVar( "tHWXSectionTimesBR" , "tHWXSectionTimesBR" , "@0*@1" , RooArgList( self.tHWXSection , self.BRGammaGamma ) )

    def SetCtCv(self, ct, cv ):
        self.CT.setVal( ct )
        self.CV.setVal( cv )

    def Print(self):
        print "CT : " , self.CT.getVal()
        print "CV : " , self.CV.getVal()
        print "KGamma2 : " , self.KGamma2.getVal()
        print "TotalWidth : " , self.TotalWidth.getVal()
        print "BRGammaGamma : " , self.BRGammaGamma.getVal()
        print "tHqXSection : " , self.tHqXSection.getVal()
        print "tHwXSection : " , self.tHWXSection.getVal()
        
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
            self.Var = RooRealVar( self.Name , self.Title , self.Value , lowerlimit if min_ < lowerlimit else min_  , self.Value+self.Stat )

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
            dmRange =2.

            dmNames = self.MakeName( "dm" , g )
            dm = self.GetParam( dmNames ,0,-dmRange,dmRange)
                        
            meanNames = self.MakeName( "mean" , g )
            mean = RooFormulaVar( meanNames[1] , meanNames[1] ,"@0+@1",RooArgList(self.MH,dm))

            sigmaNames = self.MakeName( "sigma" , g )
            sigma = self.GetParam( sigmaNames,1.*(g+1) ,0.8*(g+1),1.2*(g+1))

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
                frac = self.GetParam( fracNames ,0.1,0.01,0.99)
                setattr( self, fracNames[0] , frac )
                self.FitParams[fracNames[0]] = frac
                self.coeffs.add(frac)
            else :
                formula="1.";
                for i in range(0 , n-1):
                    formula += "-@%d"%(i)

                fracNames = self.MakeName("frac" , g)
                recFrac = RooFormulaVar( fracNames[1] , fracNames[1] , formula,self.coeffs)
                setattr( self, fracNames[0] ,  recFrac)
                self.FitUtils[fracNames[0] ] = recFrac
                self.coeffs.add(recFrac)


        sumNames = self.MakeName()
        self.BarePDFName = sumNames[0]
        self.SumOfGaussians = RooAddPdf( sumNames[1] , sumNames[1], self.gaussians,self.coeffs,False)

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
        self.DS = DS
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

            
            rvfracnames = self.RV_MakeName("RVFrac")
            self.Coeff = self.RV_.GetParam( rvfracnames , RVFraction , 0.8*RVFraction , 1.0)
            self.Signal = RooAddPdf( "SignalModel_" + self.Name , "SignalModel " + self.Name , self.RV, self.WV, self.Coeff )

            self.FitParams = self.RV_.FitParams
            for fpwv in self.WV_.FitParams:
                self.FitParams[ fpwv ] = self.WV_.FitParams[ fpwv ]
            self.FitParams[ rvfracnames[0] ] = self.Coeff

        if doFit :
            if self.NWV == 0 :
                self.Res = self.Signal.fitTo( DS , RooFit.Minimizer("Minuit","minimize"),RooFit.SumW2Error(True),RooFit.Save(True) ,RooFit.PrintLevel(verbose) )
            else :
                self.ResRV = self.RV.fitTo( DSRV , RooFit.Minimizer("Minuit","minimize"),RooFit.SumW2Error(True),RooFit.Save(True), RooFit.PrintLevel(verbose) )
                self.ResWV = self.WV.fitTo( DSWV , RooFit.Minimizer("Minuit","minimize"),RooFit.SumW2Error(True),RooFit.Save(True), RooFit.PrintLevel(verbose) )

                self.Res = self.Signal.fitTo( DS , RooFit.Minimizer("Minuit","minimize"),RooFit.SumW2Error(True),RooFit.Save(True), RooFit.PrintLevel(verbose) )
            self.NLL = self.Res.minNll()

        if Print:
            for param_ in self.FitParams:
                param = self.FitParams[param_]
                print "%s = %.2f + %.2f - %.2f" % (param_ , param.getVal() , param.getAsymErrorHi() , param.getAsymErrorLo() )
            for i in range(0,5):
                print "========================================================="
                print ""

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
        getattr( ws , "import")( self.Signal , RooFit.RecycleConflictNodes() )

    
class Dataset :
    def Write(self, ws , dir_):
        self.FinalSignal.Write( ws )
        getattr(ws , "import")( self.Norm.MakeSimpleVariable( self.FinalSignal.Signal.GetName() + "_norm" , 0.5  ) , RooFit.RecycleConflictNodes() )
        dir_.mkdir( self.Name ).cd()
        for c in self.Canvases:
            c.Write()
        dir_.cd()
        
    def __init__(self, ds, name , ws , DOSysts):
        self.Name = name
        self.DS = ds
        self.WS = ws
        
        self.DSWV = self.DS.reduce( RooFit.Cut("dZ > 1.0") )
        self.DSRV = self.DS.reduce( RooFit.Cut("dZ < 1.0") )
        dsrv = self.DSRV.sumEntries()
        dswv = self.DSWV.sumEntries()
        self.RVFraction = dsrv / (dsrv + dswv )
        #self.DS.Print()

        self.DOSysts = DOSysts
        if DOSysts:
            self.SystDS = {}
            format_=r'^'+self.DS.GetName() + "_(.*)(Up|Down)(.*)"
            for ds_ in ws.allData():
                matchObj = re.match(format_ , ds_.GetName() , re.M|re.I)
                if matchObj:
                    # if not matchObj.group(1) in ["MCSmearLowR9EEPhi"] :
                    #     continue
                    #print matchObj.group(1), matchObj.group(2), matchObj.group(3)
                    if not matchObj.group(1) in self.SystDS:
                        self.SystDS[ matchObj.group(1) ] = {}
                    self.SystDS[ matchObj.group(1) ][ matchObj.group(2) ] = { "dsname":ds_.GetName() }
                    
    def Plot(self, var):
        self.Canvases = []
        
        self.Plot = var.frame( RooFit.Title(self.Name) , RooFit.Name(self.Name) , RooFit.Bins(20) )
        self.DS.plotOn( self.Plot , RooFit.Name("Data") )

        self.Central.Draw( self.Plot ) #, RooFit.LineColor( self.Central.Color ) , RooFit.Name("Central")  )
        if self.DOSysts:
            for syst in self.SystDS :
                for variation in {"Up", "Down"}:
                    self.SystDS[syst][variation]["signal"].Draw( self.Plot ) # , RooFit.LineColor( kBlack ) , RooFit.Name( syst + variation ) )
        
        c = TCanvas( self.Name + "Canvas_All" )
        setattr(self, "Canvas_All" , c )
        c.cd()
        self.Canvases.append( c )
        self.Plot.Draw()

        self.Legend = TLegend(0.75,0.2,0.95,0.85)
        self.Legend.SetName("legend_%s" % (self.Name) )
        self.Legend.AddEntry( "Data" , "Simulation" , "l" )
        self.Legend.AddEntry( "Central" , self.Central.GetTitle() , "l" )
        for syst in self.SystDS :
            name = "%sUp" % ( syst )
            self.Legend.AddEntry( name , syst , "l" )
        self.Legend.Draw()


        if self.DOSysts:
            for param in self.Params :
                self.Canvases.append( self.Params[param].Draw() )
            # nPoints = len( self.SystDS )
            # for param in self.Central.FitParams :
            #     cname = "Canvas_" + param
            #     c = TCanvas( cname , cname )
            #     self.Canvases.append( c )
            #     setattr( self , cname , c )

            #     gname = "GraphSyst_" + param
            #     gSystem = TGraphErrors( nPoints )
            #     gSystem.SetName( gname )
            #     gSystem.SetTitle( param )
            #     setattr( self , gname , gSystem )

            #     gname = "GraphCentral_" + param
            #     gCentral = TGraphErrors( nPoints )
            #     gCentral.SetName( gname )
            #     gCentral.SetTitle( param )
            #     setattr( self , gname , gCentral )

            #     centralval = self.Central.FitParams[param].getVal()
            #     #centralErr = self.Central.FitParams[param].getAsymErrorHi()
            #     centralErr = self.Central.FitParams[param].getError()
            #     counter = 0
            #     labels = []
            #     for syst in self.SystDS :
            #         systUp = self.SystDS[syst]["Up"]["signal"].FitParams[param].getVal()
            #         systLo = self.SystDS[syst]["Down"]["signal"].FitParams[param].getVal()
            #         mean = (systUp+systLo)/2.0
            #         err = abs( systUp - systLo ) /2.0
            #         gSystem.SetPoint( counter , counter , mean )
            #         gSystem.SetPointError( counter , 0.5 , err )

            #         gCentral.SetPoint( counter , counter , centralval )
            #         gCentral.SetPointError( counter , 0.5 , centralErr )
            #         labels.append( syst )
            #         counter += 1

            #     c.cd()
            #     gCentral.SetFillColor( kGreen )
            #     gCentral.SetFillStyle( 3005 )
            #     gCentral.Draw("A3*")
            #     xax = gCentral.GetHistogram().GetXaxis()
            #     minXax = xax.GetBinLowEdge(1)
            #     maxXax = xax.GetBinUpEdge( xax.GetNbins() )
            #     xax.Set( len(labels) , minXax , maxXax )
            #     i = 1
            #     for lbl in labels:
            #         xax.SetBinLabel(i, lbl)
            #         i+=1

            #     gSystem.SetLineWidth( 2 )
            #     gSystem.Draw("P")

                
                
                    
    def fit(self, rv , wv , mass):
        normcentral = 35.9*self.DS.sumEntries()
        self.Central = SignalModel( rv , wv , self.Name  , mass , kBlack ,  "Central" )
        self.Central.fitTo( self.DS , self.DSRV , self.DSWV, self.RVFraction , "Central" , False , -1 , True )
        self.Central.Signal.Print()

        self.Norm = Variable( self.Central.Signal.GetName() +  "_norm" , normcentral , 10*normcentral , [] )
        
        self.Params = {}
        for param in self.Central.FitParams :
            var = self.Central.FitParams[ param ]
            self.Params[ param ] = Variable( param , var.getVal() , var.getError() , [] )
            
        if self.DOSysts:
            color = 1
            for syst in self.SystDS :
                color += 1
                up = {}
                low = {}
                normup = 0
                normlow = 0
                for variation in ["Up", "Down"]:
                    ds = self.WS.data( self.SystDS[syst][variation]["dsname"] )
                    self.SystDS[syst][variation]["signal"] = SignalModel( rv , wv , self.Name , mass ,  color ,  syst + variation )
                    self.SystDS[syst][variation]["signal"].fitTo( ds , self.DSRV , self.DSWV , self.RVFraction , syst + variation , False , -1 , True)
                    self.SystDS[syst][variation]["signal"].Signal.Print()
                    
                    for param in self.SystDS[syst][variation]["signal"].FitParams :
                        var = self.SystDS[syst][variation]["signal"].FitParams[ param ]
                        if variation == "Up" :
                            up[ param ] = var.getVal()
                            normup = 35.9*ds.sumEntries()
                        else :
                            low[ param ] = var.getVal()
                            normlow = 35.9*ds.sumEntries()

                
                nuisancename = "CMS_hgg_nuisance_%s_13TeV"%(syst)
                self.Norm.Systs.append( Uncertainty( "norm"+syst+"_"+self.Name , normup , normcentral , normlow , 0 , nuisancename ) )
                for param_ in up :
                    param = self.Params[ param_ ]
                    param.Systs.append( Uncertainty( param_+syst , up[param_] , param.Value , low[param_] , 0 , nuisancename ) )

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
                chi2 = 2.*(self.prevNll-thisNll);
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
