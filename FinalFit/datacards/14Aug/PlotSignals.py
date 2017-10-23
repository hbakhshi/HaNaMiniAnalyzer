from ROOT import TFile, RooWorkspace, RooAddPdf, RooArgList, TCanvas, RooExtendPdf, RooRealVar, RooFit, RooArgSet, kRed , kBlue , kGreen, kBlack, gROOT, RooDataSet, TH1D , RooDataHist
import sys
gROOT.SetBatch(True)
Kvs = [1.0 , 1.5 , 0.5]
KvKfs = {
    1.0:[ -3. , -2. , -1.5 , -1.25        , -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ],
    1.5:[ -3. , -2. , -1.5 , -1.25 ,  -1.0, -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ],
    0.5:[ -3. , -2. , -1.5 , -1.25 ,  -1.0, -.75 , -.5 , -.25 , 0.0 , 0.25 , 0.5 , 0.75 ,1 , 1.25 , 1.5 , 2. , 3. ]
}
AllCtOverCVs = {}
for Kv in Kvs:
    for Kf in KvKfs[Kv]:
        r = Kf/Kv
        if r in AllCtOverCVs.keys() :
            AllCtOverCVs[r][Kv] = 0.0
        else :
            AllCtOverCVs[r] = {Kv:0.0}

BinToPlot = sys.argv[1]
signals = { "tth":{"color":kRed} , "thq":{"color":kBlue} , "thw":{"color":kGreen} }
fOut = TFile.Open("out.root" , "recreate")
for kvkt in AllCtOverCVs:
    infile = TFile.Open( "ctcv%g/input.root" % (kvkt) )
    ws = infile.Get( "WS%s" % (BinToPlot) )

    mass = ws.var( "CMS_hgg_mass" )
    
    allPdfs = RooArgList()
    allNorms = RooArgList()
    finalNorm = 0.
    norms_ = {}
    for signal in signals :
        pdf = ws.pdf( "RV%s_mh125" % (signal) )
        norm = ws.var( "RV%s_mh125_norm" % (signal) )

        allPdfs.add( pdf )
        allNorms.add( norm )

        signals[signal]["pdf%g" % kvkt ] = pdf
        signals[signal]["norm%g" % kvkt ] = norm
        
        signals[signal]["extendedpdf%g" % kvkt ] = RooExtendPdf( "extended_%s_%g" % ( signal, kvkt ) , "extended_%s_%g" % ( signal, kvkt ) , pdf , norm )
        finalNorm += norm.getValV()
        norms_[signal] = norm.getValV()

    signal = RooAddPdf("signal_%g" % (kvkt) , "signal_%g" % (kvkt) , allPdfs , allNorms )
    AllCtOverCVs[ kvkt ]["norm"] = RooRealVar( "norm%g" % (kvkt) , "norm%g" % (kvkt) , finalNorm )
    AllCtOverCVs[ kvkt ]["signalnormed"] = signal
    AllCtOverCVs[ kvkt ]["signal"] = RooExtendPdf( "signal_%g_extended" % (kvkt) , "" , signal , AllCtOverCVs[ kvkt ]["norm"] )

    #AllCtOverCVs[ kvkt ]["hist_norm"] = TH1D("hist_norm%g" % (kvkt) , "" , 1000 , 115 , 135 )
    #AllCtOverCVs[ kvkt ]["hist_norm"].SetBinContent( 500 , finalNorm )
    #AllCtOverCVs[ kvkt ]["datahist_norm"] = RooDataHist( "datahist_norm%g" % (kvkt) , "datahist_norm%g" % (kvkt) , RooArgList(mass) , AllCtOverCVs[ kvkt ]["hist_norm"]  )
    AllCtOverCVs[ kvkt ]["datahist_norm"] = AllCtOverCVs[ kvkt ]["signal"].generate( RooArgSet( mass ) , finalNorm ) #*10000 )
    print kvkt , finalNorm , norms_ , AllCtOverCVs[ kvkt ]["datahist_norm"].sumEntries()/finalNorm
    
    AllCtOverCVs[ kvkt ]["frame"] = mass.frame()

    isFirst = True
    pdfs = RooArgList()
    norms = RooArgList()
    norm_total_sofar = 0.
    whatToPlot = {}
    plotIndex = 0
    for signal in signals:
        its_component = signals[signal]["pdf%g"%kvkt]
        pdfs.add( its_component )
        
        its_norm = signals[signal]["norm%g"%kvkt].getValV()
        norms.add( signals[signal]["norm%g"%kvkt] )
        norm_total_sofar += its_norm
        signals[signal]["normssofar%g" % kvkt] = RooRealVar( "normssofar_%s_%g" % (signal , kvkt) , "normssofar_%s_%g" % (signal , kvkt) , norm_total_sofar )

        color = RooFit.LineColor( signals[signal]["color"] )

        signals[signal]["sofaradded%g" % kvkt] = RooAddPdf( "added_%s_%g" % (signal, kvkt) , "added_%s_%g" % (signal, kvkt) , pdfs , norms )
        signals[signal]["extendedsofar%g" % kvkt] = RooExtendPdf( "extendedsofar_%s_%g" % (signal, kvkt) , "extendedsofar__%s_%g" % (signal, kvkt) , signals[signal]["sofaradded%g" % kvkt] , signals[signal]["normssofar%g" % kvkt] )
        norm = RooFit.Normalization( norm_total_sofar )

        whatToPlot[ plotIndex ] = ( signals[signal]["extendedsofar%g" % kvkt] , norm , color )
        plotIndex += 1
        #signals[signal]["extendedsofar%g" % kvkt].plotOn( AllCtOverCVs[ kvkt ]["frame"] , norm , color , RooFit.LineStyle(1), RooFit.LineWidth(4) )

        AllCtOverCVs[ kvkt ]["datahist_norm"].plotOn( AllCtOverCVs[ kvkt ]["frame"] , RooFit.Invisible() , RooFit.Rescale(1.0/1.25) )
    for ii in sorted( whatToPlot.keys() , reverse=True ):
        plotit = whatToPlot[ii]
        plotit[0].plotOn( AllCtOverCVs[ kvkt ]["frame"]  , plotit[1] , plotit[2] ,  RooFit.LineStyle(1), RooFit.LineWidth(4) )
        
    AllCtOverCVs[ kvkt ]["canvas"] = TCanvas( "canvas_%g" % (kvkt) )
    AllCtOverCVs[ kvkt ]["frame"].Draw()

    fOut.cd()
    AllCtOverCVs[ kvkt ]["canvas"].Write()
    wsOut = RooWorkspace("ws%g" % (kvkt) )
    getattr( wsOut , "import")( AllCtOverCVs[ kvkt ]["signal"] )
    wsOut.Write()
    infile.Close()

fOut.Close()

