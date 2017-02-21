from ROOT import TFile, TDirectory, gDirectory, TH1

f = TFile.Open("out_ex2j1tleptonbdt_normtolumi.root")
f.cd("Lepton/jPt/samples")
gDirectory.ls()

for a in gDirectory.GetListOfKeys():
    #print a.GetName()
    h = gDirectory.Get( a.GetName() )
    h.Print("base")
    
