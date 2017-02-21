from ROOT import Double, TF1, TFitResult, TFile, TCanvas, TH1 , TH1F , TH2F , kRed, kBlue, kOrange, kYellow, kGreen , kCyan, kGray , kBlack , gStyle
dirs = [ "MuSel" , "Jet" , "bJet" , "2J" , "2J1T" , "2JF1" , "nonIsoMu" ]

gStyle.SetOptTitle(1)

f = TFile.Open("out_jeta.root")
refdir = "DiGSelection"
refPlot =  f.Get( "/%s/mGG/cats/mGG_MultiGamma"%(refdir) )
refPlot.Add( f.Get( "/%s/mGG/cats/mGG_QCD"%(refdir) ) )
print "%s:%.2f" % (refdir , refPlot.Integral() )
refPlot.Scale(1.0/refPlot.Integral())
refPlot.SetLineColor(kBlack)
refPlot.SetTitle( refdir )
refPlot.SetStats(0)
option = "C"
allCanvases = []
for dir in dirs:
    c = TCanvas(dir , dir)
    allCanvases.append( c )
    h = f.Get( "/%s/mGG/cats/mGG_%s_MultiGamma"%(dir,dir) ) 
    h.Add( f.Get( "/%s/mGG/cats/mGG_%s_QCD"%(dir,dir) ) )
    print "%s:%.2f" % (dir , h.Integral() )
        
    h.Scale(1.0/h.Integral())
    h.SetLineColor( kRed) 
    h.SetTitle( dir )
    h.SetStats(0)
    h.Draw(option)
    refPlot.Draw("same " + option)

    

signalR = "2J1T"
print "summary of QCD estimation :"
    
cFit = TCanvas("cFit" , "Fit")
dataGG =  f.Get( "/%s/mGG/cats/mGG_Data"%(refdir) )

initial = dataGG.Integral()

#dataGG.Scale( 1.0/dataGG.Integral() )
func1 = TF1( "func1" , "TMath::Exp([0]+[1]*x)+TMath::Exp([2]+[3]*x)" , 90 , 200 )
frgg = dataGG.Fit( func1 )

ratio = func1.Integral(120,130)/func1.Integral(90 , 200)
print "%.2f/(%.2f*%.3f)=%.2f" % (func1.Integral(120,130) , initial , ratio , func1.Integral(120,130)/(initial*ratio) )

dataGG.Draw()

cFit2 = TCanvas("cFit2" , "Fit2" )
data2JF3 = f.Get( "/%s/mGG/cats/mGG_%s_Data"%(signalR , signalR) )

initial = data2JF3.Integral()

#data2JF3.Scale( 1.0 / data2JF3.Integral() )
func2 = TF1( "func2" , "TMath::Exp([0]+[1]*x)+TMath::Exp([2]+[3]*x)" , 92 , 182 )
fr2jf3 = data2JF3.Fit( func2 )

ratio = func2.Integral(122,128)/func2.Integral(92 , 182)
print "%.2f/(%.2f*%.3f)=%.2f" % (func2.Integral(122,128) , initial , ratio , func2.Integral(122,128)/(initial*ratio) )

effmu = 0.0001
qcdBkg = initial*ratio*effmu
qcdBkgErr = qcdBkg
print "qcd = %f" % (qcdBkg)
data2JF3.Draw()


signalR = "bJet"
print "H resonances + real muons :"

sm2JF3 = f.Get( "/%s/mGG/cats/mGG_%s_SM"%(signalR , signalR) )
bin1 , bin2 = sm2JF3.FindBin( 124 ) , sm2JF3.FindBin( 125 )
sm = sm2JF3.Integral( bin1 , bin2   )

sm2JF3.Add( f.Get( "/%s/mGG/cats/mGG_%s_ttH"%(signalR , signalR) ) )
smMCErr = Double(0.0)
smMC = sm2JF3.IntegralAndError( bin1 , bin2  , smMCErr )
smMCErrVal = 2*float(smMCErr)
print "%f +- %.3f" % (smMC , smMCErr)
print "sm-only = %f , ttH only = %f" % (sm , smMC - sm)




from array import array
Kvs = [1.0 , 1.5 , 0.5]
KvKfs = {
    1.0:[-3. , -2. , -1.5 , -1.25 ,      -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ],
    1.5:[-3. , -2. , -1.5 , -1.25 , -1 , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ],
    .5: [-3. , -2. , -1.5 , -1.25 , -1 , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ]
}
def GetSignalIndex(KV,KF):
    if KV==1. and KF==-1. :
        return 0
    index = 1
    for i in Kvs:
        if i==KV :
            break
        else:
            index += len( KvKfs[i] )
    index += [i for i in range(0,len(KvKfs[KV])) if KvKfs[KV][i] == KF][0]
    return index

print "Signals :"
signalIs = range(0,51)
signalHists = {ii:f.Get( "/%s/mGG/signals/mGG_%s_Signal%s" % (signalR , signalR , "" if ii==0 else ( "_%d"%(ii) ) ) ) for ii in signalIs }
signalVals = {}
for index in signalIs:
    val = signalHists[index].IntegralAndError( bin1 , bin2 , smMCErr )
    signalVals[index] = (val , float(smMCErr) )
#print signalVals
fout = TFile.Open("processes.root" , "RECREATE")
cf_bins = [-3.0	,-2.0 ,-1.5 ,-1.25 ,-1.0 , -0.75 , -0.5	,-0.25 ,0.0 , 0.25,0.5,0.75 ,1.0,1.25,1.5,2.0,3.0]
hSignalYields = TH2F("hSignalYields" , "SignalYields" , len(cf_bins)-1 , array('d' , cf_bins ) , 3 , 0.25 , 1.75 )

hSignalRVals = TH2F("hExpRVals" , "ExpRVals" , len(cf_bins)-1 , array('d' , cf_bins ) , 3 , 0.25 , 1.75 )


signal=TH1F("signal","signal",1, 0., 1.);
bkg=TH1F("bkg","bkg",1, 0., 1.);
data=TH1F("data","data",1, 0., 1.);      

import math
bkg.SetBinContent(1 , qcdBkg) #smMC + 
bkg.SetBinError( 1 , 0.05*( qcdBkg ) ) #math.sqrt( smMCErrVal*smMCErrVal + qcdBkgErr*qcdBkgErr ) )

data.SetBinContent( 1 , 1 )
data.SetBinError( 1 , 1 )

bkg.Print("ALL")
data.Print("ALL")

from ROOT import TLimitDataSource, TLimit, TConfidenceLevel

r_step = 1
steps = 100
cls = TH1F("cls", "cls",  steps, (0.5 *r_step), ((0.5+ steps) *r_step))
Expe0 = TH1F("Expe0", "ExpectedCLs_b(0)",  steps, (0.5 *r_step), ((0.5+ steps) *r_step))
Expe_plus1 = TH1F("Expe_plus1", "ExpectedCLs_b(1)",  steps, (0.5 *r_step), ((0.5+ steps) *r_step))
Expe_minus1 = TH1F("Expe_minus1", "ExpectedCLs_b(-1)",  steps, (0.5 *r_step), ((0.5+ steps) *r_step))

for KV in Kvs:
    print "%.2f:"%(KV)
    for KF in cf_bins:
        index = GetSignalIndex(KV , KF)
        bin = hSignalYields.FindBin( KF , KV )
        sig = signalVals[index][0]
        sigE = signalVals[index][1]
        hSignalYields.SetBinContent( bin , sig )
        hSignalYields.SetBinError( bin , sigE )
        for i in range( 1 , steps+1):
            signal.SetBinContent( 1 , sig*r_step*i )
            signal.SetBinError( 1 , 0.01*sig*r_step*i )

            mydatasource = TLimitDataSource( signal , bkg , data )
            # myconfidence = TLimit.ComputeLimit( mydatasource , 50000 )
            # cls.Fill( i*r_step , myconfidence.CLs() )
            # Expe_plus1.Fill((i * r_step), myconfidence.GetExpectedCLs_b(0))
            # Expe_minus1.Fill((i * r_step), myconfidence.GetExpectedCLs_b(1) )
            # Expe0.Fill((i * r_step), myconfidence.GetExpectedCLs_b(-1))

            del mydatasource
            # del myconfidence

        last = Expe0.FindLastBinAbove( 0.05 )
        observed = Expe0.GetBinCenter( last )

        print "    %.2f: %f , %f"%(KF , sig , observed)
        hSignalRVals.SetBinContent( bin , observed )
        
hSignalYields.Write()
hSignalRVals.Write()


fout.Close()
