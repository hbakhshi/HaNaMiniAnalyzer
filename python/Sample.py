from os import listdir
from os.path import isfile, join
from das_client import *
from subprocess import call
import os, ntpath
import os.path

####NEVER TRY TO IMPORT ROOT MODULES IN THE PYTHON CONFIGURATION, Oherwise CMSSW fails in initiating the tree
#kGray = 920
#kGreen = 416
#kOrange = 800
#kRed = 632
#kBlack = 1
#kCyan = 432
#kBlue = 600
######################################################################

##recommended code to group a list : https://docs.python.org/2/library/itertools.html#recipes
from itertools import izip_longest
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)
#### grouper code

class JobInformation:
    def __init__( self, sample , index , inputs , output ):
        self.Sample = sample 
        self.Index = index
        self.Inputs = inputs
        self.Output = output
        self.Output2 = ("edm_output_" + output)

class Sample :
    WD = './'

    def __init__(self , name , xsection , lheW , datasetname , appendix = "" ):
        self.Name = name
        self.XSection = xsection
        self.IsData = (self.XSection <= 0)
        self.LHEWeight = lheW
        
        self.Files = []

        if not datasetname == "" :
            self.InitiateFilesFromListOrDAS( datasetname , appendix )

    def AddFiles( self , directory ):
        files = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
        self.Files.extend( files )

    def GetListFileName( self ):
        return Sample.WD + "/" + self.Name + ".list"

    def WriteFileListToFile( self ):
        if os.path.exists(self.GetListFileName() ):
            os.remove( self.GetListFileName() )

        with open(self.GetListFileName() , 'w') as f :
            for fline in self.Files :
                f.write( fline + "\n" )

    def LoadFilesFromList(self):
        if os.path.exists( self.GetListFileName() ):
            with open(self.GetListFileName() , 'r') as f :
                for line in f.readlines() :
                    self.Files.append( line.strip() )

    def InitiateFilesFromListOrDAS( self , sample , prefix = "" ):
        self.Files = []
        self.LoadFilesFromList()

        if len(self.Files) == 0 :
            self.AddDASFiles( sample , prefix )
            self.WriteFileListToFile()

    def AddDASFiles( self , sample , prefix = "" ):
        jsondict = get_data( "https://cmsweb.cern.ch" , 
                             "file dataset=%(sample)s instance=prod/phys03"  %  {'sample':sample} ,
                             0 , #idx
                             0 , #limit
                             0 , #verbose
                             300 , #waiting time
                             "" ,  #ckey
                             "" , #cert
                             )
        
        cli_msg  = jsondict.get('client_message', None)
        if  cli_msg:
            print "DAS CLIENT WARNING: %s" % cli_msg
        if  'status' not in jsondict:
            print 'DAS record without status field:\n%s' % jsondict
            sys.exit(EX_PROTOCOL)
        if  jsondict['status'] != 'ok':
            print "status: %s, reason: %s" \
                % (jsondict.get('status'), jsondict.get('reason', 'N/A'))
            sys.exit(EX_TEMPFAIL)

        data = jsondict['data']
        iii = 1
        for jjj in data:
            #print "%d/%d : %s" % ( iii , len(data) , ntpath.basename(str(prim_value(jjj))) )
            iii += 1
            self.Files.append( prefix + str( prim_value(jjj) ) )


    def MakeJobs( self , nFilesPerRun , prefix_out ):
        self.Jobs = []
        indices = range(0 , len( self.Files) )
        job_counter = 0
        for input_files_in_job in grouper( indices , nFilesPerRun , -1000 ):
            inputfiles = [ self.Files[i] for i in input_files_in_job if i > -100 ]

            outputfilename = ""
            if nFilesPerRun == 1:
                outputfilename = "%(prefix)s_%(sample)s_%(input)s.root" % {
                    "prefix":prefix_out , 
                    "sample":self.Name , 
                    "input":os.path.splitext( os.path.basename( inputfiles[0] ))[0]
                    }
            else:
                outputfilename = "%(prefix)s_%(sample)s_%(input)s_%(nFiles)d.root" % {
                    "prefix":prefix_out , 
                    "sample":self.Name , 
                    "input":os.path.splitext( os.path.basename( inputfiles[0] ))[0],
                    "nFiles":nFilesPerRun
                    }
            jjj =JobInformation( self.Name, job_counter , inputfiles , outputfilename )
            setattr( self, "Job%d" % (job_counter) , jjj )
            self.Jobs.append( getattr( self , "Job%d" % (job_counter) ) )
            job_counter+=1
            
        return job_counter
