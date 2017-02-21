from ROOT import TFile, TH1 , TMVA

class BDTOptions:
    def __init__(self , line):
        vals = line.split(',')
        self.name = vals[0]
        self.ntrees = int(vals[1])
        self.minnodesize = float(vals[2])
        self.maxdepth = int( vals[3] )
        self.adaboostbeta = float( vals[4] )
        self.ncuts = int( vals[5] )
        self.ROCIntegral = float( vals[6] )
        self.Signal_TrainTest_Kolmo = float( vals[7] )
        self.Signal_TrainTest_Chi2 = float( vals[8] )
        self.Bkg_TrainTest_Kolmo = float( vals[9] )
        self.Bkg_TrainTest_Chi2 = float( vals[10] )

        self.List = vals
  
  

    def ReadOverTrainingParam(self , dsname , signal , what ,  dir = None ): #what (0:kolmo_x, 1:kolmo_noX, 2:chi2_p , 3:chi2_/ndf , 4:chi2)
        
        if not hasattr( self , "TestS"):
            methodTitle = self.name
            hname = dsname + "/Method_" + methodTitle + "/" + methodTitle + "/MVA_" + methodTitle
            appendix = "_S" 
            self.TestS  =  dir.Get( hname + appendix )
            self.TrainS =  dir.Get( hname + "_Train" + appendix )
            appendix = "_B"
            self.TestB  =  dir.Get( hname + appendix )
            self.TrainB =  dir.Get( hname + "_Train" + appendix )
            
            TMVA.TMVAGlob.NormalizeHists( self.TestS , self.TrainS )
            TMVA.TMVAGlob.NormalizeHists( self.TestB , self.TrainB )
            
            for i in range(0, self.TestS.GetNbinsX() + 2 ) :
                if self.TestS.GetBinContent(i) < 0 :
                    self.TestS.SetBinContent( i , 0 )
                if self.TrainS.GetBinContent(i) < 0 :
                    self.TrainS.SetBinContent( i , 0 )
                if self.TestB.GetBinContent(i) < 0 :
                    self.TestB.SetBinContent( i , 0 )
                if self.TrainB.GetBinContent(i) < 0 :
                    self.TrainB.SetBinContent( i , 0 )

        test  = self.TestS  if signal else self.TestB
        train = self.TrainS if signal else self.TrainB
  
        ret = 0.
        if what == 0 :
            ret = test.KolmogorovTest( train, "X" )
        elif what == 1 :
            ret = test.KolmogorovTest( train )
        elif what == 2:
            ret = test.Chi2Test( train , "WW" );
        elif what == 3:
            ret = test.Chi2Test( train , "WW CHI2/NDF" );
        elif what == 4:
            ret = test.Chi2Test( train , "WW CHI2" );

        return ret

    def ReproduceAllMeasures(self , dir , dsname):
        self.NewS_Kolmo_X = self.ReadOverTrainingParam( dsname , True , 0 , dir )
        self.NewS_Kolmo = self.ReadOverTrainingParam( dsname , True , 1  )
        self.NewS_Chi2_p = self.ReadOverTrainingParam( dsname , True , 2  )
        self.NewS_Chi2_ndf = self.ReadOverTrainingParam( dsname , True , 3  )
        self.NewS_Chi2_chi2 = self.ReadOverTrainingParam( dsname , True , 4  )

        self.NewB_Kolmo_X = self.ReadOverTrainingParam( dsname , False , 0 , dir )
        self.NewB_Kolmo = self.ReadOverTrainingParam( dsname , False , 1  )
        self.NewB_Chi2_p = self.ReadOverTrainingParam( dsname , False , 2  )
        self.NewB_Chi2_ndf = self.ReadOverTrainingParam( dsname , False , 3  )
        self.NewB_Chi2_chi2 = self.ReadOverTrainingParam( dsname , False , 4  )

        list = [ self.NewS_Kolmo_X , self.NewS_Kolmo , self.NewS_Chi2_p , self.NewS_Chi2_ndf , self.NewS_Chi2_chi2 ]
        list.extend( [ self.NewB_Kolmo_X , self.NewB_Kolmo , self.NewB_Chi2_p , self.NewB_Chi2_ndf , self.NewB_Chi2_chi2 ] )

        self.List.extend( [ "%.2f" % (100.*s) for s in list ] )
    def PrintAll(self):
        return ','.join( self.List )

dir = TFile.Open("TMVA_LowNT_NCOpt.root")
infile = open('BDT_TTH.csv', 'r')
lines = [s.strip() for s in infile.readlines() ]

outfile = open('BDT_TTH2.csv' , 'w')
outfile.write( lines[0] + "," + ",".join( [ "NewS_Kolmo_X" , "NewS_Kolmo" , "NewS_Chi2_p" , "NewS_Chi2_ndf" , "NewS_Chi2_chi2" , "NewB_Kolmo_X" , "NewB_Kolmo" , "NewB_Chi2_p" , "NewB_Chi2_ndf" , "NewB_Chi2_chi2"  ] ) + "\n" )

for l in lines[1:]:
    o = BDTOptions(l)
    o.ReproduceAllMeasures(dir , "ttH")
    outfile.write( o.PrintAll() + "\n" )
outfile.close()
infile.close()
