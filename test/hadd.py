#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)

from SamplesMoriond17.Samples import *
samples = None
runOnOutsOfAnotherJob = False
if runOnOutsOfAnotherJob :
    samples = skimmedSamples1
else :
    samples = MicroAODSamples

for sample in samples:
    #if sample.Name in [s.Name for s in sampleswith24juneonly]:
        #job is already created : sample.MakeJobs( 20 , "%s/%s" % (OutPath24June , prefix) )
    #    print sample.Name 
    #else:
    sample.MakeJobs( 3 , "root://eoscms//eos/cms/store/user/%s/%s/%s" % (GetUserName(), "Moriond17" , "tree" ) ) 
    # sample.ParentSample.MakeJobs( 3 , "root://eoscms//eos/cms/store/user/%s/%s/%s" % (GetUserName(), "Moriond17" , "tree" ) ) 


from tHqAnalyzer.HaNaMiniAnalyzer.ExtendedSample import *
for sample in samples:
    ss = None
    if False : #sample.Name in ["ttH" , "Signal"]:
        print "using parent for " + sample.Name
        ss = ExtendedSample( sample.ParentSample )
    else :
        ss = ExtendedSample(sample)
    #export EOS_MGM_URL=root://eosuser.cern.ch
    #eosmount eos_cb
    ss.fhadd("root://eosuser//eos/user/h/hbakhshi/Personal/Projects/tHq/nTuples/Moriond17/")
