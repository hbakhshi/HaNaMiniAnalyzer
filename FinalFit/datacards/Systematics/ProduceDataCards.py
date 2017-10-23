from ROOT import TFile, TTree, TObject
import os
import stat
import sys
import math
import shutil
from ROOT import RooWorkspace, TCanvas , RooFit, TColor, kBlue, kRed, kGreen, RooRealVar, RooConstVar, gROOT, RooAbsArg, RooRealVar, gSystem, RooFit, RooAbsPdf, RooFormulaVar, RooArgList
from subprocess import call

dirName = sys.argv[1] + "/"
if os.path.exists(dirName):
    shutil.rmtree( dirName )
os.mkdir( dirName )

AllNuisances = [ "CMS_hgg_nuisance_MaterialForward_13TeV",
                 "CMS_hgg_nuisance_ShowerShapeHighR9EB_13TeV", 
                 "CMS_hgg_nuisance_MCSmearHighR9EEPhi_13TeV", 
                 "CMS_hgg_nuisance_ShowerShapeHighR9EE_13TeV", 
                 "CMS_hgg_nuisance_MCSmearHighR9EBPhi_13TeV", 
                 "CMS_hgg_nuisance_ShowerShapeLowR9EE_13TeV", 
                 "CMS_hgg_nuisance_MCScaleGain1EB_13TeV", 
                 "CMS_hgg_nuisance_MaterialCentralBarrel_13TeV", 
                 "CMS_hgg_nuisance_MCSmearLowR9EERho_13TeV", 
                 "CMS_hgg_nuisance_MCSmearHighR9EBRho_13TeV", 
                 "CMS_hgg_nuisance_MCScaleGain6EB_13TeV", 
                 "CMS_hgg_nuisance_MCScaleLowR9EB_13TeV", 
                 "CMS_hgg_nuisance_MCSmearLowR9EBRho_13TeV", 
                 "CMS_hgg_nuisance_FNUFEB_13TeV", 
                 "CMS_hgg_nuisance_FNUFEE_13TeV", 
                 "CMS_hgg_nuisance_MCScaleLowR9EE_13TeV", 
                 "CMS_hgg_nuisance_MCScaleHighR9EB_13TeV", 
                 "CMS_hgg_nuisance_MaterialOuterBarrel_13TeV", 
                 "CMS_hgg_nuisance_MCSmearLowR9EEPhi_13TeV", 
                 "CMS_hgg_nuisance_MCScaleHighR9EE_13TeV", 
                 "CMS_hgg_nuisance_MCSmearLowR9EBPhi_13TeV", 
                 "CMS_hgg_nuisance_MCSmearHighR9EERho_13TeV", 
                 "CMS_hgg_nuisance_ShowerShapeLowR9EB_13TeV"]



class SystHandler :
    def __init__(self, fname , wsname , pdfname , order = 3 ):
        self.Order = order
        self.FileIn = TFile.Open( fname )
        self.WS = self.FileIn.Get( wsname )
        self.PDF = self.WS.pdf( pdfname )
        self.norm = self.WS.function( pdfname + "_norm" )
        self.CT = self.WS.var("CtOverCv")
        self.CV = self.WS.var("CV")

        self.Params = {}
        self.Systs = {}
        self.samplename = pdfname.split("_")[0]
        self.SystsNuisances = {}
        for syst in AllNuisances:
            systName = syst.split("_")[3]
            self.SystsNuisances[ systName ] = RooRealVar( syst , syst , 0 , -1 , 1 )
            self.Systs[ systName ] = {}
            for arg in ["sigma", "dm" , "frac"]:
                for g in range(0, order):
                    if (arg,g) not in self.Params :
                        self.Params[ (arg,g) ] = { "central": self.WS.var( "%s_%s_mh125_g%d"  % (self.samplename , arg , g )) }
                    #const_RVthq_dm_mh125_g2MCSmearLowR9EERho
                    const_name = "const_%s_%s_mh125_g%d%s" % (self.samplename , arg , g , systName)
                    const_arg = self.WS.arg( const_name )
                    if const_arg :
                        #const_arg.Print()
                        self.Systs[ systName ][ (arg , g) ] = [const_arg , const_arg.getValV() ]
                        self.Params[ (arg,g) ][ systName ] =  const_arg.getValV()


    def MakeFormula( self , arg , g , systs , ignore_or_include ): #ignore_or_include 0:ignore systs, 1:include only systs
        name = "formula_%s_%s_mh125_g%d" % (self.samplename , arg , g )
        formula = "@0*(1"
        varlist = RooArgList( self.Params[(arg,g)]["central"] )
        counter = 1
        for syst in self.Params[(arg,g)] :
            val = self.Params[(arg,g)][syst]
            if syst == "central":
                continue
            keepIt = (syst in systs and ignore_or_include==1) or (syst not in systs and ignore_or_include==0)
            if keepIt :
                formula += "+@%d*%.4f" % (counter , val )
                varlist.add( self.SystsNuisances[ syst ] )
                counter += 1
        formula += ")"
        setattr( self, name , RooFormulaVar(name, name , formula , varlist ) )
        setattr( self, name + "_list" , varlist )
        return getattr( self, name )
                        
    def MakeANewWSWithFormula(self , ct, cv , newws , argsToWork , whatToDo , verbose=False ):  #whatToDo : 1:keep the list and set others to zero   ---- 0:set the list to zero and keep the rest
        for arg in ["sigma", "dm" , "frac"]:
            for g in range(0, self.Order):
                systs = [ syst for ( syst , arg_, g_ ) in argsToWork if arg_ == arg and g_ == g ]
                formula = self.MakeFormula( arg , g , systs , whatToDo )
                if verbose :
                    formula.Print()
                getattr( newws , "import")( formula , RooFit.Silence()  )
            
        getattr( newws , "import")( self.PDF , RooFit.RecycleConflictNodes() , RooFit.Silence() )

        self.CT.setVal( ct/cv )
        self.CV.setVal( cv )
        self.new_norm = RooRealVar( self.PDF.GetName() + "_norm"  , self.PDF.GetTitle() + " norm"  , self.norm.getVal() )
        getattr( newws , "import")( self.new_norm , RooFit.RecycleConflictNodes()  , RooFit.Silence() )
                        
    def MakeANewWS(self , ct, cv , newws , argsToWork , whatToDo , verbose=True ):  #whatToDo : 1:keep the list and set others to zero   ---- 0:set the list to zero and keep the rest
        self.CT.setVal( ct/cv )
        self.CV.setVal( cv )

        for syst in self.Systs :
            if verbose :
                print "\t",syst
            setToZero = ""
            keptAsItIs = ""
            for arg , g in self.Systs[syst] :
                const_term = self.Systs[syst][ ( arg , g ) ][0]
                const_value = self.Systs[syst][ ( arg , g ) ][1]
                isInList = ( syst, arg , g ) in argsToWork
                if whatToDo == 1 :
                    if isInList :
                        const_term 
                        getattr( newws , "import")( const_term  , RooFit.Silence() )
                        keptAsItIs += "%s_%d," % (arg , g)
                    else :
                        if len( self.Systs[syst][ ( arg , g ) ] ) < 3 :
                            zero_const = RooConstVar( const_term.GetName() , const_term.GetTitle() , 0 )
                            self.Systs[syst][ ( arg , g ) ].append( zero_const )
                        getattr( newws , "import")( self.Systs[syst][ ( arg , g )][2] , RooFit.RenameVariable( const_term.GetName() , const_term.GetName() ) , RooFit.Silence()  )
                        #self.Systs[syst][ ( arg , g )][2].Print()
                        #newws.Print()
                        #newws.arg( const_term.GetName() ).Print()
                        setToZero += "%s_%d," % (arg , g)
                elif whatToDo == 0 :
                    if not isInList :
                        getattr( newws , "import")( const_term , RooFit.Silence() )
                        keptAsItIs += "%s_%d," % (arg , g)
                    else :
                        if len( self.Systs[syst][ ( arg , g ) ] ) < 3 :
                            zero_const = RooConstVar( const_term.GetName() , const_term.GetTitle() , 0.000001 )
                            self.Systs[syst][ ( arg , g ) ].append( zero_const )
                        getattr( newws , "import")( self.Systs[syst][ ( arg , g )][2] , RooFit.Silence() )
                        setToZero += "%s_%d," % (arg , g)
            if verbose :
                print "\t\tSetToZero:",  setToZero
                print "\t\tKeptAsItIs:", keptAsItIs
            
        getattr( newws , "import")( self.PDF , RooFit.RecycleConflictNodes() , RooFit.Silence() )

        self.new_norm = RooRealVar( self.PDF.GetName() + "_norm"  , self.PDF.GetTitle() + " norm"  , self.norm.getVal() )
        getattr( newws , "import")( self.new_norm , RooFit.RecycleConflictNodes()  , RooFit.Silence() )


        

SignalModelInput = sys.argv[2] #"../../signals/11July"
thq = SystHandler( "%s/out_ctcv_thq_syst.root" % (SignalModelInput) , "ctcv" , "RVthq_mh125" )
thw = SystHandler( "%s/out_ctcv_thw_syst.root" % (SignalModelInput) , "ctcv" , "RVthw_mh125" )
tth = SystHandler( "%s/out_tth_syst.root"  % (SignalModelInput),  "cms_hgg_13TeV", "RVtth_mh125" )
vh = SystHandler( "%s/out_vh_syst.root"  % (SignalModelInput),  "cms_hgg_13TeV", "RVvh_mh125" )
allSamples = [thq, thw, tth , vh]

def ProduceForAllSysts():
    fOut = TFile.Open( dirName + "/input.root" , "recreate" )
    numberofnuisances = 32
    systName = "ALL"
    with open("Bin.txt", "rt") as fin:
        with open( dirName + "/Bin.txt", "wt") as fout:
            for line in fin:
                lout = line
                lout = lout.replace( "NUMBEROFNUISANCES" , "%d"%(numberofnuisances) )
                lout = lout.replace( "WSNAME" , systName )
                lout = lout.replace( "0.01" , "1.0" )
                fout.write( lout )


        ws = RooWorkspace( systName )
        for sample in allSamples :
            argsList = [ ]
            sample.MakeANewWSWithFormula(-1, 1 , ws , argsList , 0 )

        ws.Write()


def ProduceForAllParams_PlayWithOneSyst(whatToDo): #1:keep the list and set others to zero   ---- 0:set the list to zero and keep the rest
    fSubmit = open( dirName + "submit.sh" , "w" )
    fOut = TFile.Open( dirName + "/input.root" , "recreate" )

    numberofnuisancesToRemove = 1 if whatToDo==0 else len(AllNuisances)-1
    numberofnuisances = 32 - numberofnuisancesToRemove

    for syst in AllNuisances :
        systName = syst.split("_")[3]
        print systName
        with open("Bin.txt", "rt") as fin:
            with open( dirName + "/Bin%s.txt"%(systName), "wt") as fout:
                for line in fin:
                    lout = line
                    lout = lout.replace( "NUMBEROFNUISANCES" , "%d"%(numberofnuisances) )
                    lout = lout.replace( "WSNAME" , systName )
                    lout = lout.replace( "0.01" , "1.0" )
                    if syst in lout :
                        if whatToDo == 1 :
                            fout.write( lout )
                    else :
                        isLineForOtherSyst = False
                        for othersyst in [s for s in AllNuisances if s != syst]:
                            if othersyst in lout :
                                isLineForOtherSyst = True
                                if whatToDo == 0 :
                                    fout.write( lout )
                        if not isLineForOtherSyst :
                            fout.write( lout )


        ws = RooWorkspace( systName , syst)
        for sample in allSamples :
            allArgs = sample.Systs[systName]
            argsList = [ ( systName , arg , g ) for arg , g in allArgs ]

            sample.MakeANewWSWithFormula(-1, 1 , ws , argsList , whatToDo )

        ws.Write()

        fRun = open( dirName + "/run_%s.sh" % (systName) , "w" )
        fRun.write("cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/\n")
        fRun.write("eval `scramv1 runtime -sh`\n")
        fRun.write("cd FinalFit/datacards/Systematics/%s\n" % (dirName) )

        fRun.write("text2workspace.py Bin%s.txt\n" % (systName))
        fRun.write("combine --X-rtd ADDNLL_RECURSIVE=0 -n %s  -M  Asymptotic Bin%s.root --run=blind -m 125 --ct=%g --cv=%g\n" % (systName , systName, -1, 1 ) )
        fRun.close()
        st = os.stat(dirName + "/run_%s.sh" % (systName) )
        os.chmod(dirName + "/run_%s.sh" % (systName) , st.st_mode | stat.S_IEXEC)


        fSubmit.write( "bsub -J %s -o out_%s -q 1nh run_%s.sh\n" % (systName , systName , systName) )

    fSubmit.close()
    
def ProduceForSingleParam_PlayWithOneSyst(whatToDo): #1:keep the list and set others to zero   ---- 0:set the list to zero and keep the rest

    numberofnuisancesToRemove = 0 if whatToDo==0 else len(AllNuisances)-1
    numberofnuisances = 32 - numberofnuisancesToRemove

    fSubmitAll = open( dirName + "/submit.sh" , "w" )
    for s_ in allSamples:
        for arg,g in s_.Params :
            print s_.samplename, arg, g
            dirName_ = dirName
            dirName_ += "/%s_%s_%d" % (s_.samplename , arg , g )
            os.mkdir( dirName_ )
            fSubmit = open( dirName_ + "/submit.sh" , "w" )
            fSubmitAll.write( "cd %s\n" % (dirName_ ) )
            fSubmitAll.write( "source %s\n" % ("submit.sh") )
            fSubmitAll.write( "cd ..\n" )
            fOut = TFile.Open( dirName_ + "/input.root" , "recreate" )
            for systName in s_.Params[(arg,g)] :
                if systName == "central":
                    continue
                syst = s_.SystsNuisances[systName].GetName()
                print "\t" , syst
                with open("BinPerParam.txt", "rt") as fin:
                    with open( dirName_ + "/Bin%s.txt"%(systName), "wt") as fout:
                        for line in fin:
                            lout = line
                            lout = lout.replace( "NUMBEROFNUISANCES" , "%d"%(numberofnuisances) )
                            lout = lout.replace( "WSNAME" , systName )
                            lout = lout.replace( "0.01" , "1.0" )
                            if syst in lout :
                                if whatToDo == 1 :
                                    fout.write( lout )
                            else :
                                isLineForOtherSyst = False
                                for othersyst in [s for s in AllNuisances if s != syst]:
                                    if othersyst in lout :
                                        isLineForOtherSyst = True
                                        if whatToDo == 0 :
                                            fout.write( lout )
                                if not isLineForOtherSyst :
                                    fout.write( lout )


                ws = RooWorkspace( systName , syst)
                #print [(systName , arg , g)]
                s_.MakeANewWSWithFormula(-1, 1 , ws , [(systName , arg , g)] , whatToDo )
                for sample in allSamples :
                    if sample.samplename == s_.samplename :
                        continue
                    argsList = []
                    if whatToDo == 0 :
                        for syst in AllNuisances :
                            systName_ = syst.split("_")[3]
                            allArgs = sample.Systs[systName_]
                            argsList.extend( [ ( systName_ , arg , g ) for arg , g in allArgs ] )
                    #print argsList
                    sample.MakeANewWSWithFormula(-1, 1 , ws , argsList , whatToDo )
                ws.Write()

                fRun = open( dirName_ + "/run_%s.sh" % (systName) , "w" )
                fRun.write("cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/\n")
                fRun.write("eval `scramv1 runtime -sh`\n")
                fRun.write("cd FinalFit/datacards/Systematics/%s\n" % (dirName_) )

                fRun.write("text2workspace.py Bin%s.txt\n" % (systName))
                fRun.write("combine --X-rtd ADDNLL_RECURSIVE=0 -n %s  -M  Asymptotic Bin%s.root --run=blind -m 125 --ct=%g --cv=%g\n" % (systName , systName, -1, 1 ) )
                fRun.close()
                st = os.stat(dirName_ + "/run_%s.sh" % (systName) )
                os.chmod(dirName_ + "/run_%s.sh" % (systName) , st.st_mode | stat.S_IEXEC)


                fSubmit.write( "bsub -J %s -o out_%s -q 1nh run_%s.sh\n" % (systName , systName , systName) )

            #break
            fSubmit.close()
        #break
    fSubmitAll.close()

    
whatToDo = int( sys.argv[3] )
if whatToDo == 0 :
    ProduceForAllParams_PlayWithOneSyst(0) #0:set systamtics one-by-one to zero and keep the rest
elif whatToDo == 1 :
    ProduceForAllParams_PlayWithOneSyst(1) #1:keep systematics one-by-one and set others to zero
elif whatToDo == 2 :
    ProduceForSingleParam_PlayWithOneSyst(0) #0:set systamtics one-by-one to zero and keep the rest
elif whatToDo == 3 :
    ProduceForSingleParam_PlayWithOneSyst(1) #1:keep systematics one-by-one and set others to zero
elif whatToDo == 4 :
    ProduceForAllSysts()
