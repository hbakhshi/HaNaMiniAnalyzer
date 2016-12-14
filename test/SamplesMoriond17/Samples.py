from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *
import os
Sample.WD = os.path.dirname(os.path.abspath(__file__))
print Sample.WD

MicroAODSamples = []

originjsonfile = "https://github.com/cms-analysis/flashgg/raw/master/MetaData/data/RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2/datasets.json"

DoubleEG_2016B = Sample( "DoubleEG_2016B" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-Run2016B-23Sep2016-v3-2366c4343141c765b2996ae305da0b97/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 74309280.0, 'weights': 74309280.0, 'events': 74309280.0, 'totEvents': 74309280.0} )
MicroAODSamples.append( DoubleEG_2016B )

DoubleEG_2016C = Sample( "DoubleEG_2016C" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-Run2016C-23Sep2016-v1-2366c4343141c765b2996ae305da0b97/USER" )
MicroAODSamples.append( DoubleEG_2016C )

DoubleEG_2016D = Sample( "DoubleEG_2016D" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-Run2016D-23Sep2016-v1-2366c4343141c765b2996ae305da0b97/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 40585811.0, 'weights': 40585811.0, 'events': 40585811.0, 'totEvents': 40585811.0} )
MicroAODSamples.append( DoubleEG_2016D )

DoubleEG_2016E = Sample( "DoubleEG_2016E" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-Run2016E-23Sep2016-v1-2366c4343141c765b2996ae305da0b97/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 38195110.0, 'weights': 38195110.0, 'events': 38195110.0, 'totEvents': 38195110.0} )
MicroAODSamples.append( DoubleEG_2016E )

DoubleEG_2016F = Sample( "DoubleEG_2016F" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-Run2016F-23Sep2016-v1-2366c4343141c765b2996ae305da0b97/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 28353769.0, 'weights': 28353769.0, 'events': 28353769.0, 'totEvents': 28353769.0} )
MicroAODSamples.append( DoubleEG_2016F )

DoubleEG_2016G = Sample( "DoubleEG_2016G" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-Run2016G-23Sep2016-v1-56157a2727a0c1c384898c280a0f972f/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 66901364.0, 'weights': 66901364.0, 'events': 66901364.0, 'totEvents': 66901364.0} )
MicroAODSamples.append( DoubleEG_2016G )

DoubleEG_2016Hv2 = Sample( "DoubleEG_2016Hv2" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-Run2016H-PromptReco-v2-531158c93170d8cd2bdb89d7c81ef33d/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 73682623.0, 'weights': 73682623.0, 'events': 73682623.0, 'totEvents': 73682623.0} )
MicroAODSamples.append( DoubleEG_2016Hv2 )

DoubleEG_2016Hv3 = Sample( "DoubleEG_2016Hv3" , 0 , False , "/DoubleEG/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-Run2016H-PromptReco-v3-531158c93170d8cd2bdb89d7c81ef33d/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 1780260.0, 'weights': 1780260.0, 'events': 1780260.0, 'totEvents': 1780260.0} )
MicroAODSamples.append( DoubleEG_2016Hv3 )
#==============================
#MC Samples
ttH = Sample( "ttH" , 0.5085*1.525639529*2.28e-3 , True , "/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8_v2/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1-e74a5b70c6e42b3de729c1530015af74/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 57578.0, 'weights': 58228.431640625, 'events': 57578.0, 'totEvents': 57578.0} )
MicroAODSamples.append( ttH )

ZZ = Sample( "ZZ" , 2.187 , True , "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 15498581.0, 'weights': 78628764.875, 'events': 15498581.0, 'totEvents': 15498581.0} )
MicroAODSamples.append( ZZ )


QCDDoubleEM80_m80_pt3040 = Sample( "QCDDoubleEM80_m80_pt3040" , 172800.000 , False , "/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 13234357.0, 'weights': 13234371.015625, 'events': 13234357.0, 'totEvents': 13234357.0} )
MicroAODSamples.append( QCDDoubleEM80_m80_pt3040 )


GJet80M80_2040 = Sample( "GJet80M80_2040" , 220.000 , False , "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 23021187.0, 'weights': 23021187.0, 'events': 23021187.0, 'totEvents': 23021187.0} )
MicroAODSamples.append( GJet80M80_2040 )


TGJ = Sample( "TGJ" , 2.967 , True , "/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 292508.0, 'weights': 873069.1875, 'events': 292508.0, 'totEvents': 292508.0} )
MicroAODSamples.append( TGJ )

TGJ_ext = Sample( "TGJ_ext" , 2.967 , True , "/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 1535543.0, 'weights': 4604091.09375, 'events': 1535543.0, 'totEvents': 1535543.0} )
MicroAODSamples.append( TGJ_ext )

ZG2LG80 = Sample( "ZG2LG80" , 117.864 , True , "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 3806725.0, 'weights': 906233964.0, 'events': 3806725.0, 'totEvents': 3806725.0} )
MicroAODSamples.append( ZG2LG80 )

dyEE = Sample( "dyEE" , 2008.333 , False , "/DYToEE_NNPDF30_13TeV-powheg-pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-faa0a239fcf93e081b27c889f6b0a964/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 29113024.0, 'weights': 29113024.0, 'events': 29113024.0, 'totEvents': 29113024.0} )
MicroAODSamples.append( dyEE )

WZ = Sample( "WZ" , 3.053 , True , "/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 25996157.0, 'weights': 229406490.0625, 'events': 25996157.0, 'totEvents': 25996157.0} )
MicroAODSamples.append( WZ )

WJets = Sample( "WJets" , 61526.700 , False , "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1-2ddd5a0e173d6e943a70312fcd45eccd/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 16474517.0, 'weights': 16474517.0, 'events': 16474517.0, 'totEvents': 16474517.0} )
MicroAODSamples.append( WJets )

VBFH = Sample( "VBFH" , 0.009 , True , "/VBFHToGG_M125_13TeV_amcatnlo_pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext2-v1-03c441ce0abe5028a99a11eeb0fc9751/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 1199200.0, 'weights': 4633330.6953125, 'events': 1199200.0, 'totEvents': 1199200.0} )
MicroAODSamples.append( VBFH )

GluGluHP2 = Sample( "GluGluHP2" , 0.100 , True , "/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext2-v1-6e50739fbcc735daf803d8fb7f8228e6/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 808806.0, 'weights': 88788237.75, 'events': 808806.0, 'totEvents': 808806.0} )
MicroAODSamples.append( GluGluHP2 )

GluGluH = Sample( "GluGluH" , 0.100 , True , "/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1-6e50739fbcc735daf803d8fb7f8228e6/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 984957.0, 'weights': 108302910.375, 'events': 984957.0, 'totEvents': 984957.0} )
MicroAODSamples.append( GluGluH )

VHGG = Sample( "VHGG" , 0.005 , True , "/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv1-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v1-adab2a7703d08b4fee0a4ae86e5785fb/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 272237.0, 'weights': 1818013.8806152344, 'events': 272237.0, 'totEvents': 272237.0} )
MicroAODSamples.append( VHGG )

QCDDoubleEM80_m80_pt40 = Sample( "QCDDoubleEM80_m80_pt40" , 86592.000 , False , "/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 16759235.0, 'weights': 16759235.0, 'events': 16759235.0, 'totEvents': 16759235.0} )
MicroAODSamples.append( QCDDoubleEM80_m80_pt40 )

TTGG = Sample( "TTGG" , 0.017 , True , "/TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 592894.0, 'weights': 10206.568359375, 'events': 592894.0, 'totEvents': 592894.0} )
MicroAODSamples.append( TTGG )

DiPhoton_80Box = Sample( "DiPhoton_80Box" , 84.400 , False , "/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 58432739.0, 'weights': 27635070.15234375, 'events': 58432739.0, 'totEvents': 58432739.0} )
MicroAODSamples.append( DiPhoton_80Box )


GJet8040M80 = Sample( "GJet8040M80" , 3216.000 , False , "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 32058274.0, 'weights': 32058274.0, 'events': 32058274.0, 'totEvents': 32058274.0} )
MicroAODSamples.append( GJet8040M80 )


WW = Sample( "WW" , 118.700 , False , "/WW_TuneCUETP8M1_13TeV-pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 993214.0, 'weights': 993234.03125, 'events': 993214.0, 'totEvents': 993214.0} )
MicroAODSamples.append( WW )

WG = Sample( "WG" , 1.000 , False , "/WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 4910964.0, 'weights': 4910964.0, 'events': 4910964.0, 'totEvents': 4910964.0} )
MicroAODSamples.append( WG )

TTGJ = Sample( "TTGJ" , 3.697 , True , "/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 4874091.0, 'weights': 33400200.9375, 'events': 4874091.0, 'totEvents': 4874091.0} )
MicroAODSamples.append( TTGJ )

DiPhoton_40Box80 = Sample( "DiPhoton_40Box80" , 303.200 , False , "/DiPhotonJetsBox_M40_80-Sherpa/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 4918237.0, 'weights': 3717666.7890625, 'events': 4918237.0, 'totEvents': 4918237.0} )
MicroAODSamples.append( DiPhoton_40Box80 )


TTbar = Sample( "TTbar" , 831.760 , False , "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext3-v1-2ddd5a0e173d6e943a70312fcd45eccd/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 92264396.0, 'weights': 92264396.0, 'events': 92264396.0, 'totEvents': 92264396.0} )
MicroAODSamples.append( TTbar )

GJet80M80_40 = Sample( "GJet80M80_40" , 850.800 , False , "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 2964701.0, 'weights': 2964701.0, 'events': 2964701.0, 'totEvents': 2964701.0} )
MicroAODSamples.append( GJet80M80_40 )

ZG2LG80 = Sample( "ZG2LG80" , 117.864 , True , "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 13439651.0, 'weights': 3198669538.1875, 'events': 13439651.0, 'totEvents': 13439651.0} )
MicroAODSamples.append( ZG2LG80 )

QCDDoubleEM80_m4080_pt30 = Sample( "QCDDoubleEM80_m4080_pt30" , 259296.000 , False , "/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" , info_from_json={'jsonfile': './datasets.json', 'nevents': 33712778.0, 'weights': 33712778.0, 'events': 33712778.0, 'totEvents': 33712778.0} )
MicroAODSamples.append( QCDDoubleEM80_m4080_pt30 )
#==============================

Signal = Sample("Signal" , 0.01561  , True , "/THQ_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1/ferrif-RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2-2_3_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1-0451b197ac7f8037fffa7c3d2e4e2210/USER" )
MicroAODSamples.append(Signal)

