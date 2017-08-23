from ROOT import RooDataHist, RooFit , TFile, TH1D, RooArgList, RooRealVar, RooHistFunc, RooArgSet, TCanvas, RooWorkspace, RooDataSet
from SignalFit import nGaussians

List = ["JER", "JEC" , "metJerUncertainty" , "metUncUncertainty" , "metPhoUncertainty" , "metJecUncertainty" ,"UnmatchedPUWeight","MvaLinearSyst","LooseMvaSF","PreselSF","electronVetoSF","TriggerWeight","FracRVWeight","FracRVNvtxWeight","ElectronWeight","MuonWeight","MuonMiniIsoWeight","JetBTagCutWeight","JetBTagReshapeWeight"]
for sys in List :
    print sys, "lnN" , "thq"+sys, "-" , "tth"+sys, "vh"+sys , "thw"+sys
