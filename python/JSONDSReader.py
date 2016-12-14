#!/usr/bin/env python
import sys
import json
from difflib import SequenceMatcher

baseSampleFile = sys.argv[1]
oldSamplesName = sys.argv[2]
jsonFile = sys.argv[3]

import imp
SamplePyFile = imp.load_source( oldSamplesName , baseSampleFile )
_oldsamples = getattr( SamplePyFile , oldSamplesName )

class File:
    def __init__(self, bad, events , name , nevents , totEvents , weights ):
        self.bad = bad
        self.events = events
        self.name = name
        self.nevents = nevents
        self.totEvents = totEvents
        self.weights = weights

class JSONSample :
    def FindOldSample(self , oldsamples ):
        self.OldSample = None
        parts1 = self.Path.split("/")
        nametolook = parts1[1]
        nameparts = nametolook.split("_")
        if len(nameparts) < 2:
            self.ObjName = nameparts[0]
        else:
            self.ObjName = "{S[0]}_{S[1]}".format( S=nameparts )
        self.XSection = 0.
        self.AllMatchedOldSamples = {}
        highestsimilarity = 0.
        for s in oldsamples:
            parts2 = s.DSName.split("/")
            if parts2[1]  == nametolook :
                similarityOf2ndParts = SequenceMatcher(None, parts2[2] , parts1[2] ).ratio()
                self.AllMatchedOldSamples[similarityOf2ndParts] =  s
                if similarityOf2ndParts > highestsimilarity :
                    self.OldSample = s
                    self.ObjName = s.Name
                    self.XSection = s.XSection
                    highestsimilarity = similarityOf2ndParts
    def __init__(self, path ):
        self.Path = str(path)
        self.Vetted = False
        self.Files = []
        self.Data = False

    def ISamcatnlo(self):
        return "amcatnlo" in self.Path
    
    def AddFile(self,  bad, events , name , nevents , totEvents , weights ):
        self.Files.append( File(  bad, events , str(name) , nevents , totEvents , weights ) )

    def hasLumi(self):
        self.Data = True
        
    def nTotal(self , i = -1):
        ret = 0.
        if i == -1:
            ret = {}
            ret['events'] = self.nTotal(0)
            ret['nevents'] = self.nTotal(1)
            ret['totEvents'] = self.nTotal(2)
            ret['weights'] = self.nTotal(3)
            return ret
        
        for f in self.Files:
            if i == 0 :
                ret += f.events
            elif i == 1:
                ret += f.nevents
            elif i == 2 :
                ret += f.totEvents
            elif i == 3:
                ret += weights
        return ret

    def Print(self):
        if not hasattr(self,"OldSample"):
            self.FindOldSample(_oldsamples)
        format_ = '{objName} = Sample( "{objName}" , {xsection:.3f} , {useLHE} , "{fullpath}" , info_from_json={jsoninfo} )'
        print format_.format( objName=self.ObjName , xsection=self.XSection , useLHE=self.ISamcatnlo() , fullpath=self.Path , jsoninfo=self.nTotal(-1) )

        print "MicroAODSamples.append( {objName} )".format( objName=self.ObjName )
samples = []
f = open(jsonFile, 'r' )
a = json.load(f)
for _sample in a:
    sample = JSONSample(_sample)
    vetted = False
    samples.append(sample)
    sample.FindOldSample(_oldsamples)
    for j in a[_sample]:
        if j == "vetted":
            #print a[i][j]
            sample.Vetted =  a[_sample][j]
        if j == "files":
            for file in a[_sample][j]:
                name = file["name"]
                #print "\t%s" % name
                bad = file["bad"]
                if not bad:
                    events = file["events"]
                    nevents = file["nevents"]
                    totEvents = file["totEvents"]
                    weights = file["weights"]
                    if "lumis" in file.keys():
                        sample.hasLumi()
                    sample.AddFile( bad , events , name , nevents , totEvents , weights )

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
