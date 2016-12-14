#!/usr/bin/env python

#../../python/JSONDSReader.py ../Samples80tHq/Samples.py MicroAOD80Samples ./moriond17_datasets.json > a.py
#../../python/JSONDSReader.py ../Samples80tHq/Samples.py MicroAOD80Samples https://github.com/cms-analysis/flashgg/raw/master/MetaData/data/RunIISpring16DR80X-2_3_0-25ns_Moriond17_MiniAODv2/datasets.json

import sys
import json
from difflib import SequenceMatcher
from JSONSample import *

baseSampleFile = sys.argv[1]
oldSamplesName = sys.argv[2]
jsonFile = sys.argv[3]

if jsonFile.startswith("http"):
    import os.path
    from urlparse import urlparse
    o = urlparse(jsonFile)
    jsonFile = "./" + os.path.basename( o.path )
    if not os.path.exists( jsonFile ):
        import urllib2
        
        url = sys.argv[3]
        file_name = jsonFile
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()

import imp
SamplePyFile = imp.load_source( oldSamplesName , baseSampleFile )
_oldsamples = getattr( SamplePyFile , oldSamplesName )

samples = []
f = open(jsonFile, 'r' )
a = json.load(f)
for _sample in a:
    sample = JSONSample(_sample , a[_sample] , jsonFile)
    samples.append(sample)
    sample.FindOldSample(_oldsamples)

#write the output file
print "from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *"

print "import os"
print "Sample.WD = os.path.dirname(os.path.abspath(__file__))"
print "print Sample.WD"
print "MicroAODSamples = []"

for s in samples:
    if s.OldSample:
        if s.OldSample.IsData :
            s.Print()

print "#=============================="
print "#MC Samples"
            
for s in samples:
    if s.OldSample :
        if not s.OldSample.IsData :
            s.Print()


print "#=============================="
print "#new data samples"

for s in samples:
    if not s.OldSample :
        if s.Data:
            s.Print() 

print "#=============================="
print "#new MC samples"

for s in samples:
    if not s.OldSample :
        if not s.Data:
            s.Print() 
        
            
print "#=============================="
print "#samples that don't exist any longer"
        
oldsampleswithnewcopy = [ s.OldSample for s in samples if s.OldSample ]
for olds in _oldsamples :
    if olds not in oldsampleswithnewcopy:
        print "#" + olds.Name
