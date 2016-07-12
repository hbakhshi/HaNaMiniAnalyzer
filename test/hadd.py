#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)

from Samples76tHq.Samples import *
samples = None
runOnOutsOfAnotherJob = True
if runOnOutsOfAnotherJob :
    samples = samples24june
    samples += sampleswith24juneonly
else :
    samples = MicroAOD76Samples

for sample in samples:
    if sample.Name in [s.Name for s in sampleswith24juneonly]:
        #job is already created : sample.MakeJobs( 20 , "%s/%s" % (OutPath24June , prefix) )
        print sample.Name 
    else:
        sample.MakeJobs( 3 , "eos/cms/store/user/%s/%s/%s" % (GetUserName(), "thqTree6july" , "tree" ) ) 

from tHqAnalyzer.HaNaMiniAnalyzer.Plotter import ExtendedSample
for sample in samples:
    ss = ExtendedSample(sample)
    ss.fhadd()
