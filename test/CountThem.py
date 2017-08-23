from tHqAnalyzer.HaNaMiniAnalyzer.Property import *
from ROOT import TFile, Double

File = TFile.Open( "out_fgg_FromLeptonSele2_normtolumi.root" )
CutDirName = "DiG2J1TLeptons/PlottedVars/mGG"
PropDir = File.GetDirectory( CutDirName )
print PropDir

Prop = Property.FromDir( PropDir )

error = Double()
data = Prop.Data.IntegralAndError( 0 , 100 , error )
print "data:",data , "+=", error

for sample in Prop.Samples :
    integral = sample.IntegralAndError( 0 , 100 , error )
    print sample.GetName(),integral , "+-", error    

print "------------------"
    
for bkg in Prop.Bkg :
    integral = Prop.Bkg[bkg].IntegralAndError( 0 , 100 , error )
    print bkg,integral , "+-", error
