from ROOT import TFile, TTree, TObject
import os
import stat

import math
import shutil
from ROOT import RooWorkspace, TCanvas , RooFit, TColor, kBlue, kRed, kGreen, RooRealVar, RooConstVar, gROOT
from subprocess import call

from SignalFit import CtCvCpInfo

class DatasetInfo :
    def __init__(self, sample ,File, WS , PDF , eff_file , thqDomBinName , low,high , binCut , systematics):
        self.Cut = binCut
        self.Sample = sample
        self.File = File
        self.WS = WS
        self.PDF = PDF

        
        self.file = TFile.Open( self.File )
        self.ws = self.file.Get(self.WS)
        self.DS = self.ws.data( "%s_125_13TeV_THQLeptonicTag_50" % (self.Sample) )
        #self.file.ls()
        #print sample
        #self.file.ls()
        #self.ws.Print()
        #print self.ws, self.File, self.WS
        self.pdf = self.ws.pdf( self.PDF )
        self.norm = self.ws.function( self.PDF + "_norm" )
        self.CT = self.ws.var("CtOverCv")
        self.CT_Default = self.CT.getVal()
        
        self.CV = self.ws.var("CV")
        self.CV_Default = self.CV.getVal()
        
        self.Low = low
        self.High = high

        self.Systematics = {}
        
        self.EfficiencyFile = TFile.Open( eff_file )
        gROOT.cd()
        self.EffHist = self.EfficiencyFile.Get("%(sample)s/%(bin)s/h%(sample)s_%(bin)s_eff_CtCv" % {"sample":sample , "bin":thqDomBinName}).Clone("Eff_%s" % sample )
        for syst in systematics :
            hsyst = self.EfficiencyFile.Get("%(sample)s/%(bin)s/%(sample)s_%(bin)s_%(syst)s" % {"sample":sample , "bin":thqDomBinName , "syst":syst})
            self.Systematics[syst] = ( 1.+ hsyst.GetBinContent(1) , 1.+ hsyst.GetBinContent(2) )
        self.EfficiencyFile.Close()
        #self.EffHist.Print()
        self.Eff_CtCvInfo = CtCvCpInfo( "Eff_CtCvInfo_%s_%s" % (sample , thqDomBinName) )
        self.Eff_CtCvInfo.FillFrom2DHisto( self.EffHist )
        #self.GetCtOverCv()
        
    def MakeANewWS(self , ct, cv , newws ):
        self.CT.setVal( self.CT_Default )
        self.CV.setVal( self.CV_Default )

        for vname in ["frac", "dm", "sigma"]:
            for gnumber in range(0,4) :
                varname = "RV%s_%s_mh125_g%d" % (self.Sample , vname , gnumber )
                var = self.ws.var( varname )
                if var :
                    #var.Print()
                    var.removeRange()
                    var.setConstant()
                    #var.Print()
                else :
                    var = self.ws.arg( varname )
                    if vname == "frac" and gnumber == 3 :
                        continue
                    elif var :
                        continue
                    else:
                        print varname, "wasn't found in ws"

        for syst in ["metPhoUncertainty" , "metJecUncertainty" , "metJerUncertainty" , "metUncUncertainty" , "SigmaEOverEShift" , "MvaShift" , "JER" , "JEC"] :
            nuis_name = "CMS_hgg_nuisance_%s_13TeV" % (syst)
            nuisance = self.ws.arg( nuis_name )
            if nuisance :
                nuisance.removeRange()
                nuisance.setConstant()
            else :
                print nuis_name, "for sample" , self.Sample, "was not found"

            #for variation in ["Up", "Down"] :
            #    self.ws.data( "%s_125_13TeV_THQLeptonicTag_%s%s01sigma_%s_%s" % (self.Sample , syst , variation , syst , variation) ).Print()
                        
        getattr( newws , "import")( self.pdf , RooFit.RecycleConflictNodes() , RooFit.Silence() )

        
        self.CT.setVal( ct )
        self.CV.setVal( cv )


        factor = 1.0
        #if self.Sample == "thw" :
        #    factor = 1.8
            
        self.new_norm = RooRealVar( self.PDF + "_norm"  , self.PDF + "_norm"  , factor*self.norm.getVal() ) # , factor*self.Low*self.norm.getVal() , factor*self.High*self.norm.getVal() )
        getattr( newws , "import")( self.new_norm , RooFit.RecycleConflictNodes() , RooFit.Silence() )

    def MakeDataCardLine(self, ct, cv , line ):
        eff_vals = self.Eff_CtCvInfo.AllCtOverCVs[ ct/cv ]
        eff = eff_vals[ eff_vals.keys()[0] ] 
        #binCt = self.EffHist.GetYaxis().FindBin( ct )
        #binCv = self.EffHist.GetXaxis().FindBin( cv )
        #eff = self.EffHist.GetBinContent( binCv , binCt )
        for syst in self.Systematics:
            line = line.replace( self.Sample + syst , "%.4f/%.4f" % self.Systematics[syst] )
        
        return line.replace( "%sRate" % self.Sample , "%.4f" % eff )
        
class BinDatacard :
    def __init__(self, BinName  , EffPlotName = None ):
        self.AllBinCuts = {"Preselection":"1==1" ,
                           "THQLeptonicTHQTag":"(n_jets == 2 && n_L_bjets == 1 && ( fwdjet1_eta > 2.5 || fwdjet1_eta < -2.5 ))",
                           "THQLeptonicTTHTag":"( (n_jets > 2 &&  abs(fwdjet1_eta)>2.5) || (abs(fwdjet1_eta)<=2.5) )",
                           "MVATHQ":  "MVA_Medium > 0" ,
                           "MVATTH":  "MVA_Medium <= 0",
                           "EtaNJetTTHTag":"!(n_jets == 2 && ( abs(fwdjet1_eta) >= 2.5 ) )",
                           "EtaNJetTHQTag":"(n_jets == 2 && ( abs(fwdjet1_eta) >= 2.5 ) )",
                           "EtaNbJetTTHTag":"!(n_L_bjets == 1 && ( abs(fwdjet1_eta) >= 2.5 ) )",
                           "EtaNbJetTHQTag":"(n_L_bjets == 1 && ( abs(fwdjet1_eta) >= 2.5 ) )",
                           "NJetNbJetTTHTag":"!(n_L_bjets == 1 && n_jets == 2)",
                           "NJetNbJetTHQTag":"(n_L_bjets == 1 && n_jets == 2 )"}
        
        self.Cut = self.AllBinCuts[ "Preselection" if BinName == "THQLeptonicTag" else BinName ]
        
        if not EffPlotName :
            EffPlotName = BinName
            
        self.BinName = BinName
        self.HiggsSamples = {}
        self.SystList = ["JER", "JEC" , "metJerUncertainty" , "metUncUncertainty" , "metPhoUncertainty" , "metJecUncertainty" ,"UnmatchedPUWeight","MvaLinearSyst","LooseMvaSF","PreselSF","electronVetoSF","TriggerWeight","FracRVWeight","FracRVNvtxWeight","ElectronWeight","MuonWeight","MuonMiniIsoWeight","JetBTagCutWeight","JetBTagReshapeWeight"]
        for sys in ["UnmatchedPUWeight","FracRVWeight","FracRVNvtxWeight","MuonMiniIsoWeight","JetBTagReshapeWeight"]:
            self.SystList.remove( sys )
        
        #self.HiggsSamples["thq"] = DatasetInfo("thq" , "../../out_ctcv_thq_syst.root", "ctcv", "RVthq_mh125" , "2dPlots.root" ,   EffPlotName, 0.99999 , 1.00001 )
        self.HiggsSamples["thq"] = DatasetInfo("thq" , "../../signals/22June/out_ctcv_thq_syst.root", "ctcv", "RVthq_mh125" , "2dPlots.root" ,   EffPlotName, 0.99999 , 1.00001 , self.Cut  , self.SystList  )
        self.HiggsSamples["thw"] = DatasetInfo("thw" , "../../signals/22June/out_ctcv_thw_syst.root", "ctcv", "RVthw_mh125" ,  "2dPlots.root" ,  EffPlotName, 0.99999 , 1.00001 , self.Cut  , self.SystList )
        self.HiggsSamples["tth"] = DatasetInfo("tth" , "../../signals/22June/out_tth_syst.root", "cms_hgg_13TeV", "RVtth_mh125",  "2dPlots.root",EffPlotName , 0.99999 ,1.00001 , self.Cut  , self.SystList )
        self.HiggsSamples["vh"]  = DatasetInfo("vh" , "../../signals/22June/out_vh_syst.root", "cms_hgg_13TeV", "RVvh_mh125" ,  "2dPlots.root" , EffPlotName, 0.99999 , 1.00001 , self.Cut  , self.SystList )

    def Write(self, kf , kv , dirname  ):
        ws = RooWorkspace("WS%s" % (self.BinName) )
        for sample in self.HiggsSamples:
            self.HiggsSamples[sample].MakeANewWS( kf , kv , ws )
        ws.Write()

        with open("Bin.txt", "rt") as fin:
            with open( dirname + "/Bin%s.txt"%(self.BinName), "wt") as fout:
                for line in fin:
                    lout = line.replace( "BINNAME" , self.BinName )
                    for hs in self.HiggsSamples:
                        lout = self.HiggsSamples[hs].MakeDataCardLine( kf , kv , lout  )
                    fout.write( lout )

Preselection = BinDatacard( "THQLeptonicTag", "Preselection" )
AllBins = {}
AllBins["THQLeptonic"] = {"THQ":BinDatacard( "THQLeptonicTHQTag" ) ,
                          "TTH":BinDatacard( "THQLeptonicTTHTag" ) }
AllBins["MVA"] = { "THQ":BinDatacard("MVATHQ"),
                   "TTH":BinDatacard("MVATTH") }
AllBins["EtaNJet"] = {"THQ":BinDatacard("EtaNJetTHQTag"),
                      "TTH":BinDatacard("EtaNJetTTHTag") }
AllBins["EtaNbJet"] = {"THQ":BinDatacard("EtaNbJetTHQTag"),
                       "TTH":BinDatacard("EtaNbJetTTHTag") }
AllBins["NJetNbJet"] = {"THQ":BinDatacard("NJetNbJetTHQTag"),
                        "TTH":BinDatacard("NJetNbJetTTHTag") }

Kvs = [1.0 , 1.5 , 0.5]
KvKfs = {
    1.0:[ -3. , -2. , -1.5 , -1.25        , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ],
    1.5:[ -3. , -2. , -1.5 , -1.25 ,  -1.0, -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ],
    0.5:[ -3. , -2. , -1.5 , -1.25 ,  -1.0, -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ]
}
AllCtOverCVs = {}
for Kv in Kvs:
    for Kf in KvKfs[Kv]:
        r = Kf/Kv
        if r in AllCtOverCVs.keys() :
            AllCtOverCVs[r][Kv] = 0.0
        else :
            AllCtOverCVs[r] = {Kv:0.0}

submitLx = open( "./submit.sh" , "w")
for kvkt in AllCtOverCVs:
    #if kvkt != -1 :
    #    continue
    
    kf = kvkt
    kv = 1
    dirname = "ctcv%g" % (kvkt)
        
    if os.path.exists( dirname ):
        shutil.rmtree( "./" + dirname )
    os.mkdir( dirname )
        
    fRun = open( dirname + "/run.sh" , "w" )
    
    fRun.write("cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/FinalFit\n")
    fRun.write("eval `scramv1 runtime -sh`\n")
    fRun.write("cd datacards/30June/%s\n" % (dirname) )

    fWS = TFile.Open( dirname + "/input.root" , "recreate")

    Preselection.Write( kf, kv , dirname )
    fRun.write("text2workspace.py Bin%s.txt\n" % (Preselection.BinName))
    fRun.write("combine -n Preselection  -M  Asymptotic Bin%s.root --run=blind -m 125.5 --ct=%g --cv=%g\n" % (Preselection.BinName, kf, kv ) )

    for Bin in AllBins:
        AllBins[Bin]["THQ"].Write( kf , kv , dirname  )
        fRun.write("text2workspace.py Bin%s.txt\n" % (AllBins[Bin]["THQ"].BinName) )
        fRun.write("combine -n %s  -M  Asymptotic Bin%s.root --run=blind -m 125.5 --ct=%g --cv=%g\n" % (AllBins[Bin]["THQ"].BinName,AllBins[Bin]["THQ"].BinName,kf,kv) )
            
        AllBins[Bin]["TTH"].Write( kf , kv , dirname  )
            
        fRun.write("combineCards.py Bin%s.txt Bin%s.txt > Combined%s.txt\n" % (AllBins[Bin]["THQ"].BinName, AllBins[Bin]["TTH"].BinName, Bin) )
        fRun.write("text2workspace.py Combined%s.txt\n" % (Bin) )
        fRun.write("combine -n %s -M Asymptotic Combined%s.root --run=blind -m 125.5 --ct=%g --cv=%g\n" % (Bin , Bin , kf,kv) )

    fWS.Close()
        
    fRun.close()
    st = os.stat(dirname + "/run.sh")
    os.chmod(dirname + "/run.sh", st.st_mode | stat.S_IEXEC)

    submitLx.write( "cd %s\n" % (dirname) )
    submitLx.write( "bsub -J %s -o out -q 1nd run.sh\n" % dirname )
    submitLx.write( "cd ..\n" )
    
submitLx.close()
