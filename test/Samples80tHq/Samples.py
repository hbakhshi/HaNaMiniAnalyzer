from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *

import os
Sample.WD = os.path.dirname(os.path.abspath(__file__))
print Sample.WD

MicroAOD80Samples = []

DoubleEG80Dp2 = Sample( "DoubleEG_2016Dp2" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2_p2-2_2_0-v0-Run2016D-PromptReco-v2-9a092465adbfb13c40886e07b86f6d23/USER" )
MicroAOD80Samples.append( DoubleEG80Dp2 )
DoubleEG80Dp3 = Sample( "DoubleEG_2016Dp3" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2_p3-2_2_0-v0-Run2016D-PromptReco-v2-9a092465adbfb13c40886e07b86f6d23/USER" )
MicroAOD80Samples.append( DoubleEG80Dp3 )
DoubleEG80Dp4 = Sample( "DoubleEG_2016Dp4" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2_p4-2_2_0-v0-Run2016D-PromptReco-v2-9a092465adbfb13c40886e07b86f6d23/USER" )
MicroAOD80Samples.append( DoubleEG80Dp4 )

DoubleEG80Bp3 = Sample( "DoubleEG_2016Bp3" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2_p3-2_2_0-v0-Run2016B-PromptReco-v2-6afd65c310508d0f49bd277bc7a8e5b1/USER" )
MicroAOD80Samples.append( DoubleEG80Bp3 )
DoubleEG80Bp2 = Sample( "DoubleEG_2016Bp2" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2_p2-2_2_0-v0-Run2016B-PromptReco-v2-6afd65c310508d0f49bd277bc7a8e5b1/USER" )
MicroAOD80Samples.append( DoubleEG80Bp2 )
DoubleEG80Bp1 = Sample( "DoubleEG_2016Bp1" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-Run2016B-PromptReco-v1-6afd65c310508d0f49bd277bc7a8e5b1/USER" )
MicroAOD80Samples.append( DoubleEG80Bp1 )

DoubleEG80Cp1 = Sample( "DoubleEG_2016Cp1" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-Run2016C-PromptReco-v2-9a092465adbfb13c40886e07b86f6d23/USER" )
MicroAOD80Samples.append( DoubleEG80Cp1 )
DoubleEG80Cp2 = Sample( "DoubleEG_2016Cp2" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2_p2-2_2_0-v0-Run2016C-PromptReco-v2-9a092465adbfb13c40886e07b86f6d23/USER" )
MicroAOD80Samples.append( DoubleEG80Cp2 )


ttH80GG = Sample("ttH" , 0.5085*1.525639529*2.28e-3 , True  , "/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8_v2/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1-2a45e67daf15c7abeea509b3e1c7829c/USER")
MicroAOD80Samples.append( ttH80GG )


GluGluH80GG = Sample("GluGluH" , 43.92*2.28e-3 , True , "/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1-9d6acec11aa5264fedffe5a321afb429/USER")
MicroAOD80Samples.append(GluGluH80GG)
GluGluH80GGP2 = Sample("GluGluHP2" , 43.92*2.28e-3 , True , "/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext2-v1-9d6acec11aa5264fedffe5a321afb429/USER" )
MicroAOD80Samples.append(GluGluH80GGP2)


VBFH80GG = Sample("VBFH" , 3.748*2.28e-3 , True  ,"/VBFHToGG_M125_13TeV_amcatnlo_pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext2-v1-9d6acec11aa5264fedffe5a321afb429/USER" )
MicroAOD80Samples.append(VBFH80GG)

VH80GG = Sample("VHGG" , 2.355*2.28e-3 , True  , "/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv1-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v1-9d6acec11aa5264fedffe5a321afb429/USER" )
MicroAOD80Samples.append(VH80GG)


DiG_40Box80  = Sample("DiPhoton_40Box80" ,  303.2 , False  , "/DiPhotonJetsBox_M40_80-Sherpa/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(DiG_40Box80)

DiG_80Box  = Sample("DiPhoton_80Box" ,  84.4 , False  , "/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(DiG_80Box)

DiG_Jets  = Sample("DiPhoton_Jets" ,  135.1 , True  , "/DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(DiG_Jets)

GJet8040M80  = Sample("GJet8040M80" , 3216.0 , False , "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(GJet8040M80)

GJet80M80_2040  = Sample("GJet80M80_2040" , 220.0 , False , "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER")
MicroAOD80Samples.append(GJet80M80_2040)

GJet80M80_40  = Sample("GJet80M80_40" ,  850.8 , False , "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(GJet80M80_40)

QCDDoubleEM80_m4080_pt30  = Sample("QCDDoubleEM80_m4080_pt30" , 162060000.0*0.0016 , False , "/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(QCDDoubleEM80_m4080_pt30)

QCDDoubleEM80_m80_pt3040  = Sample("QCDDoubleEM80_m80_pt3040" , 108000000.0*0.0016 , False , "/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(QCDDoubleEM80_m80_pt3040)

QCDDoubleEM80_m80_pt40  = Sample("QCDDoubleEM80_m80_pt40" , 54120000.0*0.0016 , False , "/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(QCDDoubleEM80_m80_pt40)

DYee = Sample("dyEE" ,2008.333333 , False , "/DYToEE_NNPDF30_13TeV-powheg-pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-94d03017ce60e1991044b8807b85a209/USER" )
MicroAOD80Samples.append( DYee )

ZG2LG80  = Sample("ZG2LG80" , 117.864 , True , "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(ZG2LG80)

TTGG80  = Sample("TTGG" ,  0.017  , True ,  "/TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(TTGG80)

TGJ80  = Sample("TGJ" , 2.967 , True , "/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(TGJ80)

TGJ80_ext  = Sample("TGJ_ext" , 2.967 , True , "/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1-b4da767d058dfcf162795c45ef775a16/USER" )
MicroAOD80Samples.append(TGJ80_ext)


Signal76  = Sample("Signal" , 0.01561  , True , "/THQ_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1/hbakhshi-thggqProduction-Moriond16WSFinal-0305d2bd17670bc0d20b0c34c43ed269/USER")
MicroAOD80Samples.append(Signal76)
