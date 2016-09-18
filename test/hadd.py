#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)

from Samples80tHq.Samples import *
samples = None
runOnOutsOfAnotherJob = False
if runOnOutsOfAnotherJob :
    samples = samples24june
    samples += sampleswith24juneonly
else :
    samples = MicroAOD80Samples

for sample in samples:
    #if sample.Name in [s.Name for s in sampleswith24juneonly]:
        #job is already created : sample.MakeJobs( 20 , "%s/%s" % (OutPath24June , prefix) )
    #    print sample.Name 
    #else:
    sample.MakeJobs( 3 , "eos/cms/store/user/%s/%s/%s" % (GetUserName(), "thqTree2016" , "tree" ) ) 

from tHqAnalyzer.HaNaMiniAnalyzer.ExtendedSample import *
for sample in samples:
    #if sample.Name in ["QCDDoubleEM76_m4080_pt30"] : #["TTbar_FGG"]
    #    print "skipping " + sample.Name
    #    continue
    ss = ExtendedSample(sample)
    ss.fhadd()
