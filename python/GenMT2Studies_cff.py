import FWCore.ParameterSet.Config as cms
GenMT2 = cms.EDAnalyzer('GenMETProbabilityStudies',

                        
                        Name = cms.string( "GenMT2" ),
                        NBinsPhi = cms.int32( 20 ) ,
                        PtMin = cms.double( 0 ),
                        PtMax = cms.double( 1000 ),
                        NBinsPt = cms.int32( 100 ),
                        VisMass = cms.double( 4 ),
                        InVisMass = cms.double( 80 ),
                        Precision = cms.double( 0.1 ),
                        prunedGen = cms.InputTag("prunedGenParticles"),
                        slimmedMET = cms.InputTag("slimmedMETs") ,
                        MakeTree = cms.bool( False ),
                        MT2_NBins = cms.int32(100) ,
                        MT2_Min = cms.double( 0 ) , 
                        MT2_Max = cms.double( 1000 ),
                        InputFile = cms.string("") )
