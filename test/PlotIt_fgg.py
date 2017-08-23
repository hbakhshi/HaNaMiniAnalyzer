#!/usr/bin/env python
############MAKE SAMPLE LIST : ###################

LUMI = 35.9

import os
import os.path
import math
import sys
import glob
from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *
from tHqAnalyzer.HaNaMiniAnalyzer.SampleType import *
Sample.WD = os.path.dirname(os.path.abspath(__file__))
from ROOT import kAzure, kGray, kGreen, kYellow, kOrange, kRed, kBlack, kCyan, kBlue, gROOT, TLatex, TCanvas, TFile, TColor, TSystem

TreeTemN = "tagsDumper/trees/%s_13TeV_THQLeptonicTag"
DIR="/home/hbakhshi/Downloads/tHq_Georgios/output/14_07_17/"

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
digSamples = SampleType("DiGamma" , kOrange , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName = t  ) for s,t in digamma_files.items() ] , DIR+"/bkgs/" , additionalCut = cutGammaGamma )

colorPhotons = TColor.GetColor("#ffcc00")
incPhotonSamples = SampleType( "Photons" , colorPhotons , [] , "" , False , None )
for s in digSamples.Samples :
    incPhotonSamples.Samples.append( s )
for s in jetJet.Samples :
    incPhotonSamples.Samples.append( s )
for s in gjet.Samples :
    incPhotonSamples.Samples.append( s )

BosonFiles = { DIR + "/bkgs/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" : TreeTemN % ("Wjets") ,
               DIR + "/bkgs/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root" : TreeTemN % ("ZG"),
               DIR + "/bkgs/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root" : TreeTemN % ("DY") }
colorBosons = kGreen+2
bosonsSamples = SampleType( "VectorBosons" , colorBosons , [Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in BosonFiles.items()] , DIR+"/bkgs/" )

ttHcolor = kRed
ttHSamples = { DIR + "signals/THW.root" : "thw_125" ,
              DIR + "signals/TTH.root" : "tth_125" }
ttH = SampleType( "ttH+tHW" , ttHcolor , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=TreeTemN % (t) ) for s,t in ttHSamples.items()  ] , DIR + "/signals/" )

higgs_files = { DIR + "/signals/GGH.root":TreeTemN % ("ggh_125"),
                DIR + "/signals/VBF.root":TreeTemN % ("vbf_125") ,
                DIR + "/signals/VH.root":TreeTemN % ("vh_125") }
higgsColor = kBlue
Higgs = SampleType("OtherHiggs" , higgsColor ,  [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in higgs_files.items() ] , DIR + "/signals/" )

top_files = {
    #DIR + "/bkgs/TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8.root":TreeTemN % ("ttgg"),
    #DIR + "/bkgs/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.root":TreeTemN % ("tgjets"),
    DIR + "/bkgs/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8.root":TreeTemN % ("tgjets"),
    DIR + "/bkgs/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" : TreeTemN % ("TTJet") 
}
colorTop = TColor.GetColor("#993333")
Top_Samples = SampleType( "Top" , colorTop ,  [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in top_files.items() ] , DIR + "/bkgs/" ) 


tHSamples = { DIR + "signals/THQ.root" : "thq_125" }
tH = SampleType("tHq" , kCyan+4 , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=TreeTemN % (t) ) for s,t in tHSamples.items() ] , DIR+"/signals/"   )

allSTs = [ dataSamples , tH, ttH , Higgs , bosonsSamples ,  incPhotonSamples ,  Top_Samples]
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

ELECTRON_CHANNEL = "(n_loose_ele == 1 && n_TightMu15 == 0)" #"(LeptonType == 1)" ,
MUON_CHANNEL     = "(n_LooseMu25 == 1 && n_tight_ele == 0)" #"(LeptonType == 2)" ,
Cuts = {"DiG":"(CMS_hgg_mass > 100 && CMS_hgg_mass < 180) && (diphoMVA > -0.4)",
        "atLeastTwoJets":"(n_jets >= 2)" ,  # && ((n_jets==0) )
        "atLeastThreeJets":"n_jets>2" ,
        "OneMediumB":"(n_M_bjets==1)" ,
        "TwoMediumB":"(n_M_bjets==2)" ,
        "MuonChannel" : MUON_CHANNEL ,
        "ElecChannel" : ELECTRON_CHANNEL,
        "Leptons" : "(%s || %s)" % ( ELECTRON_CHANNEL , MUON_CHANNEL  ),
        "NoLeptons" : "!(%s || %s)" % ( ELECTRON_CHANNEL , MUON_CHANNEL  ),
        "InvMassCut" : "( (CMS_hgg_mass < 130 ) && (CMS_hgg_mass > 120 ) )" ,
        "met" : "(MET_pt > 30)" ,
        "BDT" : "MVA_Medium > 0 ",
        "CRLeptons" : "(n_muons > 0 || n_ele > 0 ) && !(%s || %s)" % ( ELECTRON_CHANNEL , MUON_CHANNEL  ),
        "CRRelaxLeptonVeto" : "(n_muons > 0 || n_ele > 0 ) && !(%s || %s)" % ( ELECTRON_CHANNEL , MUON_CHANNEL  ),
        "EtaJP_NJ" : "( abs(fwdjet1_eta) > 2.5 && n_jets == 2 )",
        "EtaJP_NbJ" :"( abs(fwdjet1_eta) > 2.5 && n_L_bjets == 1 )" ,
        "NJ_NbJ" : "(n_jets == 2 && n_L_bjets == 1)" ,
        "NJ_NbJ_EtaJP" : "(n_jets == 2 && n_L_bjets == 1 && abs(fwdjet1_eta) > 2.5)",
        "InMassWindow":"( CMS_hgg_mass > 122 && CMS_hgg_mass < 128 )"}



cDiGLeptons = CutInfo( "DiGLeptons" , "&&".join( [ Cuts[s] for s in ["DiG","met","Leptons"] ] ) , "weight" , "di#gamma + 1lepton ("+str(LUMI)+"fb^{-1})" )
#cDiGNoLeptons = CutInfo( "DiGNoLeptons" , "&&".join( [ Cuts[s] for s in ["DiG" , "NoLeptons" , "met"] ] )   , "weight" , "di#gamma + lepton veto ("+str(LUMI)+"fb^{-1})" )
cDiGEle = CutInfo( "Electron" , "&&".join( [ Cuts[s] for s in [ "DiG" , "ElecChannel" , "met"] ] ), "weight" , "di#gamma + exactly one electron ("+str(LUMI)+"fb^{-1})" )
cDiGMu = CutInfo( "Muon" , "&&".join( [ Cuts[s] for s in ["DiG" , "MuonChannel" , "met"] ] )  , "weight"  , "di#gamma + exactly one #mu ("+str(LUMI)+"fb^{-1})" )
cDiG2J = CutInfo( "DiG2JLeptons" , "&&".join( [ Cuts[s] for s in [ "DiG" , "met" , "Leptons" , "atLeastTwoJets" ] ])  , "weight" , "di#gamma + 2Jets + 1Lepton ("+str(LUMI)+"fb^{-1})" )
cDiG2J1T = CutInfo( "DiG2J1TLeptons" , "&&".join( [ Cuts[s] for s in ["DiG" , "Leptons" , "atLeastTwoJets" , "OneMediumB" , "met"] ] ), "bTagWeight*weight" , "di#gamma + 2J1T + 1Lepton ("+str(LUMI)+"fb^{-1})" )
cDiG2J1TInMassWindow = CutInfo( "DiG2J1TLeptonsInMassWindow" , "&&".join( [ Cuts[s] for s in ["DiG" , "Leptons" , "atLeastTwoJets" , "OneMediumB" , "met" , "InMassWindow"] ] ), "bTagWeight*weight" , "di#gamma + 2J1T + 1Lepton ("+str(LUMI)+"fb^{-1})" )
allCuts = [ cDiGLeptons , cDiG2J1T , cDiG2J  , cDiGEle, cDiGMu , cDiG2J1TInMassWindow ] #, cDiGNoLeptons

for cut in allCuts :
    cut.AddHist( "nVertices" , "nvtx", 10 , 0. , 40. , "#vertices" , dirName = "PlottedVars" )
    cut.AddHist( "mGG",  "CMS_hgg_mass" , 20 , 100 , 180. , "#gamma#gamma invariant mass (GeV);#entries" , dirName = "PlottedVars")
    cut.AddHist( "GGmva",  "diphoMVA" , 20 , -1. , 1. , "#gamma#gamma mva;#entries", dirName = "PlottedVars")
    cut.AddHist( "maxGmva",  "((leadIDMVA>subleadIDMVA)*leadIDMVA +  (leadIDMVA<=subleadIDMVA)*subleadIDMVA)" , 10 , -1. , 1. , "max(#gamma_{1} mva,#gamma_{2} mva);#entries", dirName = "PlottedVars")
    cut.AddHist( "minGmva",  "((leadIDMVA>subleadIDMVA)*subleadIDMVA +  (leadIDMVA<=subleadIDMVA)*leadIDMVA)" , 5 , -1. , 1. , "min(#gamma_{1} mva,#gamma_{2} mva);#entries", dirName = "PlottedVars")
    cut.AddHist( "mGGFineBinned",  "CMS_hgg_mass" , 160 , 100 , 180. , "#gamma#gamma invariant mass (GeV);#entries", dirName = "PlottedVars")
    cut.AddHist( "nJets" , "n_jets" , 10 , 0. , 10. , "#Jets;#entries" , dirName = "PlottedVars")
    #cDiGLeptons.AddHist( "LepPt" , "LeptonPt",  7 , 20. , 160. , "Lepton p_{T} (GeV);#entries" )
    cut.AddHist( "nbJets" , "n_M_bjets" , 5 , 0. , 5., "#b-tagged jets;#entries" , dirName = "PlottedVars")
    met1 = cut.AddHist( "met" , "MET_pt",  3 , 30. , 180. , "MET (GeV);#entries" , dirName = "PlottedVars")
    cut.AddHist( "jPt" , "jet1_pt" ,  10 , 10. , 310. , "leading jet p_{T};#entries" , dirName = "PlottedVars")
    cut.AddHist( "jEta" , "abs(fwdjet1_eta)" ,  5 , 0 , 5.0 , "forward jet |#eta|;#entries" , dirName = "PlottedVars")
    leptT = cut.AddHist( "LeptonType" , "LeptonType" ,  5 , 0 , 5.0 , "Lepton Type;#entries" , dirName = "PlottedVars")
    cut.AddHist("metFinnedBins1" , "MET_pt",  100 , 0. , 500. , "MET (GeV);#entries" , dirName = "PlottedVars")    

from SamplesMoriond17.SystematicDumperDefaultVariables import defaultVariables
import SamplesMoriond17.THQLeptonicTagVariables as varthq
variablesUsed = defaultVariables + varthq.vtx_variables + varthq.dipho_variables + varthq.photon_variables + varthq.lepton_variables + varthq.jet_variables + varthq.thqmva_variables + varthq.truth_variables

variablesToUse = [ s.split()[0].split("[")[0].split(":")[0] for s in variablesUsed ]
AutoLimits={"CMS_hgg_mass":[10,30,230],"leadPt":[10,30,230],"subleadPt":[10,20,320],"leadEta":[10,-2.5,2.5],"subleadEta":[10,-2.5,2.5],"diphoMVA":[20,-1.0,1.0],"leadIDMVA":[20,-1,1],"subleadIDMVA":[20, -1,1],"maxEta":[10,0.0,2.5],"vtxZ":[15,-15,15],"vtxprob":[9,0.1,1],"ptbal":[10,-1.1e+02,3.9e+02],"ptasym":[10,-0.99,0.87],"logspt2":[10,-3.1,12],"p2conv":[10,0.0016,10],"nconv":[3,0,3],"vtxmva":[10,-1,1.],"vtxdz":[12,-20,1e+02],"vtx_x":[15,-1,0.5],"vtx_y":[5,0.,0.15],"vtx_z":[15,-15,15],"gv_x":[10,0,1],"gv_y":[10,0,1],"gv_z":[10,0,1],"dipho_sumpt":[20,30,430],"dipho_cosphi":[10,0.,1],"dipho_mass":[20,50,450],"dipho_pt":[20,0,400],"dipho_phi":[9,-3.15,3.15],"dipho_eta":[12,-6,6],"dipho_PtoM":[25,0.,25],"cosphi":[10,-1,1],"sigmaMrvoM":[30,0.,0.3],"sigmaMwvoM":[30,0.0,0.3],"dipho_leadPt":[36,30,3.9e+02],"dipho_leadEt":[36,30,200],"dipho_leadEta":[10,-2.5,2.5],"dipho_leadPhi":[10,-3.1,3.1],"dipho_lead_sieie":[20,0.,0.04],"dipho_lead_hoe":[10,0,0.1],"dipho_lead_sigmaEoE":[10,0.0,0.2],"dipho_lead_ptoM":[10,0.5,3.5],"dipho_leadR9":[20,0.4,1],"dipho_leadIDMVA":[20,-1,1],"dipho_lead_elveto":[2,0,2],"dipho_lead_prompt":[2,0,2],"dipho_lead_chiso":[20,-1,19],"dipho_lead_chisow":[20,-1,19],"dipho_lead_phoiso":[10,0,5],"dipho_lead_phoiso04":[10,0,5],"dipho_lead_neutiso":[10,0,10],"dipho_lead_ecaliso03":[10,0,20],"dipho_lead_hcaliso03":[10,0,20],"dipho_lead_pfcluecal03":[20,0,100],"dipho_lead_pfcluhcal03":[20,0,2e+02],"dipho_lead_trkiso03":[18,0,1.8e+02],"dipho_lead_pfchiso2":[20,-1,79],"dipho_lead_haspixelseed":[2,0,2],"dipho_lead_sieip":[18,-0.0004,0.0004],"dipho_lead_etawidth":[10,0.0031,0.057],"dipho_lead_phiwidth":[10,0.0043,0.17],"dipho_lead_regrerr":[20,0,10],"dipho_lead_s4ratio":[16,0.2,1.],"dipho_lead_effSigma":[14,0,14],"dipho_lead_scraw":[30,20,620],"dipho_lead_ese":[20,0,40],"dipho_subleadPt":[10,20,3.1e+02],"dipho_subleadEt":[10,20,3.1e+02],"dipho_subleadEta":[10,-2.5,2.5],"dipho_subleadPhi":[10,-3.1,3.1],"dipho_sublead_sieie":[10,0.00096,0.047],"dipho_sublead_hoe":[10,0,0.08],"dipho_sublead_sigmaEoE":[10,0.008,0.5],"dipho_sublead_ptoM":[10,0.25,53],"dipho_subleadR9":[10,0.2,1],"dipho_subleadIDMVA":[10,-0.9,1],"dipho_sublead_elveto":[10,1,1],"dipho_sulead_prompt":[10,0,0],"dipho_sublead_chiso":[10,-1,1e+02],"dipho_sublead_chisow":[10,-1,2.6e+02],"dipho_sublead_phoiso":[10,0,2.8e+02],"dipho_sublead_phoiso04":[10,0,2.8e+02],"dipho_sublead_neutiso":[10,0,70],"dipho_sublead_ecaliso03":[10,0,2e+02],"dipho_sublead_hcaliso03":[10,0,1.4e+02],"dipho_sublead_pfcluecal03":[10,0,2.9e+02],"dipho_sublead_pfcluhcal03":[10,0,1.7e+02],"dipho_sublead_trkiso03":[10,0,1.6e+03],"dipho_sublead_pfchiso2":[10,-1,91],"dipho_sublead_haspixelseed":[10,0,1],"dipho_sublead_sieip":[10,-0.0015,0.0015],"dipho_sublead_etawidth":[10,0.0027,0.068],"dipho_sublead_phiwidth":[10,0.0041,0.17],"dipho_sublead_regrerr":[10,0.22,59],"dipho_sublead_s4ratio":[10,0.12,0.97],"dipho_sublead_effSigma":[10,0,12],"dipho_sublead_scraw":[10,11,1.1e+03],"dipho_sublead_ese":[10,0,42],"LeptonType":[5,0,5],"n_ele":[5,0,5],"ele1_pt":[24,10,250],"ele2_pt":[10,-1e+03,27],"ele1_eta":[10,-2.5 ,2.5 ],"ele2_eta":[10,-1e+03,-0.54],"ele1_phi":[16,-3.2,3.2],"ele2_phi":[10,-1e+03,3],"ele1_ch":[3,-1,2],"ele2_ch":[10,-1e+03,-1],"ele1_sigmaIetaIeta":[20,-0.05,0.05],"ele2_sigmaIetaIeta":[10,-1e+03,0.009],"ele1_dEtaInSeed":[20,-0.01,0.01],"ele2_dEtaInSeed":[10,-1e+03,0.0015],"ele1_dPhiIn":[10,0,0.05],"ele2_dPhiIn":[10,-1e+03,-0.011],"ele1_hOverE":[15,0,0.15],"ele2_hOverE":[10,-1e+03,0],"ele1_RelIsoEA":[10,0,0.1],"ele2_RelIsoEA":[10,-1e+03,0],"ele1_ooEmooP":[10,0,0.02],"ele2_ooEmooP":[10,-1e+03,0.0019],"ele1_ConversionVeto":[2,0,2],"ele2_ConversionVeto":[10,-1e+03,1],"ele1_ChargedHadronPt":[20,0,10],"ele2_ChargedHadronPt":[10,-1e+03,0],"ele2_NeutralHadronEt":[10,0,10],"ele1_NeutralHadronEt":[10,0,10],"ele1_PhotonEt":[10,0,4],"ele2_PhotonEt":[10,-1e+03,1.1],"n_muons":[5,0,5],"muon1_pt":[16,10,1.6e+02],"muon2_pt":[10,0,100],"muon1_eta":[20,-2.5,2.5],"muon2_eta":[10,-1e+03,-1e+03],"muon1_phi":[16,-3.2,3.2],"muon2_phi":[10,-1e+03,-1e+03],"muon1_ch":[3,-1, 2],"muon2_ch":[10,-1e+03,-1e+03],"muon1_iso":[20,0,2],"muon2_iso":[10,-1e+03,-1e+03],"muon1_chi2":[10,0,3],"muon2_chi2":[10,-1e+03,-1e+03],"muon1_mHits":[30,0,30],"muon2_mHits":[10,-1e+03,-1e+03],"muon1_mStations":[5,0,5],"muon2_mStations":[10,-1e+03,-1e+03],"muon1_dxy":[40,-2 , 2],"muon2_dxy":[10,-1e+03,-1e+03],"muon1_diphodxy":[40,-2,2],"muon2_diphodxy":[10,-1e+03,-1e+03],"muon1_dz":[10, -1 , 1],"muon2_dz":[10,-1e+03,-1e+03],"muon1_diphodz":[10,-1,1],"muon2_diphodz":[10,-1e+03,-1e+03],"muon1_pxHits":[5,0,5],"muon2_pxHits":[10,-1e+03,-1e+03],"muon1_tkLayers":[15,0,15],"muon2_tkLayers":[10,-1e+03,-1e+03],"n_fwdjets":[10,0,10],"fwdjet1_pt":[20,20,220],"fwdjet2_pt":[10,-1e+03,7.1e+02],"fwdjet1_eta":[19,-4.75,4.75],"fwdjet2_eta":[10,-1e+03,3.8],"fwdjet1_phi":[16,-3.2,3.2],"fwdjet2_phi":[16,-3.2,3.2],"n_M_bjets":[5,0,5],"n_L_bjets":[5,0,5],"n_T_bjets":[10,0,10],"n_bjets":[10,0,10],"bjet1_pt":[20,20,220],"bjet2_pt":[10,-1e+03,5.2e+02],"bjet1_eta":[19,-4.75,4.75],"bjet2_eta":[10,-1e+03,4.6],"bjet1_phi":[16,-3.2,3.2],"bjet2_phi":[10,-1e+03,3.1],"n_jets":[10,0,10],"jet1_pt":[10,-1e+03,7.1e+02],"jet2_pt":[10,-1e+03,5.2e+02],"jet3_pt":[10,-1e+03,1.9e+02],"jet1_eta":[10,-1e+03,4.7],"jet2_eta":[10,-1e+03,4.6],"jet3_eta":[10,-1e+03,4.6],"jet1_phi":[10,-1e+03,3.1],"jet2_phi":[10,-1e+03,3.1],"jet3_phi":[10,-1e+03,3.1],"bTagWeight":[20,0.5,1.5],"photonWeights":[10,0.9,1.1],"FoxWolf":[5,0.0,50],"Aplanarity":[10,0,0.5],"MET_pt":[23,0,2.3e+02],"METPhi":[16,-3.2,3.2],"fwdJetEta_HighestBTagVal":[19,-4.75,4.75],"MVA_HighestBTagVal":[10,-1,1],"bJetPt_HighestBTagVal":[25,30,2.8e+02],"fwdJetEta_Medium":[19,-4.75,4.75],"MVA_Medium":[10,-1,1],"bJetPt_Medium":[25, 30,280],"fwdJetEta_Loose":[19,-4.75,4.75],"MVA_Loose":[10,-1,1],"bJetPt_Loose":[25,30,280],"fwdJetEta_Tight":[19,-4.75,4.75],"MVA_Tight":[10,-1,1],"bJetPt_Tight":[25,30,280],"ele1_dxy":[20,-1.0,1.0],"ele2_dxy":[10,-1e+03,0.00063],"ele1_diphodxy":[20,-1,1.0],"ele2_diphodxy":[10,-1e+03,0.00063],"ele1_dz":[12,-0.6,0.6],"ele2_dz":[10,-1e+03,0.0013],"ele1_diphodz":[12,-0.6,0.6],"ele2_diphodz":[10,-1e+03,0.0013],"ele1_misHits":[6,0,6],"ele2_misHits":[10,-1e+03,0],"ele1_PassTight":[2 , 0, 2],"ele2_PassTight":[10,-1e+03,1],"ele1_PassIso":[2,0,2],"ele2_PassIso":[10,-1e+03,1],"muon1_PassTight":[2 , 0, 2],"muon2_PassTight":[10,-1e+03,-1e+03],"dipho_e" : [10 , 0 , 200 ] ,"n_loose_ele":[5 , 0 , 5 ], "n_veto_ele":[5 , 0 , 5 ], "n_medium_ele":[5, 0 , 5], "n_tight_ele":[5 , 0 , 5] , "ele1_e":[10 , 0 , 200 ] , "ele2_e":[10 , 0 , 200] ,"ele1_PassVeto":[2 , 0 , 2 ] , "ele2_PassVeto":[2,0,2] , "ele1_dPhiMET":[32 , -3.2 , 3.2], "ele2_dPhiMET":[32 , -3.2 , 3.2], "n_LooseMu25":[5 , 0 , 5] , "n_LooseMu15":[5, 0 , 5 ],"n_TightMu25":[5,0,5],"n_TightMu15":[5,0,5],"n_MediumMu25":[5,0,5],"n_MediumMu15":[5,0,5],"muon1_e":[10,0,20],"muon2_e":[10,0,20],"muon1_dPhiMET":[32,-3.2,3.2], "muon2_dPhiMET":[32,-3.2,3.2] , "fwdjet3_pt":[20,20,220], "fwdjet3_eta":[19,-4.75,4.75],"fwdjet3_phi":[16,-3.2,3.2] , "fwdjet1_e":[10 , 0 , 200 ],"fwdjet2_e":[10 , 0 , 200 ],"fwdjet3_e":[10 , 0 , 200 ],"bjet3_pt":[10 , 0 , 200],"bjet3_eta":[10 , -5 , 5],"bjet3_phi":[32, -3.2,3.2],"bjet1_e":[10 , 0 , 200], "bjet2_e":[10,0,200], "bjet3_e":[10,0,200],"bjet1_discr":[20 , 0 , 1],"bjet2_discr":[20,-1,1],"bjet3_discr":[20,-1,1], "jet1_e":[20,0,200], "jet2_e":[20,0,200],"jet3_e":[20,0,200],"recoMET_pt":[20, 0 , 300],"recoMET_eta":[20,-5,5],"recoMET_phi":[32,-3.2,3.2],"recoMET_e":[20,0,200],"solvedMET_pt":[20,0,200],"solvedMET_eta":[20,-5,5],"solvedMET_phi":[32,-3.2,3.2], "solvedMET_e":[20 , 0 , 200], "HT":[30,0,300] , "bTagWeightUp":[10 , -1 , 9],"bTagWeightDown":[10,-1, 9],"MET_phi":[32,-3.2,3.2]}

TruthVars = {"Photon1_J1_dR":[10,0,5],"Photon1_J2_dR":[10,0,5],"Photon1_J3_dR":[10,0,5],"Photon2_J1_dR":[10,0,5],"Photon2_J2_dR":[10,0,5],"Photon2_J3_dR":[10,0,5],"dRToNearestPartonJ1":[10,0,5],"dRToNearestPartonJ2":[10,0,5],"dRToNearestPartonJ3":[10,0,5],"numberOfLSSMatches":[10,0,10],"numberOfLSMatches":[10,0,10],"numberOfLMatches":[10,0,10],"genJetMatchingToJ1_pt":[10,0,200],"genJetMatchingToJ2_pt":[10,0,200],"genJetMatchingToJ3_pt":[10,0,200],"genJetMatchingToJ1_eta":[20,-5,5],"genJetMatchingToJ2_eta":[20,-5,5],"genJetMatchingToJ3_eta":[20,-5,5],"genJetMatchingToJ1_phi":[32,-3.2,3.2],"genJetMatchingToJ2_phi":[32,-3.2,3.2],"genJetMatchingToJ3_phi":[32,-3.2,3.2],"genJetMatchingToJ1_e":[10,0,200],"genJetMatchingToJ2_e":[10,0,200],"genJetMatchingToJ3_e":[10,0,200],"partonMatchingToJ1_pt":[10,0,200],"partonMatchingToJ2_pt":[10,0,200],"partonMatchingToJ3_pt":[10,0,200],"partonMatchingToJ1_eta":[20,-5,5],"partonMatchingToJ2_eta":[20,-5,5],"partonMatchingToJ3_eta":[20,-5,5],"partonMatchingToJ1_phi":[32,-3.2,3.2],"partonMatchingToJ2_phi":[32,-3.2,3.2],"partonMatchingToJ3_phi":[32,-3.2,3.2],"partonMatchingToJ1_e":[10,0,200],"partonMatchingToJ2_e":[10,0,200],"partonMatchingToJ3_e":[10,0,200],"genParticleMatchingToLeadingMuon_pt":[10,0,200],"genParticleMatchingToSubLeadingMuon_pt":[10,0,200],"genParticleMatchingToLeadingMuon_eta":[24,-6,6],"genParticleMatchingToSubLeadingMuon_eta":[24,-6,6],"genParticleMatchingToLeadingMuon_phi":[32,-3.2,3.2],"genParticleMatchingToSubLeadingMuon_phi":[32,-3.2,3.2],"genParticleMatchingToLeadingMuon_e":[10,0,200],"genParticleMatchingToSubLeadingMuon_e":[10,0,200],"genParticleMatchingToLeadingElectron_pt":[10,0,200],"genParticleMatchingToSubLeadingElectron_pt":[10,0,200],"genParticleMatchingToLeadingElectron_eta":[20,-5,5],"genParticleMatchingToSubLeadingElectron_eta":[20,-5,5],"genParticleMatchingToLeadingElectron_phi":[32,-3.2,3.2],"genParticleMatchingToSubLeadingElectron_phi":[32,-3.2,3.2],"genParticleMatchingToLeadingElectron_e":[10,0,200],"genParticleMatchingToSubLeadingElectron_e":[10,0,200],"genPromptParticleMatchingToLeadingMuon_pt":[10,0,200],"genPromptParticleMatchingToSubLeadingMuon_pt":[10,0,200],"genPromptParticleMatchingToLeadingMuon_eta":[20,-5,5],"genPromptParticleMatchingToSubLeadingMuon_eta":[20,-5,5],"genPromptParticleMatchingToLeadingMuon_phi":[32,-3.2,3.2],"genPromptParticleMatchingToSubLeadingMuon_phi":[32,-3.2,3.2],"genPromptParticleMatchingToLeadingMuon_e":[10,0,200],"genPromptParticleMatchingToSubLeadingMuon_e":[10,0,200],"genPromptParticleMatchingToLeadingElectron_pt":[10,0,200],"genPromptParticleMatchingToSubLeadingElectron_pt":[10,0,200],"genPromptParticleMatchingToLeadingElectron_eta":[20,-5,5],"genPromptParticleMatchingToSubLeadingElectron_eta":[20,-5,5],"genPromptParticleMatchingToLeadingElectron_phi":[32,-3.2,3.2],"genPromptParticleMatchingToSubLeadingElectron_phi":[32,-3.2,3.2],"genPromptParticleMatchingToLeadingElectron_e":[10,0,200],"genPromptParticleMatchingToSubLeadingElectron_e":[10,0,200],"genMET_pt":[10,0,200],"genMET_eta":[10,-5,5],"genMET_phi":[32,-3.2,3.2],"genMET_e":[10,0,200],"promptGenMET_pt":[10,0,200],"promptGenMET_eta":[10,-5,5],"promptGenMET_phi":[32,-3.2,3.2],"promptGenMET_e":[10,0,200],"genMETTrue_pt":[10,0,200],"genMETTrue_eta":[10,-5,5],"genMETTrue_phi":[32,-3.2,3.2],"genMETTrue_e":[10,0,200]}

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
        elif dirName == "fwdjet2" or dirName == "fwdjet1" or dirName == "bjet1" or dirName == "bjet2" or dirName == "jet1" or dirName == "jet2" or dirName == "jet3":            
            theOtherTag = "bjet1"
            
        if not theOtherTag == "":
            theOtherOne = AutoLimits[ var.replace(dirName , theOtherTag) ]            
            nbins = theOtherOne[0]
            from_ = theOtherOne[1]
            to = theOtherOne[2]
            
        name = var.replace("_" , "")

        #for cut in allCuts :
        #    cut.AddHist( name , var , nbins , from_ , to , Title=title , dirName = dirName )
    elif  var in TruthVars :
        nbins = TruthVars[var][0]
        from_ = TruthVars[var][1]
        to = TruthVars[var][2]

        dirName = "Truth"
        name = var.replace("_" , "")

        #for cut in allCuts:
        #    cut.AddHist( name , var , nbins , from_ , to , Title=title , dirName = dirName , MCOnly = True )
    else:
        print "{0:s} does not exist in the AutoLimit collection and will be treated as Automatic variable".format( var )
        #for cut in allCuts:
        #    cut.AddHist(var , var , 10 , Auto = True , Title=title)


cDiG2J1T.AddHist( met1 , leptT )
for cut in allCuts:
    plotter.AddTreePlots( cut )

plotter.LoadHistos( LUMI  , "tagsDumper/" ) #
fout = TFile.Open( outfname , "recreate")
plotter.Write(fout, normtodata)
fout.Close()
