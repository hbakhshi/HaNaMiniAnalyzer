from ROOT import TDirectory, TFile, TCanvas , TH1D , TH1 , THStack, TList, gROOT, TLegend, TPad, TLine, gStyle, TTree , TObject , gDirectory

import os
import sys
import Sample

class ExtendedSample: #extend the sample object to store histograms
    def __init__( self , sample ):
        self.Name = sample.Name 
        self.XSection = sample.XSection 
        self.XSections = {0:self.XSection}
        self.LHEWeight = sample.LHEWeight 
        self.DSName = sample.DSName 
        self.Prefix = sample.Prefix
        self.IsData = sample.IsData
        
        self.Files = sample.Files
        self.Jobs = sample.Jobs

        if sample.ParentSample :
            self.ParentSample = ExtendedSample( sample.ParentSample )
        else :
            self.ParentSample = None

    def GetCFT(self , index = 0):
        if not hasattr( self, "CutFlowTableName" ):
            return None
        if not self.CutFlowTableName in self.AllHists:
            return None
        return self.AllHists[self.CutFlowTableName][index]

    def SetNTotal(self, n):
        self.NTotal = n
    
    def GetNTotal(self , index = 0) :
        if hasattr(self, "NTotal") :
            return self.NTotal
        if self.ParentSample :
            if not self.ParentSample.GetCFT(index) :
                print "Loading parent sample"
                self.ParentSample.LoadHistos( self.DirName , self.CutFlowTableName , [self.CutFlowTableName] , self.LoadedIndices )
                print "Loaded"
            return self.ParentSample.GetNTotal(index)
        else :
            if not self.GetCFT(index) :
                return -1
            return self.GetCFT().GetBinContent( 1 )

    def NormalizeHistos(self, lumi):
        if self.IsData :
            return
        self.nTotal = self.GetNTotal()
        if self.nTotal == 0:
            print "Sample %s has no entries" % (self.Name)
            return

        for index in self.LoadedIndices:
            self.XSFactor = lumi*self.XSections[index]/self.nTotal
            #print "%s factor : (%.2f*%.2f)/%.0f = %.3f" % (sample , lumi , self.XSections[sample] , ntotal  , factor)
            for h in self.AllHists :
                if len(self.AllHists[h]):
                    self.AllHists[h][index].Scale(self.XSFactor)

    def LoadHistos(self , dirName = "tHq" , cftName = "CutFlowTable" , loadonly = [] , indices = [0]):
        self.LoadedIndices = indices
        self.CutFlowTableName = cftName
        self.DirName = dirName
        self.AllHists = {}
        for Job in self.Jobs :
            finame = Job.Output
            sys.stdout.write("\r%s : %d of %d" % (self.Name , Job.Index+1 , len(self.Jobs)))
            sys.stdout.flush()
            ff = None
            if os.path.isfile( finame ):
                ff = TFile.Open(finame)
            else:
                print "File %d of sample %s doesn't exist, skip it , %s" % (Job.Index , self.Name , finame)
                continue
            dir = ff.GetDirectory(dirName)
            if not dir :
                print "File %d of sample %s is not valid, skip it , %s" % (Job.Index , self.Name , finame)
                continue
            for dir__ in dir.GetListOfKeys() :
                if not dir__.IsFolder():
                    continue
                propname = dir__.GetName()
                if len(loadonly) > 0 and not propname in loadonly :
                    continue
                dir_ = dir.GetDirectory( propname )
                dircontents = dir_.GetListOfKeys()
                selectedHistos = {}
                for index in indices:
                    thehisto = dir_.Get( dircontents.At(index).GetName() )
                    if thehisto.ClassName().startswith("TH"):
                        selectedHistos[index] = thehisto 

                if propname in self.AllHists.keys() :
                    for index in selectedHistos:
                        firsthisto = selectedHistos[index]
                        self.AllHists[propname][index].Add( firsthisto )
                else :
                    gROOT.cd()
                    self.AllHists[propname] = {}
                    for index in selectedHistos:
                        firsthisto = selectedHistos[index]
                        hnew = firsthisto.Clone("%s_%s_%d" % ( propname , self.Name , index ) )
                        hnew.SetBit(TH1.kNoTitle)
                        #hnew.Reset()
                        setattr( self , "%s_%d" % (propname, index) , hnew )
                        hhh = getattr( self , "%s_%d" % (propname, index) )
                        hhh.SetLineColor( 1 )
                        hhh.SetLineWidth( 2 )
                        if not self.IsData :
                            hhh.SetFillStyle( 1001 )
                        else:
                            hhh.SetStats(0)

                        self.AllHists[propname][index] = hhh    
                    
            ff.Close()

        if len(self.AllHists)==0 :
            return False
        else:
            return True


    def readKeys(self , directory):
        """Return a list of objects in directory that inherit from tree or histo. """

        if not directory.InheritsFrom("TDirectory"):
            return []
        selKeys = [key for key in directory.GetListOfKeys() if key.ReadObj().InheritsFrom("TH1") or key.ReadObj().InheritsFrom("TTree") or key.ReadObj().InheritsFrom("TDirectory")]
        ret = {}
        for k in selKeys:
            kcycle = k.GetCycle()
            kname = k.GetName()

            lastCycle = -1
            if kname in ret :
                lastCycle = ret[ kname ][0]
            if not (kcycle > lastCycle):
                continue
            elif (kcycle == lastCycle):
                print "%s has two similar cycle values %d and %d" % (kname , kcycle , lastCycle )

            ret[ kname ] = ( kcycle , k.ReadObj() )

        return [ ret[s][1] for s in ret ]

    def loop(self , directory):
        """Traverse directory recursively and return a list of (path, name) pairs of
        all objects inheriting from classname."""
        
        contents = []

        for d in self.readKeys(directory):
            if not d.InheritsFrom("TDirectory") :
                contents.append((directory.GetPath().split(':')[-1], d.GetName() ))
            else :
                contents += self.loop(d)

        return contents

    def fhadd(self, force=False, verbose=False, slow=True):
        """ taken from https://root.cern.ch/phpBB3/viewtopic.php?t=14881
        This function will merge objects from a list of root files and write them    
        to a target root file. The target file is newly created and must not
        exist, or if -f ("force") is given, must not be one of the source files.
        
        IMPORTANT: It is required that all files have the same content!

        Fast but memory hungry alternative to ROOT's hadd.
        
        Arguments:

        target -- name of the target root file
        sources -- list of source root files
        classname -- restrict merging to objects inheriting from classname
        force -- overwrite target file if exists
        """

        target = self.Name + ".root"
        sources = [j.Output for j in self.Jobs]

        TH1.AddDirectory(False)
        # check if target file exists and exit if it does and not in force mode
        if not force and os.path.exists(target):
            raise RuntimeError("target file %s exists" % target)

        # open the target file
        print "fhadd Target file:", target
        outfile = TFile(target, "RECREATE")

        # open the seed file - contents is looked up from here
        seedfilename = sources[0]
        print "fhadd Source file 1", seedfilename
        seedfile = TFile(seedfilename)

        # get contents of seed file
        print "looping over seed file"
        contents = self.loop(seedfile)
        print "done %d objects are ready to be merged" % len(contents)
        if( verbose ):
            for c in contents:
                print c
                

        # open remaining files
        otherfiles = []
        for n, f in enumerate(sources[1:]):
            print "fhadd Source file %d: %s" % (n+2, f)
            otherfiles.append(TFile(f))

        
        # loop over contents and merge objects from other files to seed file objects
        for n, (path, hname) in enumerate(contents):

            print "fhadd Target object: %s" % os.path.join(path, hname)
            obj_path = os.path.join(path, hname)
            obj_ = seedfile.Get(obj_path[1:])

            outfile.cd('/')
            # create target directory structure
            for d in path.split('/')[1:]:
                directory = gDirectory.GetDirectory(d)
                if not directory:
                    gDirectory.mkdir(d).cd()
                else:
                    gDirectory.cd(d)
            obj = None
            if obj_.InheritsFrom("TTree"):
                obj = obj_.CloneTree()
            else:
                obj = obj_.Clone()

            # merge objects
            l = TList()
            for o in [of.Get(obj_path[1:]) for of in otherfiles]:
                l.Add(o)
            obj.Merge(l)

            # delete objects if in slow mode
            if slow:
                print "Deleting %d object(s)", l.GetEntries()
                l.Delete()

            # write object to target
            obj.Write(obj.GetName(), TObject.kOverwrite)

        print "Writing and closing file"

        # let ROOT forget about open files - prevents deletion of TKeys
        for f in [outfile, seedfile]+otherfiles:
            gROOT.GetListOfFiles().Remove(f);

        outfile.Write()
        outfile.Close()

        for f in [seedfile]+otherfiles:
            f.Close()
            


class SampleType:
    def __init__(self , name , color , samples = [] , signal = False ):
        self.Name = name 
        if type(color) is int:
            self.Color = color
            self.MultiPlot = False
            
        self.Samples = [ExtendedSample(s) for s in samples]
        if type(color) is dict:
            self.Colors = color
            
        self.IsSignal = signal

    def IsData(self):
        if len(self.Samples) == 0 :
            return False
        return self.Samples[0].IsData

    def LoadHistos(self , lumi , dirName = "tHq" , cftName = "CutFlowTable"):
        self.AllHists = {}
        for s in self.Samples :
            if s.LoadHistos( dirName , cftName ):
                s.NormalizeHistos( lumi )
            print ""
            for propname in s.AllHists:
                if propname in self.AllHists.keys() :
                    print propname
                    self.AllHists[propname].Add(s.AllHists[propname][0])
                else :
                    gROOT.cd()
                    if len(s.AllHists[propname]) == 0:
                        print "%s skipped" % propname
                        continue
                    hnew = s.AllHists[propname][0].Clone("%s_%s" % ( propname , self.Name ) )
                    hnew.SetTitle( self.Name )
                    hnew.SetBit(TH1.kNoTitle) 
                    setattr( self , propname , hnew )
                    hhh = getattr( self , propname )
                    hhh.SetLineColor( 1 )
                    hhh.SetLineWidth( 2 )
                    if not self.IsData() :
                        hhh.SetFillColor( self.Color )
                        hhh.SetFillStyle( 1001 )
                    else:
                        hhh.SetStats(0)

                    self.AllHists[propname] = hhh    


class Plotter:
    def __init__(self):
        self.Samples = []
        self.Props = []

    def AddSampleType(self , st):
        self.Samples.append(st)

    @staticmethod
    def addLabels(histo , labels):
        for i in range(1, histo.GetNbinsX()+1 ):
            if not i > len(labels) :
                histo.GetXaxis().SetBinLabel( i , labels[i-1] )

    def AddLabels(self , hist , labels ):
        if labels :
            for st in self.Samples:
                Plotter.addLabels( st.AllHists[hist] , labels )
                for s in st.Samples :
                    for index in s.AllHists[hist]:
                        Plotter.addLabels( s.AllHists[hist][index] , labels )

 
    def GetStack(self, propname):
        stackname = "%s_stack" % (propname)
        if not hasattr(self , stackname):
            #print stackname
            setattr( self, stackname , THStack( stackname , propname ) )
            for st in self.Samples:
                if not st.IsData() and not st.IsSignal:
                    getattr( self, stackname ).Add( st.AllHists[propname] )

        return getattr(self , stackname)

    def GetData(self, propname):
        for st in self.Samples:
            if st.IsData():
                return st.AllHists[propname]
        return None

    def GetCanvas(self, propname , padid):
        canvasname = "%s_canvas" % (propname)
        pad1name = "%s_pad1" % (propname)
        pad2name = "%s_pad2" % (propname)
        if not hasattr(self , canvasname):
            #print canvasname
            setattr( self, canvasname , TCanvas( canvasname ) )
            setattr( self, pad1name  ,  TPad(pad1name ,pad1name,0,0.25,1,1) )
            getattr( self, pad1name).SetBottomMargin(0.1)
            getattr( self, pad1name).Draw()

            getattr( self, canvasname).cd()

            setattr( self, pad2name , TPad( pad2name,pad2name,0,0,1,0.24) )
            getattr( self, pad2name).SetTopMargin(0.1)
            getattr( self, pad2name).SetBottomMargin(0.1)
            getattr( self, pad2name).Draw()

        if padid == 0:
            getattr( self, canvasname).cd()
        elif padid == 1:
            getattr( self, pad1name).cd()
        if padid == 2:
            getattr( self, pad2name).cd()

        return getattr(self , canvasname)

    def GetLegend(self , propname ):
        legendname = "%s_legend" % (propname)
        if not hasattr(self , legendname):
            setattr( self , legendname , TLegend(0.7,0.6,0.9,0.9,"","brNDC") )
            getattr( self , legendname).SetName( legendname )
            getattr( self , legendname).AddEntry( self.GetData(propname) , "Data" , "lp" )
            for st in reversed( self.Samples ):
                if not st.IsData() and not st.IsSignal:
                    getattr( self , legendname).AddEntry( st.AllHists[propname] , st.Name , "f" )
        return getattr( self , legendname)

    def GetRatioPlot(self, propname):
        rationame = "%s_Ratio" % (propname)
        if not hasattr(self, rationame):
            setattr( self, rationame , self.GetData(propname).Clone( rationame ) )
            getattr( self, rationame).SetStats(0)
            getattr( self, rationame).Divide( self.GetStack(propname).GetStack().Last() )
            Plotter.addLabels( getattr( self, rationame) , [ "" for ii in range(0 , self.GetData(propname).GetNbinsX()+1 ) ] )
            getattr( self, rationame).SetMarkerStyle(20)
            getattr( self, rationame).GetYaxis().SetRangeUser(0,2)
            getattr( self, rationame).GetXaxis().SetLabelSize( 0.)
            getattr( self, rationame).GetYaxis().SetTitle("Data / MC")
            getattr( self, rationame).GetXaxis().SetTitleSize(0.2) 
            getattr( self, rationame).GetXaxis().SetTitleOffset(0.25)
            getattr( self, rationame).GetYaxis().SetLabelSize(0.1)
            getattr( self, rationame).GetXaxis().SetTickLength(0.09)
            getattr( self, rationame).GetYaxis().SetTitleSize(0.18)
            getattr( self, rationame).GetYaxis().SetNdivisions(509)
            getattr( self, rationame).GetYaxis().SetTitleOffset(0.25)
            getattr( self, rationame).SetFillStyle(3001)
            
        return getattr( self, rationame)

    def GetRatioUnc(self, propname):
        rationame = "%s_RatioUncert" % (propname)
        if not hasattr(self, rationame):
            mc = self.GetStack(propname).GetStack().Last()
            setattr( self, rationame , mc.Clone( rationame ) )
            getattr( self, rationame).SetStats(0)
            getattr( self, rationame).Divide(mc)
            Plotter.addLabels( getattr( self, rationame) , [ "" for ii in range(0 , self.GetData(propname).GetNbinsX()+1 ) ] )
            #getattr( self, rationame).SetMarkerStyle(20)
            getattr( self, rationame).GetYaxis().SetRangeUser(0,2)
            #getattr( self, rationame).GetXaxis().SetLabelSize( 0.)
            getattr( self, rationame).GetYaxis().SetTitle("Data / MC")
            getattr( self, rationame).GetXaxis().SetTitleSize(0.2) 
            getattr( self, rationame).GetXaxis().SetTitleOffset(0.25)
            getattr( self, rationame).GetYaxis().SetLabelSize(0.1)
            getattr( self, rationame).GetXaxis().SetTickLength(0.09)
            getattr( self, rationame).GetYaxis().SetTitleSize(0.18)
            getattr( self, rationame).GetYaxis().SetNdivisions(509)
            getattr( self, rationame).GetYaxis().SetTitleOffset(0.25)
            getattr( self, rationame).SetFillStyle(3001)
            getattr( self, rationame).SetFillColor(1)
            
        return getattr( self, rationame)


    def GetLineOne(self, propname):
        linename = "%s_lineone" % (propname)
        if not hasattr(self, linename):
            setattr( self , linename , TLine(self.GetRatioPlot(propname).GetXaxis().GetXmin(), 1.00, self.GetRatioPlot(propname).GetXaxis().GetXmax(), 1.00) )
            getattr( self , linename).SetLineWidth(2)
            getattr( self , linename).SetLineStyle(7)

        return getattr(self, linename)


    def LoadHistos(self  , lumi , dirName = "tHq" , cftName = "CutFlowTable"):
        for st in self.Samples :
            st.LoadHistos( lumi , dirName , cftName )
            for prop in st.AllHists:
                if not prop in self.Props:
                    self.Props.append( prop )

    def DrawAll(self ):
        gStyle.SetOptTitle(0)

       
        for prop in self.Props :
        
            self.GetCanvas( prop , 1 )
            self.GetData(prop).Draw("E")
            self.GetStack(prop).Draw("HIST SAME")
            self.GetData(prop).Draw("E SAME P")
            self.GetLegend(prop).Draw()
            
            self.GetCanvas( prop , 2 )
            self.GetRatioUnc( prop ).Draw("E2")
            self.GetRatioPlot(prop).Draw("ep same")
            self.GetLineOne(prop).Draw()

    def Write(self, fout ):
        for propname in self.Props :
            propdir = fout.mkdir( propname )
            propdir.cd()
            sampledir = propdir.mkdir( "samples" )
            catdir = propdir.mkdir( "cats" )
            
            for sample in self.Samples :
                catdir.cd()
                sample.AllHists[propname].Write()
                self.GetStack(propname).GetStack().Last().Write("SumMC")
                sampledir.cd()
                for ss in sample.Samples:
                    ss.AllHists[propname][0].Write()
                propdir.cd()
                self.GetCanvas(propname , 0).Write()
            fout.cd()
