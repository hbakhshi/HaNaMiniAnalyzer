from ROOT import TFile, TTree, TObject
import os
import stat

import math
import shutil
from ROOT import RooWorkspace, TCanvas , RooFit, TColor, kBlue, kRed, kGreen, RooRealVar, RooConstVar, gROOT, RooAbsArg, RooRealVar, gSystem, RooFit
from subprocess import call

fEff = TFile.Open("fSignificance.root")
hTHQ = fEff.Get("THQ_SR_diphoMVA_0")
hTHW = fEff.Get("THW_SR_diphoMVA_0")
hTTH = fEff.Get("TTH_SR_diphoMVA_0")
hVH = fEff.Get("THQ_SR_diphoMVA_0")
hBkg = fEff.Get("NormMG_GG")

def GetEff( h , bin_from ):
    integral_total = h.Integral()
    integral = h.Integral( bin_from , 100 )
    return integral/integral_total

gSystem.Load("~/Desktop/tHq/HiggsAnalysis/CombinedLimit/lib/libHiggsAnalysisCombinedLimit.so")
#gSystem.Load("~/work/tHq/CMSSW_7_4_7/lib/slc6_amd64_gcc491/libHiggsAnalysisCombinedLimit.so")
#filename, tagname = "../../bkg/CRInvertLeptCut22July/CRInvertLepCut.root", "CRInvertLepCutTHQLeptonicTag"
filename, tagname = "../../bkg/25June/THQLeptonicTag.root" ,"THQLeptonicTag"
orig_bkg_file = TFile.Open(filename)
orig_wspace   = orig_bkg_file.Get("multipdf")
orig_multipdf = orig_wspace.arg("CMS_hgg_%s_13TeV_bkgshape" % (tagname) )
orig_bkg_norm = orig_wspace.var("CMS_hgg_%s_13TeV_bkgshape_norm" % (tagname) )
orig_bkg_norm_ = orig_bkg_norm.getValV() #140

fbkg = TFile.Open("ctcv-1/bkg_limitedNorm.root", "recreate")


fSubmit = open( "submit.sh" , "w" )
fSubmit.write( "cd ctcv-1\n")
for bin_id in range(7,21):
    ws = RooWorkspace( "multipdf%d" % (bin_id) )
    getattr( ws , "import")( orig_multipdf ,  RooFit.RecycleConflictNodes() , RooFit.Silence() )
    
    thq_rate = GetEff( hTHQ , bin_id )
    thw_rate = GetEff( hTHW , bin_id )
    tth_rate = GetEff( hTTH , bin_id )
    vh_rate  = GetEff( hVH  , bin_id )
    bkg_rate = GetEff( hBkg , bin_id ) #0.43* 0.43 comes from SR/CR

    bkg_norm = bkg_rate*orig_bkg_norm_
    bkg_norm = RooRealVar( orig_bkg_norm.GetName() , orig_bkg_norm.GetTitle() , bkg_norm , 0 , 3.*bkg_norm ) #0.9*bkg_norm , 1.1*bkg_norm )
    bkg_norm.Print()
    getattr( ws , "import")( bkg_norm ,  RooFit.RecycleConflictNodes() , RooFit.Silence() )
    fbkg.cd()
    ws.Write()
    
    dirname = "ctcv-1"
    with open("BinOneSignal.txt", "rt") as fin: #Bin.txt , BinNewSignal.txt
        with open( dirname + "/Bin%d.txt"%(bin_id), "wt") as fout:
            for line in fin:
                lout = line.replace( "bkgRate" , "%.2f" % (1.) )
                lout = lout.replace( "thqRate" , "%.2f" % (thq_rate) )
                lout = lout.replace( "thwRate" , "%.2f" % (thw_rate) )
                lout = lout.replace( "tthRate" , "%.2f" % (tth_rate) )
                lout = lout.replace( "vhRate" , "%.2f" % (vh_rate) )
                lout = lout.replace( "BININDEX" , "%d" % (bin_id ) )
                lout = lout.replace( "BINNAME" , tagname )
                fout.write( lout )

    fRun = open( dirname + "/run%d.sh" % (bin_id) , "w" )
    #fRun.write("cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/\n")
    #fRun.write("eval `scramv1 runtime -sh`\n")
    #fRun.write("cd FinalFit/datacards/DiPhoMVACut/%s\n" % (dirname) )

    fRun.write("text2workspace.py Bin%d.txt\n" % (bin_id))
    fRun.write("combine --X-rtd ADDNLL_RECURSIVE=0 -n Preselection%d  -M  Asymptotic Bin%d.root --run=blind -m 125 --ct=%g --cv=%g\n" % (bin_id , bin_id, -1, 1 ) )
    fRun.close()
    
    #fSubmit.write( "bsub -J Cut%d -o out -q 1nh run%d.sh\n" % (bin_id, bin_id) )
    fSubmit.write( "source run%d.sh\n" % (bin_id) )

fSubmit.close()
