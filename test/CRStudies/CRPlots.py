from ROOT import TFile, TH1F, TDirectory , TCanvas, kRed, TLegend , kBlue, TH1 ,TH1D, TH1F, gROOT
import math

gROOT.SetBatch( True )
Regions = { "SR": { "filename":"/home/hbakhshi/Desktop/tHq/Analyzer/test/CRStudies/out_CRPlots_test.root" , "dirname":"SR" },
            "CRInvertLepCut": { "filename":"/home/hbakhshi/Desktop/tHq/Analyzer/test/CRStudies/out_CRPlots_test.root" , "dirname":"CRInvertLepCut" },
            "DiG2J1T": { "filename":"/home/hbakhshi/Desktop/tHq/Analyzer/test/CRStudies/out_CRPlots_test.root" , "dirname":"DiG2J1T" }
}

Categories = {"EtaJP_NJ":{},"EtaJP_NbJ":{},"NJ_NbJ":{},"NJ_NbJ_EtaJP":{}}

plots = {
    "ggMass":["PlottedVars/mGG"] ,
    #"etajprime":["fwdjet1/fwdjet1eta"],
    "njets":["PlottedVars/nJets"],
    "nlbjets":["PlottedVars/nlbjets"],
    "fwdjet":["PlottedVars/jprimeeta"],
    "One":["PlottedVars/One"]
}

def GetPlots(dir_, r_info , name):
    for plot in plots :
        print name , plot
        prop_dir = plots[plot][0]
        upperdirname = prop_dir.split("/")[0]
        propname = prop_dir.split("/")[1]
        Dir_=dir_.GetDirectory(upperdirname)
        Dir_=Dir_.GetDirectory(propname)
        catDir = Dir_.GetDirectory("cats" )
        sumMC = catDir.Get("SumMC")
        datahistname = dir_.GetName() + "_" + propname + "_Data"
        tophistname  = dir_.GetName() + "_" + propname + "_Top"
        #if name != "main" :
        #    datahistname = r_info["dirname"] + "_" + name[0] + "_" + propname + "_Data"
        # print datahistname
        # catDir.ls()
        data = catDir.Get( datahistname )
        tophist = catDir.Get( tophistname )
        if name in r_info :
            r_info[name][ plot ] = {"dir":dir_ , "SumMC":sumMC , "Data":data , "Top":tophist}
        else :
            r_info[name] = {plot:{"dir":dir_ , "SumMC":sumMC , "Data":data  , "Top":tophist} }

        #sumMC.Print()
        #data.Print()
        if plot == "One" :
            error = 0
            mc = tophist if r_info["dirname"] == "DiG2J1T" else sumMC
            if mc.GetBinContent(1) != 0 :
                error = mc.GetBinError(1)/mc.GetBinContent(1)
            r_info[name]["yields"] = {"SumMC":mc.GetBinContent(1) , "SumMCError":error , "Data":data.GetBinContent(1) }
            if name != "main":
                mains = r_info["main"]["yields"]
                r_info[name]["eff"] = {"SumMC":mc.GetBinContent(1)/mains["SumMC"] , "SumMCError":math.sqrt(error*error + mains["SumMCError"]*mains["SumMCError"])  , "Data":data.GetBinContent(1)/mains["Data"] }
        


for region in Regions :
    r_info = Regions[region]
    f = TFile.Open( r_info["filename"] )
    r_info["file"] = f

    dir_ = f.GetDirectory( r_info["dirname"] )
    GetPlots( dir_ , r_info , "main" )
    
    for category in Categories :
        for signal in ["THQ" , "TTH"] :
            dirname = r_info["dirname"] + "_" + category + "_" + signal
            dir_ = f.GetDirectory( dirname )
            GetPlots( dir_ , r_info , (category, signal) )

            Categories[category][ (region, signal) ] = { "data" : TH1D( "data_eff_" + category + "_" + region + "_" + signal , "Eff. of " + category + " in " + region + " in data" , 1 , 0 , 1 ) ,
                                                         "mc"   : TH1D( "mc_eff_" + category + "_" + region  + "_" + signal, "Eff. of " + category + " in " + region + " in MC" , 1 , 0 , 1 ) }
            Categories[category][ (region, signal) ]["data"].SetBinContent(1 , r_info[ (category, signal) ]["eff"]["Data"] )
            Categories[category][ (region, signal) ]["mc"].SetBinContent(1 , r_info[ (category, signal) ]["eff"]["SumMC"] )
            Categories[category][ (region, signal) ]["mc"].SetBinError(1 , r_info[ (category, signal) ]["eff"]["SumMCError"] )

CRNames = [ name for name in Regions if name != "SR" ]
fOut = TFile.Open("fCRPlots_Data.root" , "RECREATE")
fOut.mkdir("DistrbutionsBeforeSelection").cd()
for plot in plots :
    for CR in CRNames:
        c = TCanvas()
        c.SetName( "Canvas_" + plot + "_" + CR )
        c.SetTitle(plot + " " + CR)

        Regions["SR"][ "main" ][ plot ]["SumMC"].SetLineStyle(0)
        Regions["SR"][ "main" ][ plot ]["SumMC"].SetLineColor(kRed)
        Regions[CR][ "main" ][ plot ]["SumMC"].SetLineStyle(0)
        Regions[CR][ "main" ][ plot ]["SumMC"].SetLineColor(kBlue)

        Regions["SR"][ "main" ][ plot ]["SumMC"].Scale( 1./ Regions["SR"][ "main" ][ plot ]["SumMC"].Integral() )
        Regions["SR"][ "main" ][ plot ]["SumMC"].SetMaximum(1)
        Regions["SR"][ "main" ][ plot ]["SumMC"].SetMinimum(-0.2)

        Regions["SR"][ "main" ][ plot ]["SumMC"].Draw()        
        Regions[CR][ "main" ][ plot ]["SumMC"].DrawNormalized("sames")
        Regions[CR][ "main" ][ plot ]["Data"].DrawNormalized("sames")

        l = TLegend(0.1,0.7,0.48,0.9)
        l.SetName("Legend_" + plot + "_" + CR )
        l.AddEntry( Regions["SR"][ "main" ][ plot ]["SumMC"] , "MC in SR" , "l" )
        l.AddEntry( Regions[CR][ "main" ][ plot ]["Data"]    , "Data in " + CR , "l" )
        l.AddEntry( Regions[CR][ "main" ][ plot ]["SumMC"]    , "MC in " + CR , "l" )
        l.Draw()
        plots[plot].append( l )
        plots[plot].append( c )

        c.Write()
for category in Categories:        
    fOut.mkdir(category).cd()
    for plot in plots :
        for CR in CRNames:
            c = TCanvas()
            c.SetName( "Canvas_" + category + "_" + plot + "_" + CR )
            c.SetTitle(plot + " " + CR)
            c.Divide(2)
            c.cd(1)

            for signal in ["THQ", "TTH"]:

                if plot == "One" :
                    srmc = Categories[ category ][ ("SR" , signal) ][ "mc" ]
                    crmc =  Categories[ category ][ (CR , signal) ][ "mc" ]
                    crdata =  Categories[ category ][ (CR , signal) ][ "data" ]
                else :
                    srmc = Regions["SR"][ (category , signal ) ][ plot ]["SumMC"]
                    crmc = Regions[CR][ (category , signal ) ][ plot ]["SumMC"]
                    crdata = Regions[CR][ (category , signal ) ][ plot ]["Data"]

                srmc.SetLineStyle(0)
                srmc.SetLineColor(kRed)
                crmc.SetLineStyle(0)
                crmc.SetLineColor(kBlue)

                
                if plot == "One" :
                    crmc.SetMaximum(1)
                    crmc.SetMinimum(-0.2)

                    crmc.Draw()
                    srmc.Draw("sames")
                    crdata.Draw("sames")
                else:
                    crmc.Scale( 1./ crmc.Integral() )
                    crmc.SetMaximum(1)
                    crmc.SetMinimum(-0.2)

                    crmc.Draw()
                    
                    srmc.DrawNormalized("sames")
                    crdata.DrawNormalized("sames")

                l = TLegend(0.1,0.7,0.48,0.9)
                l.SetName("Legend_" + category+"_"+signal +"_"+ plot + "_" + CR )
                l.AddEntry( srmc , "MC in SR" , "l" )
                l.AddEntry( crdata  , "Data in " + CR , "l" )
                l.AddEntry( crmc    , "MC in " + CR , "l" )
                l.Draw()
                plots[plot].append( l )
                plots[plot].append( c )

                c.cd(2)
            c.Write()

fOut.Close()

    
