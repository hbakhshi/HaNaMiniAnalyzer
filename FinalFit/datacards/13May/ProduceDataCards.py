from ROOT import TFile, TTree, TObject
import os
import math
import shutil
from ROOT import RooWorkspace, TCanvas , RooFit, TColor, kBlue, kRed, kGreen, RooRealVar

HiggsSamples = {}
class DatasetInfo :
    def __init__(self, File, WS , PDF , low,high):
        self.File = File
        self.WS = WS
        self.PDF = PDF

        self.file = TFile.Open( self.File )
        self.file.ls()
        self.ws = self.file.Get(self.WS)
        print self.ws, self.File, self.WS
        self.pdf = self.ws.pdf( self.PDF )
        self.norm = self.ws.function( self.PDF + "_norm" )
        self.CT = self.ws.var("CT")
        self.CV = self.ws.var("CV")

        self.Low = low
        self.High = high

    def MakeANewWS(self , ct, cv , newws ):
        self.CT.setVal( ct )
        self.CV.setVal( cv )

        getattr( newws , "import")( self.pdf , RooFit.RecycleConflictNodes() )

        self.new_norm = RooRealVar( self.PDF + "_norm"  , self.PDF + "_norm"  , self.norm.getVal() , self.Low*self.norm.getVal() , self.High*self.norm.getVal() )
        getattr( newws , "import")( self.new_norm , RooFit.RecycleConflictNodes() )

        
HiggsSamples["thq"] = DatasetInfo("../../signals/13May/out_ctcv_thq_syst.root", "ctcv", "RVthq_mh125" , 0.999 , 1.001 )
HiggsSamples["thw"] = DatasetInfo("../../signals/13May/out_ctcv_thw_syst.root", "ctcv", "RVthw_mh125" , 0.999 , 1.001 )
HiggsSamples["tth"] = DatasetInfo("../../signals/13May/out_tth_syst.root", "cms_hgg_13tev", "RVtth_mh125" , 0.999 , 1.001 )
HiggsSamples["vh"]  = DatasetInfo("../../signals/13May/out_vh_syst.root", "cms_hgg_13tev", "RVvh_mh125" , 0.999 , 1.001 )

Kvs = [1.0 , 1.5 , 0.5]
KvKfs = {
    1.0:[3. , 2. , 1.5 , 1.25 ,  1.0, .75 , .5 , .25 , 0.0 , -0.25 , -0.5 , -0.75 , -1  , -1.25 , -1.5 , -2. , -3. ],
    1.5:[3. , 2. , 1.5 , 1.25 ,  1.0, .75 , .5 , .25 , 0.0 , -0.25 , -0.5 , -0.75 ,-1 , -1.25 , -1.5 , -2. , -3. ],
    .5:[3. , 2. , 1.5 , 1.25 ,  1.0, .75 , .5 , .25 , 0.0 , -0.25 , -0.5 , -0.75 ,-1 , -1.25 , -1.5 , -2. , -3. ]
}

for kv in Kvs :
    fRunKv = open( "./RunKv%g.sh" % kv , "w" )
    for kf in KvKfs[kv]:
        #if not (kv,kf) == (1.0 , -1 ):
        #    continue
        dirname = "ct%gcv%g" % (kf, kv)
        if not os.path.exists( dirname ):
            os.mkdir( dirname )
        fnew = TFile.Open( dirname + "/input.root" , "recreate")
        ws = RooWorkspace("WS")

        for sample in HiggsSamples:
            HiggsSamples[sample].MakeANewWS( kf , kv , ws )

        ws.Write()
        fnew.Close()
        
        
        shutil.copyfile( "./card.txt" , dirname + "/card.txt" )

        fRun = open( dirname + "/run.sh" , "w" )
        fRun.write("cd /home/hbakhshi/Desktop/tHq/HiggsAnalysis/CombinedLimit\n")
        fRun.write("source env_standalone.sh\n")
        fRun.write("cd -\n")

        fRun.write("text2workspace.py card.txt\n")
        fRun.write("combine  -M  Asymptotic card.root --run=blind -m 125.5 --ct=%g --cv=%g\n" % (kf,kv) )

        fRun.close()

        fRunKv.write( "cd %s\n" % (dirname) )
        fRunKv.write( "source run.sh\n" )
        fRunKv.write( "cd ..\n" )

    fRunKv.close()
