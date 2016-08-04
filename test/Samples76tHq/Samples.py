from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *

import os
Sample.WD = os.path.dirname(os.path.abspath(__file__))
print Sample.WD

MicroAOD76Samples = []

DoubleEG76D = Sample( "DoubleEG_D" , 0 , False , "/DoubleEG/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-Run2015D-16Dec2015-v2-5edb826a5c37da64e53f7a0f39c62a72/USER" )
MicroAOD76Samples.append( DoubleEG76D )

DoubleEG76C = Sample("DoubleEG_C" , 0 , False , "/DoubleEG/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-Run2015C_25ns-16Dec2015-v1-5edb826a5c37da64e53f7a0f39c62a72/USER" )
MicroAOD76Samples.append( DoubleEG76C )

GluGluH76GG = Sample("GluGluH" , 43.92*2.28e-3 , True , "/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-61ec12b3e335d5103b9c71fb98a2868d/USER" )
MicroAOD76Samples.append(GluGluH76GG)

VBFH76GG = Sample("VBFH" , 3.748*2.28e-3 , True  ,"/VBFHToGG_M125_13TeV_amcatnlo_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1-61ec12b3e335d5103b9c71fb98a2868d/USER")
MicroAOD76Samples.append(VBFH76GG)

VH76GG = Sample("VHGG" , 2.355*2.28e-3 , True  , "/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v4-61ec12b3e335d5103b9c71fb98a2868d/USER")
MicroAOD76Samples.append(VH76GG)


DiGG_76  = Sample("DiPhoton_" ,  135.1 , False  , "/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(DiGG_76)

DiGG76  = Sample("DiPhoton" ,  84.4 , False  , "/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(DiGG76)

GJet7640M80  = Sample("GJet7640M80" , 3216.0 , False , "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(GJet7640M80)

GJet76M80_2040  = Sample("GJet76M80_2040" , 220.0 , False , "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER" )
MicroAOD76Samples.append(GJet76M80_2040)

GJet76M80_40  = Sample("GJet76M80_40" ,  850.8 , False , "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER" )
MicroAOD76Samples.append(GJet76M80_40)

QCDDoubleEM76_m4080_pt30  = Sample("QCDDoubleEM76_m4080_pt30" , 162060000.0*0.0016 , False , "/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(QCDDoubleEM76_m4080_pt30)

QCDDoubleEM76_m80_pt3040  = Sample("QCDDoubleEM76_m80_pt3040" , 108000000.0*0.0016 , False , "/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(QCDDoubleEM76_m80_pt3040)

QCDDoubleEM76_m80_pt40  = Sample("QCDDoubleEM76_m80_pt40" , 54120000.0*0.0016 , False , "/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER" )
MicroAOD76Samples.append(QCDDoubleEM76_m80_pt40)

ZG2LG76  = Sample("ZG2LG76" , 117.864 , True , "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(ZG2LG76)

TTGG76  = Sample("TTGG" ,  0.017  , True ,  "/TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(TTGG76)

TTGJ76  = Sample("TTGJ" , 3.697 , True , "/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(TTGJ76)

TGJ76  = Sample("TGJ" , 2.967 , True , "/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-7c7ed1c7bfe704638af8ca4418b6fb3d/USER")
MicroAOD76Samples.append(TGJ76)

ttH76GG = Sample("ttH" , 0.5085*1.525639529*2.28e-3 , True  , "/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-a7cbec612cb152a63062cf78d7a8471c/USER") 
MicroAOD76Samples.append( ttH76GG )

DYee = Sample("dyEE" ,2008.333333 , False , "/DYToEE_NNPDF30_13TeV-powheg-pythia8/ferrif-RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-9dd966127498bcac8c2a422833c3836e/USERd" )
MicroAOD76Samples.append( DYee )

Signal76  = Sample("Signal" , 0.01561  , True , "/THQ_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1/hbakhshi-thggqProduction-Moriond16WSFinal-0305d2bd17670bc0d20b0c34c43ed269/USER")
MicroAOD76Samples.append(Signal76)


###import SM samples
WJetsMG76_FGG = Sample( "WJetsMG_FGG" , 61526.7 , False , "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/hbakhshi-thqSM-Moriond16WSFinal-57-g2d12144-v0_2-dda6ada328391ea2517e775b7551afcb/USER" )
MicroAOD76Samples.append( WJetsMG76_FGG )

TTBar76_FGG = Sample( "TTbar_FGG" ,  831.76 , False , "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/hbakhshi-thqSM-Moriond16WSFinal-57-g2d12144-v0_2-dda6ada328391ea2517e775b7551afcb/USER" )
MicroAOD76Samples.append( TTBar76_FGG )

ZZ76_FGG = Sample( "ZZ_FGG" , 15.4*2*0.071 , True  , "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/hbakhshi-thqSM-Moriond16WSFinal-57-g2d12144-v0_2-dda6ada328391ea2517e775b7551afcb/USER"  )
MicroAOD76Samples.append(ZZ76_FGG)

WZ76_FGG = Sample( "WZ_FGG" ,  44.9*0.068 , True  , "/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/hbakhshi-thqSM-Moriond16WSFinal-57-g2d12144-v0_2-dda6ada328391ea2517e775b7551afcb/USER" )
MicroAOD76Samples.append(WZ76_FGG)

WW76_FGG = Sample( "WW_FGG" ,  118.7 , False  , "/WW_TuneCUETP8M1_13TeV-pythia8/hbakhshi-thqSM-Moriond16WSFinal-57-g2d12144-v0_2-dda6ada328391ea2517e775b7551afcb/USER" )
MicroAOD76Samples.append(WW76_FGG)

WG76_FGG = Sample( "WG_FGG" , 1 , False , "/WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/hbakhshi-thqSM-Moriond16WSFinal-57-g2d12144-v0_2-dda6ada328391ea2517e775b7551afcb/USER" )
MicroAOD76Samples.append( WG76_FGG )


sampleswith24juneonly = [WG76_FGG, TTBar76_FGG] #[DiGG_76, DYee , WJetsMG76_FGG, TTBar76_FGG, ZZ76_FGG, WZ76_FGG , WW76_FGG]
def MakeAllChildSamples( nFilesPerJob , outputName  ):
    ret = []
    for s in MicroAOD76Samples :
        s.MakeJobs( nFilesPerJob , outputName )
        if s in sampleswith24juneonly :
            pass
            #ret.append( s )
        else:
            ret.append( s.MakeSampleFromOutputs() )
    return ret
        
samples24june = MakeAllChildSamples( 20 , "/store/user/%s/%s/%s" % ("hbakhshi", "thq24june" , "out" )  )
