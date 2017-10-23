from ROOT import TFile, RooWorkspace, RooDataSet , RooAbsPdf, TGraph , RooFit, kOrange, RooBreitWigner, RooRealVar, RooCBShape, RooAddPdf, RooArgList, RooArgSet, TCanvas
import sys


frame = None
fInDS = TFile.Open( "~/Downloads/tHq_Georgios/output/29June/signals/WS_THQ.root" )
wsDS = fInDS.Get("tagsDumper/cms_hgg_13TeV")
DS = wsDS.data("thq_125_13TeV_THQLeptonicTag")
var = wsDS.var( "CMS_hgg_mass")
var.setRange( 115 , 135 )
var.SetTitle("m_{#gamma#gamma}")
var.setUnit("GeV")
# mean = RooRealVar("test_mean" , "test_mean" , 125 , 120 , 130 )
# width = RooRealVar("test_width" , "test_width" , 4 , 0 , 10 )
# Signal_bw = RooBreitWigner("test" , "title" , var , mean, width )

# mean_cb = RooRealVar("cb_mean" , "cb_mean" , 125 , 120 , 130 )
# sigma = RooRealVar("cb_sigma" , "" , 4 , 0 , 10 )
# alpha = RooRealVar("cb_alpha" , "" , 2 , 0 , 5 )
# cb_n = RooRealVar("cb_n" , "" ,  0 , 10 )
# Signal_cb = RooCBShape( "cb" , "cb" , var , mean_cb , sigma , alpha , cb_n )

# fraction = RooRealVar("fraction" , "" , 0 , 1 )

# Signal = RooAddPdf("Signal" , "Signal" , Signal_bw , Signal_cb , fraction )

# Signal.fitTo( DS , RooFit.Minimizer("Minuit","minimize"), RooFit.Hesse(True) ,RooFit.SumW2Error(True),RooFit.Save(True) ,RooFit.PrintLevel(0) )


def PlotAll( nBins ):
    var.setBins( nBins )
    frame = var.frame()
    frame.SetTitle("tHq signal model, nBins=%d" % (nBins) )
    frame.SetName("frame_nbins%d" % (nBins) )
    DS.plotOn( frame ).getHist().SetTitle("tHq")

    # Signal.plotOn( frame , RooFit.LineColor( kOrange ) ).getCurve().SetTitle("BW" )

    #fIn1 = TFile.Open( "../out_thq_syst_order1.root" )
    #ws1 = fIn1.Get( "cms_hgg_13TeV" )
    #pdf1 = ws1.pdf( "RVthq_mh125" )
    #pdf1.plotOn( frame , RooFit.LineColor( 8 ) ).getCurve().SetTitle("nGaussians = 1" )


    #fIn2 = TFile.Open( "../out_thq_syst_order2.root" )
    #ws2 = fIn2.Get( "cms_hgg_13TeV" )
    #pdf2 = ws2.pdf( "RVthq_mh125" )
    #pdf2.plotOn( frame , RooFit.LineColor( 4 ) ).getCurve().SetTitle("nGaussians = 2" )

    fIn3 = TFile.Open( "../out_thq_syst.root" )
    ws3 = fIn3.Get( "cms_hgg_13TeV" )
    pdf3 = ws3.pdf( "RVthq_mh125" )
    allpdfs = pdf3.pdfList()
    listToPlot = RooArgSet()
    colors = [8 , 4 , 2 ]
    nParams = [ 3, 6 , 8]
    chi2s = []
    for pdfindex in range(0, allpdfs.getSize() ):
        innerpdf = allpdfs.at( pdfindex )
        name = innerpdf.GetName()
        listToPlot.add( innerpdf )
        color = colors[pdfindex]
        if pdfindex == 2 :
            pdf3.plotOn( frame , RooFit.LineColor( color ) , RooFit.Components( listToPlot )).getCurve().SetTitle( name ) #"nGaussians = 3" )
            chi2 = frame.chiSquare( nParams[pdfindex] )
            #print name, chi2
            chi2s.append( chi2 )

    #frame.Draw()
    frame.GetXaxis().SetRangeUser(122, 128)
    return chi2s, frame

allChi2s = {}
frames = {}
for nbin in range(50 , 210 , 50):
    chi2s , frame_ = PlotAll( nbin )
    allChi2s[nbin] = chi2s
    frames[nbin] = frame_
    print frame_
print allChi2s
allCanvases = {}
canvas = None
for a in frames:
    canvas = TCanvas( "canvas_nbins%d" % a )
    frames[a].Draw()
    allCanvases[a] = canvas
    canvas.SaveAs("tHqSignalModel_nBins%d.pdf"%a)
