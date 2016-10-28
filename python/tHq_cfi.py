import FWCore.ParameterSet.Config as cms
tHq = cms.EDFilter('tHqAnalyzer',
                     LHE = cms.PSet ( useLHEW = cms.bool( False ),
                                      Input = cms.InputTag("source")
                                      ),

                     HLT = cms.PSet( Input = cms.InputTag( "TriggerResults","","HLT" ), 
                                     HLT_To_Or = cms.vstring()
                                     ),
                     Vertex = cms.PSet( Input = cms.InputTag( "offlineSlimmedPrimaryVertices" ),
                                        pileupSrc = cms.InputTag("slimmedAddPileupInfo")
                                        ),
                     Muons = cms.PSet( Input = cms.InputTag("flashggSelectedMuons"),
                                       MuonPtCut = cms.double(20),
                                       MuonIsoCut = cms.double( 0.15 ),
                                       MuonEtaCut = cms.double( 2.4 ),
                                       MuonID = cms.int32( 3 ), #0:no id, 1:Loose , 2:Medium , 3:tight , 4 : soft
                                       DeltaRMuonPho = cms.double( 0.3 )
                                       ),
                     Electrons = cms.PSet( Input = cms.InputTag("flashggSelectedElectrons"),
                                       ElectronPtCut = cms.double(20),
                                       ElectronEtaCut = cms.double( 2.4 ),
                                       ElectronID = cms.int32( 3 ), #0:veto, 1:Loose , 2:Medium , 3:tight ,
                                       DeltaRElectronPho = cms.double( 0.3 ),
                                       DeltaRElectronTrk = cms.double( 0.4 ),
                                       DeltaMassElectronZ = cms.double( 10 )
                                       ),

                     MET = cms.PSet( Input = cms.InputTag("slimmedMETs"),
                                     Cut = cms.double( -1. )
                                     ),
                     Jets = cms.PSet( Input = cms.InputTag("flashggUnpackedJets","0"),
                                      flashgg = cms.bool( True ),
                                      MoreInputs = cms.VInputTag( cms.InputTag("flashggUnpackedJets","1"),
                                                                  cms.InputTag("flashggUnpackedJets","2"),
                                                                  cms.InputTag("flashggUnpackedJets","3"),
                                                                  cms.InputTag("flashggUnpackedJets","4"),
                                                                  cms.InputTag("flashggUnpackedJets","5"),
                                                                  cms.InputTag("flashggUnpackedJets","6"),
                                                                  cms.InputTag("flashggUnpackedJets","7"),
                                                                  ),
                                      ApplyJER = cms.bool( False ),
                                      JetPtCut = cms.double( 30 ),
                                      JetEtaCut = cms.double( 4.7 ),
                                      BTagAlgo = cms.string("pfCombinedInclusiveSecondaryVertexV2BJetTags"),
                                      BTagWPL = cms.double( 0.460 ),
                                      BTagWPM = cms.double( 0.800 ),
                                      BTagWPT = cms.double( 0.935 ),
                                      #Which WP to use in selection: 0,1,2 ---> L, M, T
                                      # -1 ---> no requirement
                                      BTagCuts = cms.vint32(1,-1), # supporting up to two working point, the second is for veto

                                      MinNJets = cms.uint32( 2 ),
                                      MinNBJets = cms.uint32( 1 )
                                      ),
                     
                     diPhoton = cms.PSet( Input = cms.InputTag("flashggPreselectedDiPhotons"),
                                          mvaResults = cms.PSet ( Input = cms.InputTag("flashggDiPhotonMVA") ),
                                          leadPhoOverMassThreshold = cms.double( 0.5 ),
                                          subleadPhoOverMassThreshold = cms.double( 0.25 ),
                                          MVAThreshold = cms.double( -0.4 ),
                                          PhoMVAThreshold = cms.double( -0.9 ),
                                          InvMassCut = cms.double( 100. )

                                          ),
                     sample = cms.string("WJetsMG"),
                     isData = cms.bool( False ),
                     SetupDir = cms.string("Setup80"),
                     StoreEventNumbers = cms.bool( True )
                     )
