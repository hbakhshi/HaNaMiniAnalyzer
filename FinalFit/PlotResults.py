from SignalFit import CtCvCpInfo
from ROOT import TFile, TTree, TObject
import os
import math
from ROOT import RooWorkspace, TCanvas , RooFit, TColor, kBlue, kRed, kGreen, gROOT,  TObjArray, TList, TGraph, Double, gPad

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
def PlotLimits():
    DIR = "./datacards/13May/ct%gcv%g/higgsCombineTest.Asymptotic.mH125.5.cv%g.ct%g.root"
    out = CtCvCpInfo("Results")

    for index in range( -1, 50):
        ct,cv,cp = out.GetCValues( index )
        path = DIR % (ct, cv , cv, ct )
        if os.path.exists( path ) :
            f = TFile.Open( path )
            limit = f.Get("limit")
            val = -100
            if not type(limit) == TTree :
                val = -200
            else :
                for i in limit :
                    if i.quantileExpected == 0.5 :
                        val = i.limit
            f.Close()
        else:
            val = -300

        print cv,ct, path, val
        out.SetValue( index , val )

    canvas = TCanvas()
    #out.hCtCv.SetContour(1)
    #out.hCtCv.SetContourLevel(0, 1)
    out.hCtCv.Draw("COLZ TEXT")
    return canvas, out.hCtCv
    out.hCtCv.Draw("CONT Z LIST")
    canvas.Update()
    gPad.Update()
    conts = gROOT.GetListOfSpecials().FindObject("contours")

    TotalConts = 0
    if conts:
        TotalConts = conts.GetSize()
    vg = vGraph( out.hCtCv )
    print TotalConts
    for i in range( 0 ,  TotalConts ) :
        contLevel = conts.At(i)
        for j in range(0 , contLevel.GetSize() ) :
            curv = contLevel.At(j)
            np = curv.GetN()
            vg.Add( TGraph(np) )
            x0 = Double()
            y0 = Double()
            for k in range(0,  np):
                curv.GetPoint(k, x0, y0)
                vg.AddPoint( j , k, x0 , y0 )
            # vg.g[j]->SetLineColor(h->GetLineColor());
            # vg.g[j]->SetLineStyle(h->GetLineStyle());
            # vg.g[j]->SetLineWidth(h->GetLineWidth());
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
a,b = PlotHiggsBkgs()
