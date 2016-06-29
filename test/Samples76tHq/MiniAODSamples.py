from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *

import os
Sample.WD = os.path.dirname(os.path.abspath(__file__))
print Sample.WD

MiniAOD76Samples = []

WJetsMG76 = Sample( "WJetsMG" , 61526.7 , False , "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" , "" , "global" )
MiniAOD76Samples.append( WJetsMG76 )

TTBar76 = Sample( "TTbar" ,  831.76 , False , "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/MINIAODSIM"  , "" , "global" )
MiniAOD76Samples.append( TTBar76 )

ZZ76 = Sample( "ZZ" , 15.4*2*0.071 , True  , "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" , "" , "global" )

MiniAOD76Samples.append(ZZ76)

WZ76 = Sample( "WZ" ,  44.9*0.068 , True  , "/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv1-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" , "" , "global" )

MiniAOD76Samples.append(WZ76)

WW76 = Sample( "WW" ,  118.7 , False  , "/WW_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" , "" , "global")

MiniAOD76Samples.append(WW76)

