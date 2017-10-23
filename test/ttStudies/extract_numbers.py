from ROOT import TFile, TH2, Double
from math import sqrt
selections = ["DiG2J" , "DiG2J1T" , "DiGNoLeptons" , "SR" ]

#varname = "IsdiphosuleadpromptvsIsdipholeadprompt"
varname = "diphosuleadpromptvsdipholeadprompt"

frmt = "{sel}/PlottedVars/{var}/cats/{sel}_{var}_{sample}"


class SelectionResults :
    def __init__(self, name, h):
        self.Name = name
        self.Entries = h.GetEntries()
        self.Error = Double(0)
        self.Integral = h.IntegralAndError(0,200 ,0,200, self.Error)
        self.Values = {}
        prompt_stat = {"unknown":0.1 , "prompt":1.1 , "fake":2.1 }
        for lead_stat,lead_index in prompt_stat.items() :
            for sub_lead_stat,sub_lead_index in prompt_stat.items() :
                if lead_index != sub_lead_index :
                    bin_ = h.FindBin( lead_index , sub_lead_index )
                    bin_2 = h.FindBin( sub_lead_index , lead_index )
                    self.Values[ ( int(lead_index-0.1) , int(sub_lead_index-0.1) ) ] = ( h.GetBinContent( bin_ )+h.GetBinContent( bin_2 ) , sqrt( h.GetBinError( bin_ )*h.GetBinError( bin_ ) + h.GetBinError( bin_2 )*h.GetBinError( bin_2 ) ) )
                else :
                    bin_ = h.FindBin( lead_index , sub_lead_index )
                    self.Values[ ( int(lead_index-0.1) , int(sub_lead_index-0.1) ) ] = ( h.GetBinContent( bin_ ) ,  h.GetBinError( bin_ ) )
        

    def GetRatioErr(self, val, err ):
        if(val == 0 ):
            return 0
        else:
            return err/val
    @staticmethod
    def PrintHeader():
        print "\t".join( ["Name" , "Entries" , "Integral" , "UnkUnk" , "UnkPrmpt" , "UnkFake" , "PrmptPrmpt" , "PrmptFake" , "FakeFake" ] )
    def Print(self):
        sorted_indices = [(0,0),(0,1),(0,2) , (1,1), (1,2) , (2,2) ]
        print self.Name , "\t".join( [str(v) for v in ( [self.Entries, self.Integral] + [ self.Values[index][0] for index in sorted_indices ] ) ] )
        print "\t" , "\t".join( [str(v) for v in ([self.Integral/self.Entries, self.GetRatioErr( self.Integral , self.Error) ] + [ self.GetRatioErr( self.Values[index][0], self.Values[index][1]) for index in sorted_indices ] ) ] )
        
class SampleInfo :
    def __init__(self, name):
        self.Name = name
        self.Selections = {}
    def Add(self, sel_name , histo ):
        self.Selections[ sel_name ] = SelectionResults( sel_name , histo )
        return self.Selections[ sel_name ]

    def Print(self):
        print self.Name
        for sel in selections:
            self.Selections[sel].Print()

samples = [ SampleInfo("TTJetsAMC") , SampleInfo("TTJetsMG") , SampleInfo("TTGJets") , SampleInfo("TTGG") ]

fIn = TFile.Open("out_allTopSamples.root")
SelectionResults.PrintHeader()
for sample in samples :
    for sel in selections :
        h = fIn.Get( frmt.format( sel=sel , var=varname , sample=sample.Name ) )
        sample.Add( sel , h )
    sample.Print()
        
        

fIn.Close()

