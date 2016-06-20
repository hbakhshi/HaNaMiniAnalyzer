from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan, kBlue

import os
Sample.WD = os.path.dirname(os.path.abspath(__file__))
print Sample.WD

MicroAOD76Samples = []

DoubleEG76D = Sample( "DoubleEG_D" , "Data" , 0 , False , kBlack , "/DoubleEG/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-Run2015D-16Dec2015-v2-5edb826a5c37da64e53f7a0f39c62a72/USER" )
MicroAOD76Samples.append( DoubleEG76D )

DoubleEG76C = Sample("DoubleEG_C" , "Data" , 0 , False , kBlack , "/DoubleEG/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-Run2015C_25ns-16Dec2015-v1-5edb826a5c37da64e53f7a0f39c62a72/USER" )
MicroAOD76Samples.append( DoubleEG76C )

GluGluH76GG = Sample("GluGluH" , "Higgs" , 43.92*2.28e-3 , True , kRed , "/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-61ec12b3e335d5103b9c71fb98a2868d/USER" )
MicroAOD76Samples.append(GluGluH76GG)

VBFH76GG = Sample("VBFH" , "Higgs" , 3.748*2.28e-3 , True , kRed ,"/VBFHToGG_M125_13TeV_amcatnlo_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1-61ec12b3e335d5103b9c71fb98a2868d/USER")
MicroAOD76Samples.append(VBFH76GG)

VH76GG = Sample("VHGG" , "Higgs" , 2.355*2.28e-3 , True , kRed , "/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v4-61ec12b3e335d5103b9c71fb98a2868d/USER")
MicroAOD76Samples.append(VH76GG)

DiGG76  = Sample("DiPhoton" , "multi-#gamma" , 84.0 , False , kOrange , "/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(DiGG76)

GJet7640M80  = Sample("GJet7640M80" , "multi-#gamma" , 3216.0 , False , kOrange , "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(GJet7640M80)

GJet76M80_2040  = Sample("GJet76M80_2040" , "multi-#gamma" , 220.0 , False , kOrange , "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER" )
MicroAOD76Samples.append(GJet76M80_2040)

GJet76M80_40  = Sample("GJet76M80_40" , "multi-#gamma" , 850.8 , False , kOrange , "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER" )
MicroAOD76Samples.append(GJet76M80_40)

QCDDoubleEM76_m4080_pt30  = Sample("QCDDoubleEM76_m4080_pt30" , "QCD" , 162060000.0*0.0016 , False , kGreen+2 , "/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(QCDDoubleEM76_m4080_pt30)

QCDDoubleEM76_m80_pt3040  = Sample("QCDDoubleEM76_m80_pt3040" , "QCD" , 108000000.0*0.0016 , False , kGreen+2 , "/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(QCDDoubleEM76_m80_pt3040)

QCDDoubleEM76_m80_pt40  = Sample("QCDDoubleEM76_m80_pt40" , "QCD" , 54120000.0*0.0016 , False , kGreen+2 , "/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER" )
MicroAOD76Samples.append(QCDDoubleEM76_m80_pt40)

ZG2LG76  = Sample("ZG2LG76" , "multi-#gamma" , 117.864 , True , kOrange , "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(ZG2LG76)

TTGG76  = Sample("TTGG" , "Top" ,  0.017  , True , kBlue  , "/TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(TTGG76)

TTGJ76  = Sample("TTGJ" , "Top" , 3.697 , True , kBlue , "/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(TTGJ76)

TGJ76  = Sample("TGJ" , "Top" , 2.967 , True , kBlue , "/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(TGJ76)

ttH76GG = Sample("ttH" , "Top" , 0.5085*1.525639529*2.28e-3 , True , kBlue , "/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-a7cbec612cb152a63062cf78d7a8471c/USER") 
MicroAOD76Samples.append( ttH76GG )

Signal76  = Sample("Signal" , "Signal" , 0.01561  , True , kCyan , "/THQ_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1/hbakhshi-thggqProduction-Moriond16WSFinal-0305d2bd17670bc0d20b0c34c43ed269/USER")
MicroAOD76Samples.append(Signal76)


