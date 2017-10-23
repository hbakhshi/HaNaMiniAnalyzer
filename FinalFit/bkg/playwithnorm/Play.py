from ROOT import TFile, RooWorkspace, gSystem, RooRealVar, RooFit

gSystem.Load("~/Desktop/tHq/HiggsAnalysis/CombinedLimit/lib/libHiggsAnalysisCombinedLimit.so")

fIn = TFile.Open("THQLeptonicTag.root")
ws_in = fIn.Get("multipdf")

mpdf_In = ws_in.arg("CMS_hgg_THQLeptonicTag_13TeV_bkgshape")
norm_In = ws_in.arg("CMS_hgg_THQLeptonicTag_13TeV_bkgshape_norm")
norm_In.Print()
norm_In_val = norm_In.getValV()


fOut = TFile.Open("MultiWeights.root" , "RECREATE")
workspaces = []

for i in range( 1 , 21 ):
    ws = RooWorkspace("ws%d" % i )
    workspaces.append( ws )
    
    new_norm = norm_In_val*float(i)/20.0
    norm_In.setVal( new_norm )
    norm_In.setRange( 0 , 3*new_norm )

    getattr( ws , "import")( norm_In , RooFit.Silence() )
    getattr( ws , "import")( mpdf_In , RooFit.Silence() )

    ws.Write()

fOut.Close()

    

