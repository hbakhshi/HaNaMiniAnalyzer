from SignalFit import CtCvCpInfo, KappaFramework
from ROOT import TFile, TTree, TObject, TLine, TLatex
import os
import stat
import math
import sys
from ROOT import RooWorkspace, TCanvas , RooFit, TColor, kBlue, kCyan,  kRed, kGreen, kYellow,kBlack, gROOT,  TObjArray, TList, TGraph, Double, gPad, RooWorkspace, RooArgList , RooAddPdf, TGraphAsymmErrors, kOrange, kAzure, kMagenta
import array

kappa = KappaFramework()

def PlotDS():
    CtCvCpIndex = CtCvCpInfo("temp")
    fIn = TFile.Open("out.root")
    ws = fIn.Get("ws")
    mvar = ws.var("CMS_hgg_mass")
    mvar.setRange( 115 , 135 )
    frame = mvar.frame()
    print CtCvCpIndex.AllCtCVs
    colors = {(1.,-1.):kBlue , (1.,1.):kRed , (1.,-3.):kGreen}
    for point in colors:
        index_ = -1
        if point in CtCvCpIndex.AllCtCVs:
            index = CtCvCpIndex.AllCtCVs.index( point )
            ds = ws.data("thw_125_13TeV_THQLeptonicTag_%d" % (index))

    
    
        ds.plotOn( frame , RooFit.LineColor(colors[point]) , RooFit.Rescale(1.0/ds.sumEntries()) , RooFit.Name("Cv%gCt%g" % point ) )

    c = TCanvas()
    frame.Draw()

objsToKeep = []
def PlotSignalShapes(Selection):
    f__ = TFile.Open( "datacards/22June/2dPlots.root")
    signal_fname_1 = ("signals/22June/out_{sample:s}_syst.root", "cms_hgg_13TeV" )
    signal_fname_2 = ("signals/22June/out_ctcv_{sample:s}_syst.root" , "ctcv" )
    samples = {"thw":signal_fname_2, "thq":signal_fname_2, "tth":signal_fname_1 , "vh":signal_fname_1 }
    purity_h_name = "{sample:s}/"+Selection+"/h{sample:s}_"+Selection+"_purity_CtCv"
    purities = RooArgList()
    signalshapes = RooArgList()

    ctOverCvs = []

    mVar = None
    ctovercv_vals = None
    for sample in samples :
        purity = CtCvCpInfo("purity_" + sample)
        ctovercv_vals = sorted(purity.AllCtOverCVs.keys())
        purity.FillFrom2DHisto( f__.Get( purity_h_name.format( sample=sample ) ) )
        purity.GetCtOverCv()
        purities.add( purity.CtOverCvDataHistFunc )
        objsToKeep.append( purity )

        sFile = TFile.Open( samples[sample][0].format( sample=sample ) )
        ws = sFile.Get( samples[sample][1] )
        pdf = ws.pdf("RV{sample:s}_mh125".format( sample=sample) )
        objsToKeep.append(sFile)
        objsToKeep.append(ws)
        objsToKeep.append(pdf)
        signalshapes.add( pdf )

        ctOverCvs.append( ws.var( "CtOverCv" ) )
        mVar = ws.var("CMS_hgg_mass")
        
    ret = RooAddPdf("signal" , "signal" , signalshapes , purities )
    objsToKeep.append( ret )
    plot = mVar.frame()
    options = ""
    for ctovercv in ctovercv_vals :
        for var in ctOverCvs:
            var.setVal( ctovercv )
        name = "name%g" % ctovercv
        ret.plotOn( plot , RooFit.DrawOption(options) , RooFit.Name(name) )
        
        c = TCanvas()
        plot.Draw()
        c.SaveAs("a.gif+")

        if not "same" in options :
            options += " same"

    return c
    
def PlotPDFs():
    fIn = TFile.Open("./hgg_card_13TeV_thq_moriond17_NoTHMVACut_onlythq.root")
    ws = fIn.Get("w")
    mvar = ws.var("CMS_hgg_mass")
    mvar.setRange( 115 , 135 )
    frame = mvar.frame()

    ct = ws.var("CT")
    cv = ws.var("CV")
    shape_thq = ws.pdf("shapeSig_thw_hgg_THQLeptonicTag2_13TeV")
    norm_thq = ws.function("shapeSig_thw_hgg_THQLeptonicTag2_13TeV__norm")
    norm_thq_plot = CtCvCpInfo("norm_thq_plot")

    Kvs = [1.0 , 1.5 , 0.5]
    KvKfs = {
        1.0:[3. , 2. , 1.5 , 1.25 ,  1.0, .75 , .5 , .25 , 0.0 , -0.25 , -0.5 , -0.75 , -1  , -1.25 , -1.5 , -2. , -3. ],
        1.5:[3. , 2. , 1.5 , 1.25 ,  1.0, .75 , .5 , .25 , 0.0 , -0.25 , -0.5 , -0.75 ,-1 , -1.25 , -1.5 , -2. , -3. ],
        .5:[3. , 2. , 1.5 , 1.25 ,  1.0, .75 , .5 , .25 , 0.0 , -0.25 , -0.5 , -0.75 ,-1 , -1.25 , -1.5 , -2. , -3. ]
    }

    NColors = 60
    Stops = [ 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000 ]
    Red   = [ 243./255., 243./255., 240./255., 240./255., 241./255., 239./255., 186./255., 151./255., 129./255.]
    Green = [  0./255.,  46./255.,  99./255., 149./255., 194./255., 220./255., 183./255., 166./255., 147./255. ]
    Blue  = [  6./255.,   8./255.,  36./255.,  91./255., 169./255., 235./255., 246./255., 240./255., 233./255. ]
    palette = {}
    index = 0
    for g in range(0, len(Red) ) :
        nColorsGradient = (math.floor(NColors*Stops[g]) - math.floor(NColors*Stops[g-1]))
        for c in range(0, int(nColorsGradient) ):
            color = TColor( 800+c ,
                            ( Red[g-1]   +  c * (Red[g]   - Red[g-1])  / nColorsGradient),
                            ( Green[g-1] +  c * (Green[g] - Green[g-1])/ nColorsGradient),
                            ( Blue[g-1]  +  c * (Blue[g]  - Blue[g-1]) / nColorsGradient) )
            palette[index] = 800+c
            index += 1

        index = 0

    for kv in Kvs:
        for kf in KvKfs[kv]:
            if not (kv,kf) in colors.keys():
                index += 1
                continue
            ct.setVal(kf)
            cv.setVal(kv)

            shape_thq.plotOn( frame , RooFit.LineColor(colors[(kv,kf)]) , RooFit.Name("Ct%gCv%g" % (kf, kv)) )
            index_ = -1
            if (kv,kf) in norm_thq_plot.AllCtCVs:
                index_ = norm_thq_plot.AllCtCVs.index( (kv , kf ) )
            norm_thq_plot.SetValue( index_ , norm_thq.getVal() )

            index += 1
    c = TCanvas("sahpes") 
    frame.Draw()

    #c2 = TCanvas("norm")
    #norm_thq_plot.hCtCv.Draw("COLZ TEXT")


class vGraph:
    def __init__(self , h):
        self.g = []
        self.C = TCanvas("Exclusion")
        self.h = h.Clone(h.GetName() + "_cloned" )
    def Add(self, g):
        self.g.append( g )

    def AddPoint(self, gIndex , pIndex , x , y ):
        self.g[gIndex].SetPoint( pIndex , x, y )
        
    def draw(self , h) :
        self.h = h
        self.C.cd()
        self.h.Draw("COLZ TEXT")
        for i in range(0, len(self.g) ):
            self.g[i].Draw("P")


vg = None
wrongFiles = {}
limits = {}
def Smoother( errors ):
    return errors
    i = 0
    ret = array.array('d')
    while i < len(errors) :
        a0 = errors[i]
        i += 1
        if i == len(errors) :
            ret.append( a0 )
            continue
        
        a1 = errors[i]
        i += 1
        
        a2 = errors[i]
        i+= 1
        
        normed = (a0+a1+a2)/3.
        ret.append( normed )
        ret.append( normed )
        ret.append( normed )

    #print errors
    #print ret
    return ret

def PlotLimits(Bin, color , style , date , canvas = None , dx = 0 , cv = 1):
    DIR = "./datacards/"+date+"/ctcv%g/higgsCombine" + Bin + ".Asymptotic.mH125.5.root"
    INPUT_FILE = "./datacards/"+date+"/ctcv%g/input.root"
    
    x = array.array('d')
    y = array.array('d')
    ex = array.array('d')
    ey1sigmap = array.array('d')
    ey1sigman = array.array('d')
    ey2sigmap = array.array('d')
    ey2sigman = array.array('d')
    
    out = CtCvCpInfo("ResultsMedian%s%s" % (date, Bin ) )
    out1sigmaP = CtCvCpInfo("Results1sigmaP%s%s" % (date,Bin) )
    out1sigmaM = CtCvCpInfo("Results1sigmaM%s%s" % (date,Bin) )

    nEvents = array.array('d')
    for ctcv in sorted(out.AllCtOverCVs):
        #ct,cv,cp = out.GetCValues( index )
        #if not ctcv in [ -1 ]:
        #    continue
        #CT = ct #0 if ct == 0 else -ct
        ct = ctcv

        print INPUT_FILE%(ctcv)
        input_file = TFile.Open( INPUT_FILE%( ctcv) )
        #input_file.ls()
        wsPreselection = input_file.Get("WSTHQLeptonicTag")
        xsec_ = 1*(kappa.GetXSecBR( "thq" , ct, cv , False )+kappa.GetXSecBR( "tth" , ct, cv , False )+kappa.GetXSecBR( "thw" , ct, cv , False )+kappa.GetXSecBR( "vh" , ct, cv , False ))
        kappa.SetCtCv( ct , cv )
        xsec = kappa.SumXSections.getVal()

        #wsPreselection.var("RVvh_mh125_norm").getVal() +
        nevents = ( wsPreselection.var("RVthq_mh125_norm").getVal() + 1.02*wsPreselection.var("RVtth_mh125_norm").getVal() + wsPreselection.var("RVthw_mh125_norm").getVal() + cv*cv*0.1)
        nEvents.append( nevents )
        #xsec2 = nevents / (35900. )
        input_file.Close()
        path = DIR % (ctcv)
        print path
        
        val = -100
        val1sigmap = -100
        val1sigmam = -100
        val2sigmap = -100
        val2sigmam = -100
        
        if os.path.exists( path ) :
            f = TFile.Open( path )
            if f :
                limit = f.Get("limit")
                if not type(limit) == TTree :
                    val = -200
                    val1sigmap = -200
                    val1sigmam = -200
                else :
                    for i in limit :
                        if i.quantileExpected == 0.5 :
                            val = i.limit
                        elif int(100*i.quantileExpected) in [15,16,17] :
                            val1sigmam = i.limit
                        elif int(100*i.quantileExpected) in [83,84,85] :
                            val1sigmap = i.limit
                        elif int(100*i.quantileExpected) in [2,3,4]:
                            val2sigmam = i.limit
                        elif int(100*i.quantileExpected) in [97,98,99]:
                            val2sigmap = i.limit
                        else :
                            print int(100*i.quantileExpected)
                f.Close()
            else :
                val = -400
                val1sigmap = -400
                val1sigmam = -400
        else:
            print path
            val = -300
            val1sigmap = -300
            val1sigmam = -300

        if val < 0 :
            if (ct , cv) in wrongFiles :
                wrongFiles[ (ct,cv) ].append( Bin )
            else :
                wrongFiles[ (ct,cv) ]=[Bin]
        else :
            if (ct , cv) in limits :
                limits[ (ct,cv) ][ Bin ] = val
            else :
                limits[ (ct,cv) ]= { Bin: val}
            
        print Bin, val, val1sigmam, val1sigmap, val2sigmam, val2sigmap
        if val <= 0 :
            val /= 1000
        
        #print cv,ct, path, val
        cv_ = out.AllCtOverCVs[ctcv].keys()[0]
        index = out.AllCtCVs.index( ( cv_ , ctcv*cv_) )
        if val < 0 :
            out.SetValue( index , val )
        else :
            #print Bin, "%.2f" % val, "+" , "%.2f" % abs(val2sigmap-val) , "-" , "%.2f" % abs(val2sigmam-val)
            out.SetValue( index , val )
            out1sigmaM.SetValue( index , val1sigmam )
            out1sigmaP.SetValue( index , val1sigmap )
            if val > 0 :
                x.append( ctcv+dx )
                y.append( val*xsec )
                ex.append(0)
                ey1sigmap.append( abs(val1sigmap-val)*xsec )
                ey1sigman.append( abs(val1sigmam-val)*xsec )
                ey2sigmap.append( abs(val2sigmap-val)*xsec )
                ey2sigman.append( abs(val2sigmam-val)*xsec )

    

    print x
    print y
    print ex
    print ey2sigman
    print ey2sigmap
    graph_2sigma = TGraphAsymmErrors( len(x) , x , y , ex , ex , Smoother(ey2sigman) , Smoother(ey2sigmap) )
    graph_2sigma.SetName( "GraphAsym_%s_2SigmaBand_%s" % (date , Bin ))
    graph_2sigma.SetTitle( Bin+ "(" +date+ ")" )
    graph_2sigma.SetLineColor( color )
    graph_2sigma.SetMarkerStyle( style )
    graph_2sigma.SetMarkerColor( color )
    graph_2sigma.SetFillColor( color )
    graph_2sigma.SetFillStyle( 3005 )

    graph_1sigma = TGraphAsymmErrors( len(x) , x , y , ex , ex , Smoother(ey1sigman) , Smoother(ey1sigmap) )
    graph_1sigma.SetName( "GraphAsym_%s_1SigmaBand_%s" % (date , Bin ) )
    graph_1sigma.SetTitle( Bin + "(" +date+ ")" )
    graph_1sigma.SetLineColor( color )
    graph_1sigma.SetMarkerStyle( style )
    graph_1sigma.SetMarkerColor( color )
    graph_1sigma.SetFillColor( color )
    graph_1sigma.SetFillStyle( 3005 )
    
    options = "P SAME"
    if canvas == None :
        canvas = TCanvas()
        options = "AP"
    #canvas.Divide(2,1)
    #canvas.cd(1)
    out.GetCtOverCv(color , style , dx=dx , IgnoreNegatives = False).Draw(options)
    #canvas.cd(2)
    #out.hCtCv.Draw("COLZ text")
    canvas.Update()

    graph_nevents = TGraph( len(nEvents) , x , nEvents )
    
    return canvas, out.CtOverCvGraph, out.hCtCv , graph_1sigma , graph_2sigma, graph_nevents

    arr = array.array('d' , [1,2,3] )
    out.hCtCv.SetContour(3 , arr)
    out.hCtCv.SetContourLevel(0,1)

    out.hCtCv.Draw("CONT Z LIST")
    canvas.Update()
    gPad.Update()
    conts = gROOT.GetListOfSpecials().FindObject("contours")

    TotalConts = 0
    if conts:
        TotalConts = conts.GetSize()
    else :
        print "contours is not set"
        
    vg = vGraph( out.hCtCv )
    print TotalConts
    for i in range( 0 ,  TotalConts ) :
        contLevel = conts.At(i)
        print contLevel.GetSize()
        for j in range(0 , contLevel.GetSize() ) :
            curv = contLevel.At(j)
            np = curv.GetN()
            vg.Add( TGraph(np) )
            x0 = Double()
            y0 = Double()
            for k in range(0,  np):
                curv.GetPoint(k, x0, y0)
                vg.AddPoint( -1 , k, x0 , y0 )
            vg.g[-1].SetLineColor(out.hCtCv.GetLineColor())
            vg.g[-1].SetLineStyle(out.hCtCv.GetLineStyle())
            vg.g[-1].SetLineWidth(out.hCtCv.GetLineWidth())
    vg.draw( out.hCtCv )
    print vg.h
    return vg, canvas

def PlotHiggsBkgs():
    DIR = "./datacards/13May/ct%gcv%g/input.root"
    out = CtCvCpInfo("HiggsBackgrounds")

    for index in range( -1, 50):
        ct,cv,cp = out.GetCValues( index )
        if not (ct == 1 and cv == 1):
            continue
        path = DIR % (ct, cv )
        if os.path.exists( path ) :
            f = TFile.Open( path )
            ws = f.Get("WS")
            val = 0

            vhVal = ws.var("RVvh_mh125_norm").getVal()
            tthVal = ws.var("RVtth_mh125_norm").getVal()
            #gghVal = ws.var("RVggh_mh125_norm").getVal()
            #vbfVal = ws.var("RVvbf_mh125_norm").getVal()
            print vhVal, tthVal
            val += (vhVal + tthVal ) # + gghVal + vbfVal)
            
            f.Close()
        else:
            val = -300

        print cv,ct, path, val
        out.SetValue( index , val )

    canvas = TCanvas()
    out.hCtCv.Draw("COLZ TEXT")
    return canvas, out.hCtCv
#a,b = PlotHiggsBkgs()

bins = {"Preselection":[2, 23 , 0 , "Preselection"],
        "THQLeptonicTHQTag":[3, 22 , 0.0005 , "|#eta_{forward jet}| > 2.5 + #jets=2 + #loose-bJets=1" ] , 
        "THQLeptonic":[2 , 21 , 0.001 , "Combined results when |#eta_{forward jet}|, #jet and #loose-bJets are used"] ,
        #"MVATHQ":[9,47 , 0.015 , "MVATHQ" ] , 
        #"MVA":[9,46 , 0.02 , "MVA Combined"] ,
        "EtaNJetTHQTag":[ 8 , 29 , 0.0025 , "|#eta_{forward jet}| > 2.5 + #jets=2" ] , 
        "EtaNJet":[ 29 , 30 , 0.03 , "Combined results when |#eta_{forward jet}| and #jet are used"] ,
        "EtaNbJetTHQTag":[ 46, 25 , 0.0035 , "|#eta_{forward jet}| > 2.5 + #loose-bJets=1" ] , 
        "EtaNbJet":[ 46 , 21 , 0.004 , "Combined results when |#eta_{forward jet}| and #loose-bJets are used"], 
        "NJetNbJetTHQTag":[ 30 , 2 , 0.0045 , "#jets=2 + #loose-bJets=1"] , 
        "NJetNbJet":[ 30 , 5 , 0.005 , "Combined results when #jet and #loose-bJets are used"]
}
canvas = None
graphs = []
graphs_sigma_bands = {}
dir_name = sys.argv[1]
bin_index = int( sys.argv[2] )
print bins.keys()
bin = bins.keys()[bin_index]
plotInfo = bins[bin]
if bin in ["THQLeptonicTHQTag" , "MVATHQ" , "EtaNJetTHQTag" , "EtaNbJetTHQTag" , "NJetNbJetTHQTag" ] and "CRInvLepCut" in dir_name :
    bin = "CRInvertLepCut" + bin
if "CRInvLepCut" in dir_name :
   plotInfo[3] += " (CR)" 
#for bin in bins :
canvas, b, c , onesigma , twosigma , nevents = PlotLimits( bin , plotInfo[0] , plotInfo[1] , dir_name , canvas , plotInfo[2] )
graphs.append( b )
graphs.append( c )
graphs_sigma_bands[(bin,dir_name)] = ( onesigma , twosigma )


frame = kappa.CtOverCv.frame()
kappa.SumXSections.plotOn( frame , RooFit.DrawOption("same") , RooFit.LineColor(kOrange+1))
frame.SetAxisRange( -6 , 6 , "X" )
frame.SetAxisRange( 0.0001 , 1. , "Y" )

# kappa.BRGammaGamma.plotOn( frame , RooFit.DrawOption("same") )
# kappa.tHqXSecValue.plotOn( frame , RooFit.LineColor(kGreen+2), RooFit.DrawOption("same") )
# kappa.tHWXSecValue.plotOn( frame , RooFit.LineColor(kOrange+1), RooFit.DrawOption("same") )
# kappa.ttHXSecValue.plotOn( frame , RooFit.LineColor(kAzure+6), RooFit.DrawOption("same") )
# kappa.vHXSecValue.plotOn( frame , RooFit.LineColor(kMagenta+3), RooFit.DrawOption("same") )

#kappa2 = KappaFramework()
#kappa2.SetCtCv( 2 , 2 )
#kappa2.SumXSections.plotOn( frame ,  RooFit.LineColor(kGreen+2), RooFit.DrawOption("same") )

# frame2 = kappa.CV.setRange( 0 , 10 )
# frame2 = kappa.CV.frame()
# kappa.SumXSections.plotOn( frame2 ,  RooFit.LineColor(kMagenta+3) )
# kappa.BRGammaGamma.plotOn( frame , RooFit.DrawOption("same")  )
# kappa.tHqXSecValue.plotOn( frame , RooFit.LineColor(kGreen+2), RooFit.DrawOption("same") )
# kappa.tHWXSecValue.plotOn( frame , RooFit.LineColor(kOrange+1), RooFit.DrawOption("same") )
# kappa.ttHXSecValue.plotOn( frame , RooFit.LineColor(kAzure+6), RooFit.DrawOption("same") )
# kappa.vHXSecValue.plotOn( frame , RooFit.LineColor(kMagenta+3), RooFit.DrawOption("same") )


canvas2 = TCanvas("sigma_bands")
options = "ap"
x_intersection = -7
min_distance=1000000
nsteps , stepsize = 10000 , 6./10000
for i in range(0,nsteps):
    ctOvercv = -6.+i*stepsize
    kappa.SetCtCv( ctOvercv , 1 )
    xsec = kappa.SumXSections.getVal()

    limit = onesigma.Eval( ctOvercv )

    distance = abs( limit - xsec )
    if distance < min_distance :
        x_intersection = ctOvercv
        min_distance = distance

kappa.SetCtCv( -1 , 1 )        
limitAtNegativeOne = onesigma.Eval( -1 )/kappa.SumXSections.getVal()

for bin_ in graphs_sigma_bands :
    graphs_sigma_bands[bin_][1].SetLineColor( kYellow-4)
    graphs_sigma_bands[bin_][1].SetFillColor( kYellow -4)
    graphs_sigma_bands[bin_][1].SetFillStyle( 1001 )
    graphs_sigma_bands[bin_][1].SetTitle( plotInfo[3] )
    graphs_sigma_bands[bin_][1].Draw( "a3" )
    graphs_sigma_bands[bin_][1].GetYaxis().SetRangeUser( 0.00004 ,0.8 )
    graphs_sigma_bands[bin_][1].GetXaxis().SetRangeUser( -6.0 , 6.0 )
    graphs_sigma_bands[bin_][1].GetHistogram().GetXaxis().SetTitle( "c_{t}/c_{v}")
    graphs_sigma_bands[bin_][1].GetHistogram().GetYaxis().SetTitle( "pb")

    graphs_sigma_bands[bin_][0].SetLineColor( kGreen - 4)
    graphs_sigma_bands[bin_][0].SetFillColor( kGreen -4)
    graphs_sigma_bands[bin_][0].SetFillStyle( 1001 )
    graphs_sigma_bands[bin_][0].Draw( "3 same" )

    graphs_sigma_bands[bin_][0].SetLineColor( kBlack )
    graphs_sigma_bands[bin_][0].SetLineWidth( 2 )
    graphs_sigma_bands[bin_][0].SetLineStyle( 2 )

    graphs_sigma_bands[bin_][0].SetMarkerColor( kBlack )
    graphs_sigma_bands[bin_][0].SetMarkerStyle( 0 )
    graphs_sigma_bands[bin_][0].Draw("lp X")
    #if not "same" in options :
    #    options = "same p"
frame.Draw("SAME")

lineNegativeOne = TLine( -6 , onesigma.Eval( -1 ) , -1 , onesigma.Eval( -1 ) )
lineNegativeOne.SetLineColor( kCyan - 8 )
lineNegativeOne.SetLineStyle( 4 )
lineNegativeOne.SetLineWidth( 4 )
lineNegativeOne.Draw()

lineNegativeOneVertical = TLine( -1 , 0 , -1 , onesigma.Eval( -1 ) )
lineNegativeOneVertical.SetLineColor( kCyan - 8 )
lineNegativeOneVertical.SetLineStyle( 4 )
lineNegativeOneVertical.SetLineWidth( 4 )
lineNegativeOneVertical.Draw()

lineIntersection = TLine( x_intersection , 0 , x_intersection , onesigma.Eval( x_intersection ) )
lineIntersection.SetLineColor( kBlue )
lineIntersection.SetLineStyle( 5 )
lineIntersection.SetLineWidth( 2 )
lineIntersection.Draw()

lineIntersectionHorizontal = TLine( -6 , onesigma.Eval( x_intersection ) , x_intersection , onesigma.Eval( x_intersection ) )
lineIntersectionHorizontal.SetLineColor( kBlue )
lineIntersectionHorizontal.SetLineStyle( 5 )
lineIntersectionHorizontal.SetLineWidth( 2 )
lineIntersectionHorizontal.Draw()

InfoBox = TLatex()
InfoBox.SetNDC()
InfoBox.SetTextSize(0.03)
InfoBox.DrawLatex(0.14,0.85, "c_{t}/c_{v} < %.2f is excluded"%(x_intersection))
InfoBox.DrawLatex(0.14,0.8, "r(c_{t}/c_{v}=-1) = %.2f"%(limitAtNegativeOne))


canvas2.SetLogy()
canvas2.SaveAs( "datacards/%s/%s.pdf" % (dir_name , bin) )

class BinDatacard:
    def __init__(self, binName):
        self.BinName = binName

def ProduceSubmitFileForMissingJobs ():        
    Preselection = BinDatacard( "THQLeptonicTag" )
    AllBins = {}
    AllBins["THQLeptonic"] = {"THQ":BinDatacard( "THQLeptonicTHQTag" ) ,
                              "TTH":BinDatacard( "THQLeptonicTTHTag" ) }
    AllBins["MVA"] = { "THQ":BinDatacard("MVATHQ"),
                       "TTH":BinDatacard("MVATTH") }
    AllBins["EtaNJet"] = {"THQ":BinDatacard("EtaNJetTHQTag"),
                          "TTH":BinDatacard("EtaNJetTTHTag") }
    AllBins["EtaNbJet"] = {"THQ":BinDatacard("EtaNbJetTHQTag"),
                           "TTH":BinDatacard("EtaNbJetTTHTag") }
    AllBins["NJetNbJet"] = {"THQ":BinDatacard("NJetNbJetTHQTag"),
                            "TTH":BinDatacard("NJetNbJetTTHTag") }
    
    submitLx = open( "./datacards/15June/submit2.sh" , "w")
    for kf,kv in wrongFiles :
        dirname = "./datacards/15June/ct%gcv%g" % (kf, kv)
        
        fRun = open( dirname + "/run2.sh" , "w" )
        fRun.write("cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/src/FinalFit\n")
        fRun.write("eval `scramv1 runtime -sh`\n")
        fRun.write("cd %s\n" % (dirname) )

        if "Preselection" in wrongFiles[(kf,kv)]:
            fRun.write("text2workspace.py Bin%s.txt\n" % (Preselection.BinName))
            fRun.write("combine -n Preselection  -M  Asymptotic Bin%s.root --run=blind -m 125 --ct=%g --cv=%g\n" % (Preselection.BinName, kf,kv) )

        for Bin in AllBins:
            fRun.write("text2workspace.py Bin%s.txt\n" % (AllBins[Bin]["THQ"].BinName) )
            if AllBins[Bin]["THQ"].BinName in wrongFiles[(kf,kv)]:
                fRun.write("combine -n %s  -M  Asymptotic Bin%s.root --run=blind -m 125 --ct=%g --cv=%g\n" % (AllBins[Bin]["THQ"].BinName,AllBins[Bin]["THQ"].BinName,kf,kv) )
            
            fRun.write("combineCards.py Bin%s.txt Bin%s.txt > Combined%s.txt\n" % (AllBins[Bin]["THQ"].BinName, AllBins[Bin]["TTH"].BinName, Bin) )
            fRun.write("text2workspace.py Combined%s.txt\n" % (Bin) )
            if Bin in wrongFiles[(kf,kv)]:
                fRun.write("combine -n %s -M Asymptotic Combined%s.root --run=blind -m 125 --ct=%g --cv=%g\n" % (Bin , Bin , kf,kv) )

        fRun.close()
        st = os.stat(dirname + "/run2.sh")
        os.chmod(dirname + "/run2.sh", st.st_mode | stat.S_IEXEC)

        submitLx.write( "cd %s\n" % ("ct%gcv%g" % (kf, kv)) )
        submitLx.write( "bsub -J %s -o out -q 1nd run2.sh\n" % "ct%gcv%g" % (kf, kv) )
        submitLx.write( "cd ..\n" )
    
        submitLx.close()

