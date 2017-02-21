#!/usr/bin/env python
############MAKE SAMPLE LIST : ###################

LUMI = 35.5

import os
import os.path
import math
import sys
import glob
from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *
from tHqAnalyzer.HaNaMiniAnalyzer.SampleType import *
Sample.WD = os.path.dirname(os.path.abspath(__file__))
from ROOT import kGray, kGreen, kYellow, kOrange, kRed, kBlack, kCyan, kBlue, gROOT, TLatex, TCanvas, TFile, TColor, TSystem

TreeTemN = "thqLeptonicTagDumper/trees/%s_13TeV_all"
DIR = "/home/hbakhshi/Downloads/tHq_Georgios/output/18_02_17/"


cutJetGamma = "(!(dipho_lead_prompt==1 && dipho_sulead_prompt==1) && (dipho_lead_prompt==1 || dipho_sulead_prompt==1))"
cutJetJet = "(dipho_lead_prompt!=1 && dipho_sulead_prompt!=1)"
cutGammaGamma = "(dipho_lead_prompt==1 && dipho_sulead_prompt==1)"

data_files = sorted( glob.glob( DIR + "/data/Run2016*.root" ) , key=os.path.getsize) 
dataSamples = SampleType("Data" , kBlack , [ Sample( os.path.basename(s).split('.')[0] , 0 , False , "" , treeName = TreeTemN % ("Data") ) for s in data_files ] , os.path.dirname(data_files[0]) )

gjets_files = { DIR + "/bkgs/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8.root":TreeTemN % ("gjet"),
                DIR + "/bkgs/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8.root":TreeTemN % ("gjet") }
qcd_files = glob.glob(DIR+"/bkgs/QCD*.root")
fake_files = gjets_files
for file in qcd_files :
    fake_files[file] = TreeTemN % ("qcd")


gjet = SampleType("gammajet" , kCyan-2  , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in fake_files.items()  ] , DIR+"/bkgs/" , additionalCut = cutJetGamma )
jetJet = SampleType("jetjet" , kCyan-3  , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in fake_files.items()  ] , DIR+"/bkgs/" , additionalCut = cutJetJet )

digamma_files = {DIR + "/bkgs/DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8.root":TreeTemN % ("dipho") }
# DIR + "/bkgs/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa.root":TreeTemN % ("dipho") }

digSamples = SampleType("DiGamma" , kOrange , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName = t  ) for s,t in digamma_files.items() ] , DIR+"/bkgs/" , additionalCut = cutGammaGamma )
#QCDSamples = SampleType("QCD" , kCyan-8  , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=TreeTemN % ("qcd") ) for s in qcd_files  ] , DIR+"/bkgs/" )

W = SampleType("W" , kGreen - 3 , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "", treeName=TreeTemN % ("Wjets") ) for s in [DIR + "/bkgs/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root.root"] ] , DIR+"/bkgs/" )

ZG = SampleType("ZG" , kCyan+3 , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "", treeName=TreeTemN % ("ZG") ) for s in [DIR + "/bkgs/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root"] ] , DIR+"/bkgs/" )

DY = SampleType("DY" , kGreen - 3 , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "", treeName=TreeTemN % ("DY") ) for s in [DIR + "/bkgs/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root"] ] , DIR+"/bkgs/" )

ttH = SampleType( "ttH" , kGreen+2 , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=TreeTemN % ("tth_125") ) for s in [DIR + "/signals/ttHToGG_M125_13TeV_powheg_pythia8_v2.root"] ] , DIR + "/signals/" )
#TTG = SampleType( "topG", kGray , [GetSample(TTGG80), GetSample(TTGJ80) , GetSample(TGJ80)] , nTuples)
higgs_files = { DIR + "/signals/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia.root":TreeTemN % ("ggh_125"),
                DIR + "/signals/VBFHToGG_M125_13TeV_powheg_pythia8.root":TreeTemN % ("vbf_125") ,
                DIR + "/signals/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8.root":TreeTemN % ("vh_125") }

Higgs = SampleType("Higgs" , kGray ,  [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in higgs_files.items() ] , DIR + "/signals/" )

top_files = { DIR + "/bkgs/TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8.root":TreeTemN % ("ttgg"),
              DIR + "/bkgs/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.root":TreeTemN % ("tgjets"),
              DIR + "/bkgs/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8.root":TreeTemN % ("ttgjets")
}
Top_Samples = SampleType( "TopGamma" , kRed ,  [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in top_files.items() ] , DIR + "/bkgs/" , additionalCut = "( " + cutJetGamma + " || " + cutGammaGamma + " )" )

ttbar = SampleType("ttbar" , kRed-2  , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=TreeTemN % ("ttjets") ) for s in [DIR + "/bkgs/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"] ] , DIR+"/bkgs/" , additionalCut = cutJetJet )


tHw = SampleType("tHw" , kGreen+8  , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=TreeTemN % ("THw") ) for s in [DIR + "/bkgs/THW_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1.root"] ] , DIR+"/bkgs/" )
tHq = SampleType("Signal" , kYellow  , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=TreeTemN % ("THQ") ) for s in [DIR + "/bkgs/THQ_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1.root"] ] , DIR+"/bkgs/" , True )


allSTs = [ dataSamples , digSamples , gjet, jetJet , W , DY, ZG, Higgs , Top_Samples , ttbar , ttH , tHw  , tHq ]


###############  SAMPLE LIST CREATED #############

outfname = ""
normtodata = True



if len(sys.argv) < 2:
    raise RuntimeError("at least one parameter has to be given")

appendix = "all"
if len(sys.argv) > 2 :
    appendix = sys.argv[2]

if sys.argv[1] == "lumi":
    outfname = "out_fgg_%s_normtolumi.root" % appendix
    normtodata = False
elif sys.argv[1] == "data":
    outfname = "out_fgg_%s_normtodata.root" % appendix
    normtodata = True
else :
    raise RuntimeError("the first argument must be either lumi or data to set the final normalization method of the histograms")
    
    
gROOT.SetBatch(True)

            
from tHqAnalyzer.HaNaMiniAnalyzer.Plotter import *
plotter = Plotter()
for st in allSTs :
    plotter.AddSampleType( st )

Cuts = {"DiG":"(CMS_hgg_mass > 100 && CMS_hgg_mass < 180) && (diphoMVA > -0.4)",
        "atLeastTwoJets":"(n_jets >= 2)" ,  # && ((n_jets==0) )
        "atLeastThreeJets":"n_jets>2" ,
        "OneMediumB":"(n_M_bjets==1)" ,
        "MuonChannel" : "(LeptonType == 2)" ,
        "ElecChannel" : "(LeptonType == 1)" ,
        "Leptons" : "(LeptonType == 1 || LeptonType == 2)" , # && LeptonPt > 20" ,
        "NoLeptons" : "(LeptonType == 0)",
        "InvMassCut" : "( (CMS_hgg_mass < 130 ) && (CMS_hgg_mass > 120 ) )" ,
        "met" : "(MET > 30)" ,
        "BDT" : "MVA_Medium > 0 " }


cDiGLeptons = CutInfo( "Lepton" , "&&".join( [ Cuts[s] for s in [ "DiG" , "met" , "Leptons"  ] ])  , "weight" , "di#gamma + lepton selection ("+str(LUMI)+"fb^{-1})" )
cDiGLeptons.AddHist( "nVertices" , "nvtx", 10 , 0. , 40. , "#vertices" , dirName = "PlottedVars" )
cDiGLeptons.AddHist( "mGG",  "CMS_hgg_mass" , 20 , 100 , 180. , "#gamma#gamma invariant mass (GeV);#entries" , dirName = "PlottedVars")
cDiGLeptons.AddHist( "GGmva",  "diphoMVA" , 20 , -1. , 1. , "#gamma#gamma mva;#entries", dirName = "PlottedVars")
cDiGLeptons.AddHist( "maxGmva",  "((leadIDMVA>subleadIDMVA)*leadIDMVA +  (leadIDMVA<=subleadIDMVA)*subleadIDMVA)" , 10 , -1. , 1. , "max(#gamma_{1} mva,#gamma_{2} mva);#entries", dirName = "PlottedVars")
cDiGLeptons.AddHist( "minGmva",  "((leadIDMVA>subleadIDMVA)*subleadIDMVA +  (leadIDMVA<=subleadIDMVA)*leadIDMVA)" , 5 , -1. , 1. , "min(#gamma_{1} mva,#gamma_{2} mva);#entries", dirName = "PlottedVars")
cDiGLeptons.AddHist( "mGGFineBinned",  "CMS_hgg_mass" , 160 , 100 , 180. , "#gamma#gamma invariant mass (GeV);#entries", dirName = "PlottedVars")
cDiGLeptons.AddHist( "nJets" , "n_jets" , 10 , 0. , 10. , "a;#Jets;#entries" , dirName = "PlottedVars")
#cDiGLeptons.AddHist( "LepPt" , "LeptonPt",  7 , 20. , 160. , "a;Lepton p_{T} (GeV);#entries" )
cDiGLeptons.AddHist( "nbJets" , "n_M_bjets" , 5 , 0. , 5., "a;#b-tagged jets;#entries" , dirName = "PlottedVars")
met1 = cDiGLeptons.AddHist( "met" , "MET",  3 , 30. , 180. , "a;MET (GeV);#entries" , dirName = "PlottedVars")
cDiGLeptons.AddHist( "jPt" , "jet1_pt" ,  10 , 10. , 310. , "a;leading jet p_{T};#entries" , dirName = "PlottedVars")
cDiGLeptons.AddHist( "jEta" , "abs(fwdJetEta_Medium)" ,  5 , 0 , 5.0 , "a;forward jet |#eta|;#entries" , dirName = "PlottedVars")
leptT = cDiGLeptons.AddHist( "LeptonType" , "LeptonType" ,  5 , 0 , 5.0 , "a;Lepton Type;#entries" , dirName = "PlottedVars")
cDiGLeptons.AddHist("metFinnedBins1" , "MET",  100 , 0. , 500. , "a;MET (GeV);#entries" , dirName = "PlottedVars")    
plotter.AddTreePlots( cDiGLeptons )

from SamplesMoriond17.SystematicDumperDefaultVariables import defaultVariables
import SamplesMoriond17.THQLeptonicTagVariables as varthq
variablesUsed = defaultVariables + varthq.vtx_variables + varthq.dipho_variables + varthq.photon_variables + varthq.lepton_variables + varthq.jet_variables + varthq.thqmva_variables



variablesToUse = [ s.split()[0].split("[")[0].split(":")[0] for s in variablesUsed ]
AutoLimits={"CMS_hgg_mass":[10,30,230],"leadPt":[10,30,230],"subleadPt":[10,20,320],"leadEta":[10,-2.5,2.5],"subleadEta":[10,-2.5,2.5],"diphoMVA":[20,-1.0,1.0],"leadIDMVA":[20,-1,1],"subleadIDMVA":[20, -1,1],"maxEta":[10,0.0,2.5],"vtxZ":[15,-15,15],"vtxprob":[9,0.1,1],"ptbal":[10,-1.1e+02,3.9e+02],"ptasym":[10,-0.99,0.87],"logspt2":[10,-3.1,12],"p2conv":[10,0.0016,10],"nconv":[3,0,3],"vtxmva":[10,-1,1.],"vtxdz":[12,-20,1e+02],"vtx_x":[15,-1,0.5],"vtx_y":[5,0.,0.15],"vtx_z":[15,-15,15],"gv_x":[10,0,1],"gv_y":[10,0,1],"gv_z":[10,0,1],"dipho_sumpt":[20,30,430],"dipho_cosphi":[10,0.,1],"dipho_mass":[20,50,450],"dipho_pt":[20,0,400],"dipho_phi":[9,-3.15,3.15],"dipho_eta":[12,-6,6],"dipho_PtoM":[25,0.,25],"cosphi":[10,-1,1],"sigmaMrvoM":[30,0.,0.3],"sigmaMwvoM":[30,0.0,0.3],"dipho_leadPt":[36,30,3.9e+02],"dipho_leadEt":[36,30,200],"dipho_leadEta":[10,-2.5,2.5],"dipho_leadPhi":[10,-3.1,3.1],"dipho_lead_sieie":[20,0.,0.04],"dipho_lead_hoe":[10,0,0.1],"dipho_lead_sigmaEoE":[10,0.0,0.2],"dipho_lead_ptoM":[10,0.5,3.5],"dipho_leadR9":[20,0.4,1],"dipho_leadIDMVA":[20,-1,1],"dipho_lead_elveto":[2,0,2],"dipho_lead_prompt":[2,0,2],"dipho_lead_chiso":[20,-1,19],"dipho_lead_chisow":[20,-1,19],"dipho_lead_phoiso":[10,0,5],"dipho_lead_phoiso04":[10,0,5],"dipho_lead_neutiso":[10,0,10],"dipho_lead_ecaliso03":[10,0,20],"dipho_lead_hcaliso03":[10,0,20],"dipho_lead_pfcluecal03":[20,0,100],"dipho_lead_pfcluhcal03":[20,0,2e+02],"dipho_lead_trkiso03":[18,0,1.8e+02],"dipho_lead_pfchiso2":[20,-1,79],"dipho_lead_haspixelseed":[2,0,2],"dipho_lead_sieip":[18,-0.0004,0.0004],"dipho_lead_etawidth":[10,0.0031,0.057],"dipho_lead_phiwidth":[10,0.0043,0.17],"dipho_lead_regrerr":[20,0,10],"dipho_lead_s4ratio":[16,0.2,1.],"dipho_lead_effSigma":[14,0,14],"dipho_lead_scraw":[30,20,620],"dipho_lead_ese":[20,0,40],"dipho_subleadPt":[10,20,3.1e+02],"dipho_subleadEt":[10,20,3.1e+02],"dipho_subleadEta":[10,-2.5,2.5],"dipho_subleadPhi":[10,-3.1,3.1],"dipho_sublead_sieie":[10,0.00096,0.047],"dipho_sublead_hoe":[10,0,0.08],"dipho_sublead_sigmaEoE":[10,0.008,0.5],"dipho_sublead_ptoM":[10,0.25,53],"dipho_subleadR9":[10,0.2,1],"dipho_subleadIDMVA":[10,-0.9,1],"dipho_sublead_elveto":[10,1,1],"dipho_sulead_prompt":[10,0,0],"dipho_sublead_chiso":[10,-1,1e+02],"dipho_sublead_chisow":[10,-1,2.6e+02],"dipho_sublead_phoiso":[10,0,2.8e+02],"dipho_sublead_phoiso04":[10,0,2.8e+02],"dipho_sublead_neutiso":[10,0,70],"dipho_sublead_ecaliso03":[10,0,2e+02],"dipho_sublead_hcaliso03":[10,0,1.4e+02],"dipho_sublead_pfcluecal03":[10,0,2.9e+02],"dipho_sublead_pfcluhcal03":[10,0,1.7e+02],"dipho_sublead_trkiso03":[10,0,1.6e+03],"dipho_sublead_pfchiso2":[10,-1,91],"dipho_sublead_haspixelseed":[10,0,1],"dipho_sublead_sieip":[10,-0.0015,0.0015],"dipho_sublead_etawidth":[10,0.0027,0.068],"dipho_sublead_phiwidth":[10,0.0041,0.17],"dipho_sublead_regrerr":[10,0.22,59],"dipho_sublead_s4ratio":[10,0.12,0.97],"dipho_sublead_effSigma":[10,0,12],"dipho_sublead_scraw":[10,11,1.1e+03],"dipho_sublead_ese":[10,0,42],"LeptonType":[5,0,5],"n_ele":[5,0,5],"ele1_pt":[24,10,250],"ele2_pt":[10,-1e+03,27],"ele1_eta":[10,-2.5 ,2.5 ],"ele2_eta":[10,-1e+03,-0.54],"ele1_phi":[16,-3.2,3.2],"ele2_phi":[10,-1e+03,3],"ele1_ch":[3,-1,2],"ele2_ch":[10,-1e+03,-1],"ele1_sigmaIetaIeta":[20,-0.05,0.05],"ele2_sigmaIetaIeta":[10,-1e+03,0.009],"ele1_dEtaInSeed":[20,-0.01,0.01],"ele2_dEtaInSeed":[10,-1e+03,0.0015],"ele1_dPhiIn":[10,0,0.05],"ele2_dPhiIn":[10,-1e+03,-0.011],"ele1_hOverE":[15,0,0.15],"ele2_hOverE":[10,-1e+03,0],"ele1_RelIsoEA":[10,0,0.1],"ele2_RelIsoEA":[10,-1e+03,0],"ele1_ooEmooP":[10,0,0.02],"ele2_ooEmooP":[10,-1e+03,0.0019],"ele1_ConversionVeto":[2,0,2],"ele2_ConversionVeto":[10,-1e+03,1],"ele1_ChargedHadronPt":[20,0,10],"ele2_ChargedHadronPt":[10,-1e+03,0],"ele2_NeutralHadronEt":[10,0,10],"ele1_NeutralHadronEt":[10,0,10],"ele1_PhotonEt":[10,0,4],"ele2_PhotonEt":[10,-1e+03,1.1],"n_muons":[5,0,5],"muon1_pt":[16,10,1.6e+02],"muon2_pt":[10,0,100],"muon1_eta":[20,-2.5,2.5],"muon2_eta":[10,-1e+03,-1e+03],"muon1_phi":[16,-3.2,3.2],"muon2_phi":[10,-1e+03,-1e+03],"muon1_ch":[3,-1, 2],"muon2_ch":[10,-1e+03,-1e+03],"muon1_iso":[20,0,2],"muon2_iso":[10,-1e+03,-1e+03],"muon1_chi2":[10,0,3],"muon2_chi2":[10,-1e+03,-1e+03],"muon1_mHits":[30,0,30],"muon2_mHits":[10,-1e+03,-1e+03],"muon1_mStations":[5,0,5],"muon2_mStations":[10,-1e+03,-1e+03],"muon1_dxy":[40,-2 , 2],"muon2_dxy":[10,-1e+03,-1e+03],"muon1_diphodxy":[40,-2,2],"muon2_diphodxy":[10,-1e+03,-1e+03],"muon1_dz":[10, -1 , 1],"muon2_dz":[10,-1e+03,-1e+03],"muon1_diphodz":[10,-1,1],"muon2_diphodz":[10,-1e+03,-1e+03],"muon1_pxHits":[5,0,5],"muon2_pxHits":[10,-1e+03,-1e+03],"muon1_tkLayers":[15,0,15],"muon2_tkLayers":[10,-1e+03,-1e+03],"n_fwdjets":[10,0,10],"fwdjet1_pt":[20,20,220],"fwdjet2_pt":[10,-1e+03,7.1e+02],"fwdjet1_eta":[19,-4.75,4.75],"fwdjet2_eta":[10,-1e+03,3.8],"fwdjet1_phi":[16,-3.2,3.2],"fwdjet2_phi":[10,-1e+03,3.1],"n_M_bjets":[5,0,5],"n_L_bjets":[5,0,5],"n_T_bjets":[10,0,10],"n_bjets":[10,0,10],"bjet1_pt":[10,-1e+03,7.1e+02],"bjet2_pt":[10,-1e+03,5.2e+02],"bjet1_eta":[10,-1e+03,4.7],"bjet2_eta":[10,-1e+03,4.6],"bjet1_phi":[10,-1e+03,3.1],"bjet2_phi":[10,-1e+03,3.1],"n_jets":[10,0,10],"jet1_pt":[10,-1e+03,7.1e+02],"jet2_pt":[10,-1e+03,5.2e+02],"jet3_pt":[10,-1e+03,1.9e+02],"jet1_eta":[10,-1e+03,4.7],"jet2_eta":[10,-1e+03,4.6],"jet3_eta":[10,-1e+03,4.6],"jet1_phi":[10,-1e+03,3.1],"jet2_phi":[10,-1e+03,3.1],"jet3_phi":[10,-1e+03,3.1],"bTagWeight":[20,0.5,1.5],"photonWeights":[10,0.9,1.1],"FoxWolf":[5,0.0,50],"Aplanarity":[10,0,0.5],"MET":[23,0,2.3e+02],"METPhi":[16,-3.2,3.2],"fwdJetEta_HighestBTagVal":[19,-4.75,4.75],"MVA_HighestBTagVal":[10,-1,1],"bJetPt_HighestBTagVal":[25,30,2.8e+02],"fwdJetEta_Medium":[19,-4.75,4.75],"MVA_Medium":[10,-1,1],"bJetPt_Medium":[25, 30,280],"fwdJetEta_Loose":[19,-4.75,4.75],"MVA_Loose":[10,-1,1],"bJetPt_Loose":[25,30,280],"fwdJetEta_Tight":[19,-4.75,4.75],"MVA_Tight":[10,-1,1],"bJetPt_Tight":[25,30,280]
            ,"ele1_dxy":[20,-1.0,1.0],"ele2_dxy":[10,-1e+03,0.00063],"ele1_diphodxy":[20,-1,1.0],"ele2_diphodxy":[10,-1e+03,0.00063],"ele1_dz":[12,-0.6,0.6],"ele2_dz":[10,-1e+03,0.0013],"ele1_diphodz":[12,-0.6,0.6],"ele2_diphodz":[10,-1e+03,0.0013],"ele1_misHits":[6,0,6],"ele2_misHits":[10,-1e+03,0],"ele1_PassTight":[2 , 0, 2],"ele2_PassTight":[10,-1e+03,1],"ele1_PassIso":[2,0,2],"ele2_PassIso":[10,-1e+03,1],"muon1_PassTight":[2 , 0, 2],"muon2_PassTight":[10,-1e+03,-1e+03]}

cDiGLeptons2j1t = CutInfo( "Lepton2J1T" , "&&".join( [ Cuts[s] for s in ["DiG" , "atLeastTwoJets" , "OneMediumB" , "met", "Leptons"] ] ) , "bTagWeight*weight" , "2J1T + Lepton + di#gamma ("+str(LUMI)+"fb^{-1})"  )
for var_ in variablesUsed:
    var = var_.split()[0].split("[")[0].split(":")[0]
    title = var_.split("=")[-1]
    if var in AutoLimits:
        nbins = AutoLimits[var][0]
        from_ = AutoLimits[var][1]
        to = AutoLimits[var][2]
        if from_ == -100.00:
            from_ = -1*to
        elif from_ == -1000:
            from_ = 0

        dirName = var.split("_")[0]
        if var_ in varthq.vtx_variables :
            dirName = "Vertex"
        elif var_ in varthq.dipho_variables:
            dirName = "DiPhoton"
        elif "_lead" in var:
            dirName = "LeadinPhoton"
        elif "_sublea" in var :
            leadingone = AutoLimits[ var.replace("_sublead" , "_lead") ]
            nbins = leadingone[0]
            from_ = leadingone[1]
            to = leadingone[2]
            dirName = "SubLeadingPhoton"
        elif var_ in varthq.thqmva_variables:
            dirName = "THQ"
        elif dirName == var :
            dirName = "Others"
        if var_ in defaultVariables:
            dirName = "Basics"

        theOtherOne = None
        theOtherTag = ""
        if dirName == "ele2" :
            theOtherTag="ele1"
        elif dirName == "muon2":
            theOtherTag = "muon1"
        elif dirName == "fwdjet2" or dirName == "bjet1" or dirName == "bjet2" or dirName == "jet1" or dirName == "jet2" or dirName == "jet3":            
            theOtherTag = "fwdjet1"
            
        if not theOtherTag == "":
            theOtherOne = AutoLimits[ var.replace(dirName , theOtherTag) ]            
            nbins = theOtherOne[0]
            from_ = theOtherOne[1]
            to = theOtherOne[2]
            
        name = var.replace("_" , "")

        cDiGLeptons.AddHist( name , var , nbins , from_ , to , Title=title , dirName = dirName )
        cDiGLeptons2j1t.AddHist( name , var , nbins , from_ , to , Title=title , dirName = dirName )
    else:
        print "{0:s} does not exist in the AutoLimit collection and will be treated as Automatic variable".format( var )
        cDiGLeptons.AddHist(var , var , 10 , Auto = True , Title=title)
        #cDiGLeptons2j1t.AddHist(var , var , 10 , Auto = True , Title=title)
        
cDiG = CutInfo( "DiG" , "&&".join( [ Cuts[s] for s in ["DiG","met"] ] ) , "weight" , "di#gamma + met cut ("+str(LUMI)+"fb^{-1})" )
for h in cDiGLeptons.ListOfHists:
    cDiG.AddHist( h )

    
plotter.AddTreePlots( cDiG )


cDiGNoLeptons = CutInfo( "DiGNoLeptons" , "&&".join( [ Cuts[s] for s in ["DiG" , "NoLeptons" , "met"] ] )   , "weight" , "di#gamma + lepton veto ("+str(LUMI)+"fb^{-1})" )
for h in cDiGLeptons.ListOfHists:
    cDiGNoLeptons.AddHist( h )

plotter.AddTreePlots( cDiGNoLeptons )


#cut2J1T = " && " + Cuts["atLeastTwoJets"] + " && " + Cuts["OneMediumB"]  + " && " + Cuts["met"] 
cDiG2J1T = CutInfo( "DiG2J1T" , "&&".join( [ Cuts[s] for s in ["DiG" , "atLeastTwoJets" , "OneMediumB" , "met"] ] ), "bTagWeight*weight" , "di#gamma + 2J1T selection ("+str(LUMI)+"fb^{-1})" )
for h in cDiGLeptons.ListOfHists:
    cDiG2J1T.AddHist( h )
cDiG2J1T.AddHist( met1 , leptT )
plotter.AddTreePlots( cDiG2J1T )

cDiGEle = CutInfo( "Electron" , "&&".join( [ Cuts[s] for s in [ "DiG" , "ElecChannel" , "met"] ] ), "weight" , "di#gamma, exactly one electron ("+str(LUMI)+"fb^{-1})" )
for h in cDiGLeptons.ListOfHists:
    cDiGEle.AddHist( h )
plotter.AddTreePlots( cDiGEle )

cDiGMu = CutInfo( "Muon" , "&&".join( [ Cuts[s] for s in ["DiG" , "MuonChannel" , "met"] ] )  , "weight"  , "di#gamma, exactly one #mu ("+str(LUMI)+"fb^{-1})" )
for h in cDiGLeptons.ListOfHists:
    cDiGMu.AddHist( h )
plotter.AddTreePlots( cDiGMu )


#cDiGLeptons2j1t.AddHist( "TopMass",  "topMass" , 40 , 100 , 300 , "Reconstructed top mass")
cDiGLeptons2j1t.AddHist( "Aplanarity",  "Aplanarity" , 10 , 0 , 0.4 , "aplanarity" , dirName = "PlottedVars")
cDiGLeptons2j1t.AddHist( "met" , "MET",  3 , 30. , 180. , "met (GeV)" , dirName = "PlottedVars")
cDiGLeptons2j1t.AddHist( "jprimeeta" , "abs(fwdJetEta_Medium)" , 5 , 0 , 5 , "forward jet |#eta|" , dirName = "PlottedVars")
cDiGLeptons2j1t.AddHist( "maxGmva",  "((leadIDMVA>subleadIDMVA)*leadIDMVA +  (leadIDMVA<=subleadIDMVA)*subleadIDMVA)" , 20 , -1. , 1. , "max(#gamma_{1} mva,#gamma_{2} mva);#entries", dirName = "PlottedVars")
cDiGLeptons2j1t.AddHist( "minGmva",  "((leadIDMVA>subleadIDMVA)*subleadIDMVA +  (leadIDMVA<=subleadIDMVA)*leadIDMVA)" , 20 , -1. , 1. , "min(#gamma_{1} mva,#gamma_{2} mva);#entries", dirName = "PlottedVars")

BDThist  = cDiGLeptons2j1t.AddHist( "BDT",  "MVA_Medium" , 2 , -1.1 ,1.1 , "BDT output" , dirName = "PlottedVars")
mGGhist = cDiGLeptons2j1t.AddHist( "mGG",  "CMS_hgg_mass" , 60 , 100. , 400. , "#gamma#gamma invariant mass (GeV)" , dirName = "PlottedVars" )
cDiGLeptons2j1t.AddHist( "GGmva",  "diphoMVA" , 20 , -1. , 1. , "#gamma#gamma mva;#entries", dirName = "PlottedVars")

plotter.AddTreePlots( cDiGLeptons2j1t )

cutFinal = "&&".join( [ Cuts[s] for s in ["DiG" , "atLeastTwoJets" , "OneMediumB" , "met", "Leptons" , "BDT"] ] )
#cutFinal = Cuts["DiG"] + " && " + Cuts["Leptons"] +  " && " + Cuts["BDT"] + cut2J1T
print cutFinal
cDiGLeptons2j1tBDT = CutInfo( "Lepton2J1TBDT" , cutFinal  , "bTagWeight*weight" , "BDT Cut ("+str(LUMI)+"fb^{-1})" )
for h in cDiGLeptons2j1t.ListOfHists:
    cDiGLeptons2j1tBDT.AddHist( h )
cDiGLeptons2j1tBDT.AddHist( mGGhist, BDThist )
plotter.AddTreePlots( cDiGLeptons2j1tBDT )

cDiGLeptons2j1t.AddHist( mGGhist, BDThist )


plotter.LoadHistos( LUMI  , "thqLeptonicTagDumper/" ) #

fout = TFile.Open( outfname , "recreate")

plotter.Write(fout, normtodata)

    
fout.Close()

