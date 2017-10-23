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
from ROOT import kAzure, kGray, kGreen, kYellow, kOrange, kRed, kBlack, kCyan, kBlue, gROOT, TLatex, TCanvas, TFile, TColor, TSystem, RooWorkspace, RooDataSet

TreeTemN = "tagsDumper/trees/%s_13TeV_THQLeptonicTag"
DIR="/home/hbakhshi/Downloads/tHq_Georgios/output/14_07_17/"

cutJetGamma = "(!(dipho_lead_prompt==1 && dipho_sulead_prompt==1) && (dipho_lead_prompt==1 || dipho_sulead_prompt==1))"
cutJetJet = "(dipho_lead_prompt!=1 && dipho_sulead_prompt!=1)"
cutGammaGamma = "(dipho_lead_prompt==1 && dipho_sulead_prompt==1)"

data_files = sorted( glob.glob( DIR + "/data/2gamma_2jets/Run2016*.root" ) , key=os.path.getsize) 
dataSamples = SampleType("Data" , kBlack , [ Sample( os.path.basename(s).split('.')[0] , 0 , False , "" , treeName = TreeTemN % ("Data") ) for s in data_files ] , os.path.dirname(data_files[0]) )


gjets_files = { DIR + "/bkgs/2gamma_2jets/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8.root":TreeTemN % ("gjet"),
                DIR + "/bkgs/2gamma_2jets/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8.root":TreeTemN % ("gjet") }
qcd_files = glob.glob(DIR+"/bkgs/2gamma_2jets/QCD*.root")
fake_files = gjets_files
for file in qcd_files :
    fake_files[file] = TreeTemN % ("qcd")

gjet = SampleType("gammajet" , kCyan-2  , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in fake_files.items()  ] , DIR+"/bkgs/2gamma_2jets/" , additionalCut = cutJetGamma )
jetJet = SampleType("jetjet" , kCyan-3  , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in fake_files.items()  ] , DIR+"/bkgs/2gamma_2jets/" , additionalCut = cutJetJet )
digamma_files = {DIR + "/bkgs/DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8.root":TreeTemN % ("dipho") }
digSamples = SampleType("DiGamma" , kOrange , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName = t  ) for s,t in digamma_files.items() ] , DIR+"/bkgs/2gamma_2jets/" , additionalCut = cutGammaGamma )

colorPhotons = TColor.GetColor("#ffcc00")
incPhotonSamples = SampleType( "Photons" , colorPhotons , [] , "" , False , None )
for s in digSamples.Samples :
    incPhotonSamples.Samples.append( s )
for s in jetJet.Samples :
    incPhotonSamples.Samples.append( s )
for s in gjet.Samples :
    incPhotonSamples.Samples.append( s )

BosonFiles = { DIR + "/bkgs/2gamma_2jets/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" : TreeTemN % ("Wjets") ,
               DIR + "/bkgs/2gamma_2jets/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root" : TreeTemN % ("ZG"),
               DIR + "/bkgs/2gamma_2jets/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root" : TreeTemN % ("DY") }
colorBosons = kGreen+2
bosonsSamples = SampleType( "VectorBosons" , colorBosons , [Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in BosonFiles.items()] , DIR+"/bkgs/2gamma_2jets/" )

ttHcolor = kRed
ttHSamples = { DIR + "signals/2gamma_2jets/THW.root" : "thw_125" ,
              DIR + "signals/2gamma_2jets/TTH.root" : "tth_125" }
ttH = SampleType( "ttH+tHW" , ttHcolor , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=TreeTemN % (t) ) for s,t in ttHSamples.items()  ] , DIR + "/signals/" )

higgs_files = { DIR + "/signals/2gamma_2jets/GGH.root":TreeTemN % ("ggh_125"),
                DIR + "/signals/2gamma_2jets/VBF.root":TreeTemN % ("vbf_125") ,
                DIR + "/signals/2gamma_2jets/VH.root":TreeTemN % ("vh_125") }
higgsColor = kBlue
Higgs = SampleType("OtherHiggs" , higgsColor ,  [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in higgs_files.items() ] , DIR + "/signals/" )

top_files = {
    #DIR + "/bkgs/TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8.root":TreeTemN % ("ttgg"),
    #DIR + "/bkgs/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.root":TreeTemN % ("tgjets"),
    DIR + "/bkgs/2gamma_2jets/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8.root":TreeTemN % ("tgjets"),
    DIR + "/bkgs/2gamma_2jets/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" : TreeTemN % ("TTJet") 
}
colorTop = TColor.GetColor("#993333")
Top_Samples = SampleType( "Top" , colorTop ,  [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=t ) for s,t in top_files.items() ] , DIR + "/bkgs/2gamma_2jets/" ) 


tHSamples = { DIR + "signals/THQ.root" : "thq_125" }
tH = SampleType("tHq" , kCyan+4 , [ Sample( os.path.basename(s).split('.')[0] , -1 , False , "" , treeName=TreeTemN % (t) ) for s,t in tHSamples.items() ] , DIR+"/signals/2gamma_2jets/"   )

allSTs = [ dataSamples , tH, ttH , Higgs , bosonsSamples ,  incPhotonSamples ,  Top_Samples]
###############  SAMPLE LIST CREATED #############


outfname = ""
outfname = "out_CRPlots_%s.root" % ( sys.argv[1] )

if sys.argv[1] == "WS" :
    Workspaces = []
    ws = RooWorkspace( "cms_hgg_13TeV" )
    intLumi = RooRealVar("IntLumi" , "IntLumi" , LUMI )
    getattr( ws , "import")( intLumi )
    Workspaces.append( ws )
    for st in allSTs :
        if st.IsData() :
            st.LoadDataset()


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
        "met" : "1==1", #(MET_pt > 30)" ,
        "BDT" : "MVA_Medium > 0 ",
        "CRLeptons" : "(n_muons > 0 || n_ele > 0 ) && !(%s || %s)" % ( ELECTRON_CHANNEL , MUON_CHANNEL  ),
        "CRRelaxLeptonVeto" : "(n_muons > 0 || n_ele > 0 ) && !(%s || %s)" % ( ELECTRON_CHANNEL , MUON_CHANNEL  ),
        "EtaJP_NJ" : "( abs(fwdjet1_eta) > 2.5 && n_jets == 2 )",
        "EtaJP_NbJ" :"( abs(fwdjet1_eta) > 2.5 && n_L_bjets == 1 )" ,
        "NJ_NbJ" : "(n_jets == 2 && n_L_bjets == 1)" ,
        "NJ_NbJ_EtaJP" : "(n_jets == 2 && n_L_bjets == 1 && abs(fwdjet1_eta) > 2.5)" }


Regions = {"EtaJP_NJ":"EtaNJet","EtaJP_NbJ":"EtaNbJet","NJ_NbJ":"NJetNbJet","NJ_NbJ_EtaJP":"THQLeptonic"}

cDiGLeptons2j1t = CutInfo( "SR" , "&&".join( [ Cuts[s] for s in ["DiG" , "atLeastTwoJets" , "OneMediumB" , "met", "Leptons"] ] ) , "bTagWeight*weight" , "2J1T + Lepton + di#gamma ("+str(LUMI)+"fb^{-1})"  )
cCRbRelaxed = CutInfo( "CRbRelaxed" , "&&".join( [ Cuts[s] for s in ["DiG" , "Leptons" , "atLeastTwoJets" , "met"] ] )  , "weight"  , "cCRbRelaxed" )
cCR2MediumB = CutInfo( "CR2MediumB" , "&&".join( [ Cuts[s] for s in ["DiG"  , "atLeastTwoJets" , "TwoMediumB" , "met"] ] )  , "weight"  , "cCR2MediumB" )
cCRInvertLepCut = CutInfo( "CRInvertLepCut" , "&&".join( [ Cuts[s] for s in ["DiG" , "CRLeptons" , "atLeastTwoJets" , "OneMediumB" , "met"] ] )  , "weight"  , "Inverted Lepton Selection (Control Region)" )
cCRInvertLepCutBRelaxed = CutInfo( "CRInvertLepCutBRelaxed" , "&&".join( [ Cuts[s] for s in ["DiG" , "CRLeptons" , "atLeastTwoJets" , "met"] ] )  , "weight"  , "cCRInvertLepCutBRelaxed" )
cDiG2J1T = CutInfo( "DiG2J1T" , "&&".join( [ Cuts[s] for s in ["DiG" , "atLeastTwoJets" , "OneMediumB" , "met"] ] ), "weight" , "di#gamma + 2J1T selection ("+str(LUMI)+"fb^{-1})" )

BasicCuts = [ cDiGLeptons2j1t  , cCRInvertLepCut ] # cDiG2J1T , cCRbRelaxed , cCR2MediumB , cCRInvertLepCutBRelaxed ]
AllCuts = [ bs for bs in BasicCuts ]
NameMap = {}
for cut in AllCuts :
    NameMap[ cut.Name ] = ( cut.Name , None , None )
    
def MakeDSName( cutName ):
    name, region, signal = NameMap[ cutName ]
    if signal :
        tagName = Regions[region] + signal + "Tag"
    else:
        tagName = "THQLeptonicTag"

    if name == "SR":
        return tagName
    else :
        return name+tagName
    
for cut_ in BasicCuts :
    cut = "(" + cut_.Cut + ")"
    name = cut_.Name
    for region in Regions :
        thq_bin = CutInfo( name + "_"+region+"_THQ" , "&&".join( [ cut , Cuts[ region ] ] )  , "weight"  , name + ", " + region + ", thq bin" )
        tth_bin = CutInfo( name + "_"+region+"_TTH" , "&&".join( [ cut ,  "(!(" + Cuts[region] + "))" ] )  , "weight"  ,  name + ", " + region + ", tth bin" )
        NameMap[name + "_"+region+"_THQ"] = (name , region , "THQ")
        NameMap[name + "_"+region+"_TTH"] = (name , region , "TTH")
        print tth_bin.Cut
        AllCuts.append( thq_bin )
        AllCuts.append( tth_bin )


for cut_ in AllCuts :
    mgg = cut_.AddHist( "mGG",  "CMS_hgg_mass" , 8 , 100 , 180. , "#gamma#gamma invariant mass (GeV);#entries" , dirName = "PlottedVars")
    jprimeeta = cut_.AddHist( "jprimeeta" , "abs(fwdjet1_eta)" , 10 , 0 , 5 , "forward jet |#eta|" , dirName = "PlottedVars")
    n_L_bjets = cut_.AddHist( "nlbjets" , "n_L_bjets" , 10 , 0 , 10 , "number of loose b jets" , dirName="PlottedVars" )
    n_jets    = cut_.AddHist( "nJets" , "n_jets" , 10 , 0 , 10 , "number of jets" , dirName="PlottedVars" )
    One = cut_.AddHist( "One" , "1" , 1 , 0 , 2 , "One" , dirName="PlottedVars" )

    cut_.AddHist( jprimeeta , n_L_bjets )
    cut_.AddHist( jprimeeta , n_jets )
    cut_.AddHist( n_L_bjets , n_jets )

    plotter.AddTreePlots( cut_ )

    if sys.argv[1] == "WS" :
        for st in allSTs :
            if st.IsData() :
                ds = st.LoadDataset(cut_.Cut , Name="Data_13TeV_%s" % ( MakeDSName( cut_.Name) ) )
                ds.Print()
                getattr( ws , "import" )( ds ) 


if sys.argv[1] != "WS" :                 
    plotter.LoadHistos( LUMI  , "tagsDumper/" ) #
fout = TFile.Open( outfname , "recreate")
if sys.argv[1] != "WS" :                 
    plotter.Write(fout, False)
else :
    fout.mkdir( "tagsDumper" ).cd()
    for ws_ in Workspaces :
        ws_.Write()
    fout.cd()
    s = ""
    for n in NameMap :
        name, region , signal = NameMap[n]
        if name == cCRInvertLepCut.Name :
            s +=  MakeDSName( n ) + ","
    print s

fout.Close()


