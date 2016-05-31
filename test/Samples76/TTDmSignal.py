from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan

import os
Sample.WD = os.path.dirname(os.path.abspath(__file__))
print Sample.WD

TTDMSignals = []

sampleNameTemplate = "/TTbarDMJets_%(sc_ps)s_Mchi-%(mchi)d_Mphi-%(mphi)d_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12%(ext)s-v1/MINIAODSIM" 

sc_ps_vals = [ "pseudoscalar" , "scalar" ]
ext_vals = ["" , "_ext1" ]

mchi_mphi = { 
    1:{10,20,50,100,200,300,500},
    10:{10,100},
    50:{50,200,300},
    150:{200}
}

exceptions = [ ("pseudoscalar" , "" , 50 , 300) , ( "scalar" , "" , 1 , 20 ) ]

for sc_ps in sc_ps_vals:
    for ext in ext_vals:
        for mchi in mchi_mphi:
            for mphi in mchi_mphi[mchi] :
                info = (sc_ps , ext , mchi , mphi)
                name = "TTDM_%s_%s_%d_%d" % info
                if info in exceptions:
                    print name + " is in the exception list and is skipped" 
                    continue

                title = "TTDM_%s_%d_%d"  % (sc_ps , mchi , mphi)
                xsection = 1.0
                sampleFullName = sampleNameTemplate % { "sc_ps":sc_ps , "ext":ext , "mchi":mchi , "mphi":mphi }
                #print name
                #print title 
                #print sampleFullName
                TTDMSignals.append( Sample( name  , title  , xsection , False , kBlack , sampleFullName ) )


