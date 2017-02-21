from ROOT import TFile, kBlue , kRed , kGreen, TCanvas


##########################
from tHqAnalyzer.HaNaMiniAnalyzer.Property import *
    
gROOT.SetBatch(True)

allProps = { "DiG2J1T":{"maxGmva":None , "GGmva":None , "minGmva":None},
             "Lepton2J1T":{"maxGmva":None , "GGmva":None , "minGmva":None} }
             

f = TFile.Open("out_all_normtolumi.root")
fOut = TFile.Open("a.root" , "recreate")

for cut in allProps:
    cutDir = fOut.mkdir(cut)
    for var in allProps[cut] :
        dir = f.GetDirectory("%s/%s" % (cut,var) )
        p = Property.FromDir( dir )

        for sig in range(1,6):
            p.SetSignificances(sig)

        p.SetExpectedLimits()
            
        allProps[cut][var] = p
            
        p.Write(cutDir , False , True)
        
fOut.Close()

exit()
##########################

from tHqAnalyzer.HaNaMiniAnalyzer.ExtendedSample import *
from SamplesMoriond17.Samples import *
for s in MicroAODSamples :
    ss = ExtendedSample( s )
    ss.LoadJobs( "/home/hbakhshi/Desktop/tHq/nTuples/Moriond17/" )
    if ss.IsData :
        ss.LoadHistos(loadonly=["CutFlowTable"] )
        continue
    else :
        ss.LoadHistos(loadonly=["CutFlowTable"] , indices=[0,1])
    


    if not ss.JSONInfo:
        print "sample %s doesn't have json info" % (s.Name)
        continue

    nTotH = ss.GetNTotal(1) #0 if ss.IsData else 1)
    nTotW = ss.GetNTotal(0)
    weffM = nTotW / nTotH
    nTotF = ss.JSONInfo['nevents']
    nSumW = ss.JSONInfo['weights']
    weffF = nSumW/nTotF
    
    #if not nTotH == nTotF : #and ss.LHEWeight:
    print "sample %s is not OK : f(%.2f/%d = %.2f) , m(%.2f/%d = %.2f) | WEff_(F/M) = %.2f // W_(F/M)=%.2f // Tot_(F/M) = %.2f" % ( s.Name , nSumW , nTotF , weffF , nTotW ,nTotH , weffM , weffF/weffM , nSumW/nTotW , nTotF/ nTotH )

exit()

f = TFile.Open("out_2j1tleptonbdt_normtolumi.root")

sample = "Data"
samplesToSubtract = ["ttH" , "Higgs" , "SM"]
dirs = {"Lepton2J1TBDT":kRed} #"CR12j1t":kRed , "CR1":kBlue , "Lepton2J1T":kGreen}
variable = "mGG"

c = TCanvas()
option = ""
for dir in dirs :
    data = {"dir":dir , "sample":sample , "var":variable}
    hfullname = "{dir:s}/{var:s}/cats/{dir:s}_{var:s}_{sample:s}".format( **data )
        
    h = f.Get( hfullname )
    for s in samplesToSubtract:
        data = {"dir":dir , "sample":s , "var":variable}
        hfullname = "{dir:s}/{var:s}/cats/{dir:s}_{var:s}_{sample:s}".format( **data )
        h.Add( f.Get( hfullname ) , -1 )
        
    h.SetLineColor( dirs[dir] )
    h.SetFillStyle(0)
    h.SetTitle( dir )
    h.DrawNormalized( option )
    option = "same"
