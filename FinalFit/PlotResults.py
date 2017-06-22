from SignalFit import CtCvCpInfo, KappaFramework
from ROOT import TFile, TTree, TObject
import os
import stat
import math
from ROOT import RooWorkspace, TCanvas , RooFit, TColor, kBlue, kRed, kGreen, gROOT,  TObjArray, TList, TGraph, Double, gPad, RooWorkspace
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
def PlotLimits(Bin, color , style , canvas = None , dx = 0):
    DIR = "./datacards/15June/ct%gcv%g/higgsCombine" + Bin + ".Asymptotic.mH125.5.root"
    INPUT_FILE = "./datacards/15June/ct%gcv%g/input.root"
    out = CtCvCpInfo("ResultsMedian%s" % Bin)
    out1sigmaP = CtCvCpInfo("Results1sigmaP%s" % Bin)
    out1sigmaM = CtCvCpInfo("Results1sigmaM%s" % Bin)

    for index in range( -1 , 50):
        ct,cv,cp = out.GetCValues( index )
        #if not ct/cv == -1 :
        #    continue
        CT = ct #0 if ct == 0 else -ct
        input_file = TFile.Open( INPUT_FILE%( CT , cv) )
        wsPreselection = input_file.Get("WSTHQLeptonicTag")
        xsec2 = 1*(kappa.GetXSecBR( "thq" , ct, cv , False )+0.5071*kappa.GetXSecBR( "tth" , ct, cv , False )+kappa.GetXSecBR( "thw" , ct, cv , False ))

        kappa.SetCtCv( ct , cv )
        xsec = (wsPreselection.var("RVvh_mh125_norm").getVal() + wsPreselection.var("RVthq_mh125_norm").getVal() + wsPreselection.var("RVtth_mh125_norm").getVal() + wsPreselection.var("RVthw_mh125_norm").getVal()) / (xsec2*35900 )
        input_file.Close()
        path = DIR % (CT, cv)
        if os.path.exists( path ) :
            f = TFile.Open( path )
            limit = f.Get("limit")
            val = -100
            val1sigmap = -100
            val1sigmam = -100
            if not type(limit) == TTree :
                val = -200
                val1sigmap = -200
                val1sigmam = -200
            else :
                for i in limit :
                    if i.quantileExpected == 0.5 :
                        val = i.limit
                    elif i.quantileExpected == 0.16 :
                        val1sigmam = i.limit
                    elif i.quantileExpected == 0.84 :
                        val1sigmap = i.limit
            f.Close()
        else:
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
            
        if val <= 0 :
            continue
        
        print cv,ct, path, val
        out.SetValue( index , val*xsec )
        out1sigmaM.SetValue( index , val1sigmam*xsec )
        out1sigmaP.SetValue( index , val1sigmap*xsec )

    options = "P SAME"
    if canvas == None :
        canvas = TCanvas()
        options = "AP"
    #canvas.Divide(2,1)
    #canvas.cd(1)
    out.GetCtOverCv(color , style , dx=dx).Draw(options)
    #canvas.cd(2)
    #out.hCtCv.Draw("COLZ text")
    canvas.Update()

    return canvas, out.CtOverCvGraph, out.hCtCv

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

bins = {"Preselection":(2, 23 , 0) ,
        "THQLeptonicTHQTag":(3, 22 , 0.005 ) , 
        "THQLeptonic":(3 , 21 , 0.01) ,
        "MVATHQ":(9,47 , 0.015) , 
        "MVA":(9,46 , 0.02) ,
        "EtaNJetTHQTag":( 8 , 29 , 0.025 ) , 
        "EtaNJet":( 8 , 30 , 0.03) ,
        "EtaNbJetTHQTag":( 46, 25 , 0.035 ) , 
        "EtaNbJet":( 46 , 21 , 0.04) ,
        "NJetNbJetTHQTag":( 30 , 2 , 0.045 ) , 
        "NJetNbJet":( 30 , 5 , 0.05 ) }
canvas = None
graphs = []
for bin in bins :
    canvas, b, c = PlotLimits( bin , bins[bin][0] , bins[bin][1] , canvas , bins[bin][2] )
    graphs.append( b )
    graphs.append( c )


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
            fRun.write("combine -n Preselection  -M  Asymptotic Bin%s.root --run=blind -m 125.5 --ct=%g --cv=%g\n" % (Preselection.BinName, kf,kv) )

        for Bin in AllBins:
            fRun.write("text2workspace.py Bin%s.txt\n" % (AllBins[Bin]["THQ"].BinName) )
            if AllBins[Bin]["THQ"].BinName in wrongFiles[(kf,kv)]:
                fRun.write("combine -n %s  -M  Asymptotic Bin%s.root --run=blind -m 125.5 --ct=%g --cv=%g\n" % (AllBins[Bin]["THQ"].BinName,AllBins[Bin]["THQ"].BinName,kf,kv) )
            
            fRun.write("combineCards.py Bin%s.txt Bin%s.txt > Combined%s.txt\n" % (AllBins[Bin]["THQ"].BinName, AllBins[Bin]["TTH"].BinName, Bin) )
            fRun.write("text2workspace.py Combined%s.txt\n" % (Bin) )
            if Bin in wrongFiles[(kf,kv)]:
                fRun.write("combine -n %s -M Asymptotic Combined%s.root --run=blind -m 125.5 --ct=%g --cv=%g\n" % (Bin , Bin , kf,kv) )

        fRun.close()
        st = os.stat(dirname + "/run2.sh")
        os.chmod(dirname + "/run2.sh", st.st_mode | stat.S_IEXEC)

        submitLx.write( "cd %s\n" % ("ct%gcv%g" % (kf, kv)) )
        submitLx.write( "bsub -J %s -o out -q 1nd run2.sh\n" % "ct%gcv%g" % (kf, kv) )
        submitLx.write( "cd ..\n" )
    
        submitLx.close()

