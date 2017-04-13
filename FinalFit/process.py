from ROOT import RooWorkspace, RooDataSet, RooPlot, RooRealVar, RooFit, RooExtendPdf, RooAbsPdf, RooFitResult, RooFormulaVar , RooGaussian, RooArgList, RooAddPdf, RooConstVar , RooArgSet
from ROOT import TFile, gSystem, TH1D, TCanvas,  kRed, kGreen, kBlack , TMath , TLegend, TGraphErrors
import re


f = TFile.Open("out.root")
ws = f.Get("testws")

vars = ws.allVars()
iter = vars.createIterator()
var = iter.Next()
while var :
    val = var.getVal()
    name = var.GetName()
    max = var.getMax()
    min = var.getMin()
    #var.Print()
    #print , var.getAsymErrorLo() , var.getAsymErrorHi(), var.getError(), var.getMin() , 
    if min > max or val < min or val > max :
        print name, min , val, max
    var = iter.Next()
    
funcs = ws.allFunctions()
iter = funcs.createIterator()
var = iter.Next()
while var :
    #var.Print()
    #print var.getVal(), var.getMin() , var.getMax()
    var = iter.Next()
