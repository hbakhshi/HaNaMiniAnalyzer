from ROOT import RooWorkspace, RooDataSet, RooPlot, RooRealVar, RooFit, RooExtendPdf, RooAbsPdf, RooFitResult, RooFormulaVar , RooGaussian, RooArgList, RooAddPdf, RooConstVar , RooArgSet
from ROOT import TFile, gSystem, TH1D, TCanvas,  kRed, kGreen, kBlack , TMath , TLegend, TGraphErrors
import re
from math import sqrt

gSystem.Load("~/Desktop/tHq/HiggsAnalysis/CombinedLimit/lib/libHiggsAnalysisCombinedLimit.so")
from ROOT import RooMultiPdf, RooCategory

f = TFile.Open("CMS-HGG_multipdf_HggAnalysis_2016_THQ_InvertedTHMVACut.root")
ws = f.Get("multipdf")

newws = RooWorkspace("multipdf_inverted")

vars = ws.allVars()
iter = vars.createIterator()
var = iter.Next()
while var :
    #print var.GetName()
    if var.GetName()=="pdfindex_THQLeptonicTag_13TeV":
        getattr( newws , "import")( var.Clone("pdfindex_THQLeptonicTag_New_13TeV") , RooFit.RecycleConflictNodes() )
    else:
        getattr( newws , "import")( var.Clone() , RooFit.RecycleConflictNodes() )
    var = iter.Next()
                   
    
funcs = ws.allFunctions()
iter = funcs.createIterator()
var = iter.Next()
while var :
    getattr( newws , "import")( var.Clone() , RooFit.RecycleConflictNodes() )
    var = iter.Next()

data = ws.allData()
for var in data:
# iter = data.createIterator()
# var = iter.Next()
# while var :
    getattr( newws , "import")( var.Clone() , RooFit.RecycleConflictNodes())
    var = iter.Next()

a = RooArgList("pdfs")
cat = RooCategory("pdfindex_THQLeptonicTag_inverted_13TeV" , "title")
cat.Print()
pdfs = ws.allPdfs()
iter = pdfs.createIterator()
var = iter.Next()
while var :
    getattr( newws , "import")( var.Clone() , RooFit.RecycleConflictNodes())
    if var.GetName() in ["env_pdf_0_13TeV_bern1","env_pdf_0_13TeV_exp1","env_pdf_0_13TeV_pow1","env_pdf_0_13TeV_lau1"]:
        a.add( var )
    var = iter.Next()
multipdf = RooMultiPdf("CMS_hgg_THQLeptonicTag_inverted_13TeV_bkgshape" , "title" , cat , a )
getattr( newws , "import")( multipdf, RooFit.RecycleConflictNodes() )

f.Close()

fnew = TFile.Open("new.root" , "recreate")
newws.Write()
fnew.Close()
print "done"
