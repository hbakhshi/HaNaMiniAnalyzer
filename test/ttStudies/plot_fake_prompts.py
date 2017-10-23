from ROOT import TFile, TH2, Double , TCanvas, kRed , kBlue , kOrange , kGreen , Double, TBrowser
from math import sqrt
selections = ["DiG2J" , "DiG2J1T" , "DiGNoLeptons" , "SR" ]
variables = ["diphoMVA" , "CMShggmass"]
frmt = "{sel}/PlottedVars/{var}/samples/{sample}_{fakeprompt}_{sel}_{var}_0"
samples = {"TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8":(kRed, "TTJets(amc@nlo)") , "TTGJets":(kBlue ,"TTGJets") , "TTGG":(kOrange, "TTGG") , "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":(kGreen, "TTJets(MG)" ) }
fakeprompts = ["fp" , "pp" , "ff"]

fOut = TFile.Open( "out_plots_fakeprompts.root" , "recreate" )
fIn = TFile.Open("out_allTopSamples_mvaonly.root")
for sel in selections :
    fOut.mkdir( sel ).cd()
    for varname in variables :
        for fp in fakeprompts :
            c = TCanvas( varname + "_" + fp )
            option = ""
            for sample,info in samples.items() :
                color = info[0]
                title = info[1]
                name = frmt.format( fakeprompt=fp , sel=sel , var=varname , sample=sample )
                h = fIn.Get( name )
                h.SetLineColor( color )
                h.SetMarkerColor( color )
                h.SetTitle( title )
                err = Double(0)
                integral = h.IntegralAndError( 0 , 1000 , err )
                if integral > 0 :
                    if err/integral < 0.3 :
                        h.DrawNormalized( option )
                        if "same" not in option :
                            option += " same"

            c.Write()


allTemplates = { "NormMG" :{ "ff":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "DiG2J1T" ),
                             "fp":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTGJets" , "DiG2J1T" ),
                             "pp":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTGG" , "DiG2J1T") ,
                             "color":kRed },
                 "NormAMC":{ "ff":( "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "SR" , "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "DiG2J1T" ),
                             "fp":( "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "SR" , "TTGJets" , "DiG2J1T" ),
                             "pp":( "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "SR",  "TTGG" , "DiG2J1T" ) ,
                             "color":kBlue },
                 "MG2J1T" :{ "ff":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "DiG2J1T" ),
                             "fp":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "DiG2J1T" ),
                             "pp":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "DiG2J1T"),
                             "color" : kGreen },
                 "AMC":{ "ff":( "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "SR" , "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "DiG2J1T" ),
                         "fp":( "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "SR" , "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "DiG2J1T" ),
                         "pp":( "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "SR",  "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "DiG2J1T" ),
                         "color" : kBlue+4},
                 "MGSR" :{ "ff":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" ),
                           "fp":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" ),
                           "pp":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR") ,
                           "color":kRed-3},
                 "NormMG_GG" :{ "ff":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "DiG2J1T" ),
                                "fp":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTGG" , "DiG2J1T" ),
                                "pp":( "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" , "SR" , "TTGG" , "DiG2J1T") ,
                                "color":kRed+3 },
                 "NormAMC_GG":{ "ff":( "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "SR" , "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "DiG2J1T" ),
                                "fp":( "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "SR" , "TTGG" , "DiG2J1T" ),
                                "pp":( "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8" , "SR",  "TTGG" , "DiG2J1T" ) ,
                                "color":kBlue },
                 
                 }
for varname in variables :
    fOut.mkdir( varname ).cd()
    c = TCanvas( varname )
    option = ""
    color_ = 0
    allHistos = {}
    for fp in fakeprompts :
        for sample,info in samples.items() :
            for sel in selections:
                color = info[0]
                title = info[1]
                name = frmt.format( fakeprompt=fp , sel=sel , var=varname , sample=sample )
                h = fIn.Get( name )
                h.SetLineColor( color + color_ )
                h.SetMarkerColor( color + color_ )
                h.SetTitle( title + "," + fp )
                err = Double(0)
                integral = h.IntegralAndError( 0 , 1000 , err )
                allHistos[(sample,fp,sel)] = (h , integral , err)
                if sel == "DiG2J":
                    if integral > 0 :
                        if err/integral < 0.3 :
                            h.DrawNormalized( option )
                            if "same" not in option :
                                option += " same"

        color_ += 2

    c.Write()
    for name,template in allTemplates.items():
        nFF = allHistos[ (template["ff"][0] , "ff" , template["ff"][1] ) ][1]
        hFF = allHistos[ (template["ff"][2] , "ff" , template["ff"][3] ) ][0].Clone( name )
        hFF.Scale( nFF/hFF.Integral() )
        hFF.SetLineColor( template["color"] )
        hFF.SetMarkerColor( template["color"] )
        hFF.SetTitle( name )
        
        nPF = allHistos[ (template["fp"][0] , "fp" , template["ff"][1] ) ][1]
        hPF = allHistos[ (template["fp"][2] , "fp" , template["ff"][3] ) ][0].Clone( name )
        hPF.Scale( nPF/hPF.Integral() )
        hFF.Add( hPF )

        nPP = allHistos[ (template["pp"][0] , "pp" , template["ff"][1] ) ][1]
        hPP = allHistos[ (template["pp"][2] , "pp" , template["ff"][3] ) ][0].Clone( name )
        hPP.Scale( nPP/hPP.Integral() )
        hFF.Add( hPP )

        hFF.Write()
            
fIn.Close()

b = TBrowser()
fOut.Browse(b)
#fOut.Close()
