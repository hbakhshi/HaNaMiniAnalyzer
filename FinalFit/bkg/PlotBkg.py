import os
import sys
import stat
import math
import shutil
from ROOT import  TFile, TTree, TObject, RooWorkspace, TCanvas , RooFit, TColor, kBlue, kRed, kGreen, RooRealVar, RooConstVar, gROOT, RooAbsArg, RooRealVar, gSystem, RooFit , kOrange, kYellow , kCyan , RooArgSet , RooExtendPdf

gSystem.Load("~/Desktop/tHq/HiggsAnalysis/CombinedLimit/lib/libHiggsAnalysisCombinedLimit.so")

colors = [ kRed , kBlue, kGreen , kYellow , kCyan , kOrange , kRed + 4 , kBlue+ 4, kGreen+ 4 , kYellow+ 4 , kCyan+ 4 , kOrange+ 4 , kRed- 4 , kBlue- 4, kGreen- 4 , kYellow- 4 , kCyan- 4  , kOrange- 4]

fbkgName = sys.argv[1]
fbkg = TFile.Open( fbkgName )
ws = fbkg.Get("multipdf")
wsname = "CMS_hgg_%s_13TeV_bkgshape" % (sys.argv[2])
multipdf = ws.pdf( wsname )
norm = ws.arg( wsname + "_norm")
norm.Print()
mass_var = multipdf.getVariables().first()
mass_var.setRange("HiggsMassWindow5",120,130)
mass_var.setRange("HiggsMassWindow2",123,127)
mass_var.setRange("HiggsMassWindow10",115,135)
mass_var.setRange("WholeRange",100,180)
frame = mass_var.frame()
option = "AL"
pdf_information = {}

multipdf.plotOn( frame )
for pdf_index in range(0,multipdf.getNumPdfs()):
    pdf_ = multipdf.getPdf( pdf_index )
    print pdf_.GetName() + "_Normalized" , pdf_.GetTitle()
    pdf = RooExtendPdf( pdf_.GetName() + "_Normalized" , pdf_.GetTitle() , pdf_ , norm )
    pdf.plotOn( frame , RooFit.DrawOption(option) , RooFit.LineColor( colors[pdf_index] ) , RooFit.LineStyle(0) , RooFit.LineWidth(3) , RooFit.Range("WholeRange") )
    totalInt = pdf.createIntegral( RooArgSet(mass_var) ,RooFit.Range("WholeRange"))
    #totalInt.Print() , RooFit.NormSet( RooArgSet(mass_var) ),
    fracInt5 = pdf.createIntegral( RooArgSet(mass_var) ,RooFit.Range("HiggsMassWindow5"))
    fracInt2 = pdf.createIntegral( RooArgSet(mass_var) ,RooFit.Range("HiggsMassWindow2"))
    fracInt10 = pdf.createIntegral( RooArgSet(mass_var) ,RooFit.Range("HiggsMassWindow10"))
    #fracInt.Print()
    if "A" in option :
        option = "L"
    pdf_information[ pdf_index ] = { "name":pdf.GetName() , "pdf":pdf , "ratio5":fracInt5.getVal()/totalInt.getVal(), "ratio2":fracInt2.getVal()/totalInt.getVal(), "ratio10":fracInt10.getVal()/totalInt.getVal() }

doSig = False
if len(sys.argv) > 3 :
    fsigName = sys.argv[2]
    fsig = TFile.Open( fsigName )
    sigPdf = fsig.Get( sys.argv[3] )
    doSig = True


canvas = TCanvas("MultiPDF")
frame.Draw()

for pdf in pdf_information :
    print pdf_information[pdf]["name"] , "%.2f%%" % (100*pdf_information[pdf]["ratio2"]), "%.2f%%" % (100*pdf_information[pdf]["ratio5"]), "%.2f%%" % (100*pdf_information[pdf]["ratio10"])
