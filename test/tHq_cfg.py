import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

process = cms.Process("tHq")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff") # gives deprecated message in 80X but still runs
from Configuration.AlCa.GlobalTag import GlobalTag


process.TFileService = cms.Service("TFileService", fileName = cms.string("histo.root") )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
                            fileNames = cms.untracked.vstring(),
                            skipEvents=cms.untracked.uint32(10000)
)

process.load("tHqAnalyzer.HaNaMiniAnalyzer.tHq_cfi")

import FWCore.ParameterSet.VarParsing as opts
options = opts.VarParsing ('analysis')
options.register('sync',
                 0,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int ,
                 "")
options.register('sample',
                 'WJetsMG',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Sample to analyze')
options.register('job',
                 0,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int ,
                 "number of the job")
options.register('nFilesPerJob',
                 1,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int ,
                 "number of the files pre job")
options.register('output',
                 "out",
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string ,
                 "could be root://eoscms//eos/cms/store/user/hbakhshi/out")

options.parseArguments()


theSample = None
import os

if options.sync == 0 :
    from Samples76tHq.Samples import MicroAOD76Samples as samples


    for sample in samples:
        if sample.Name == options.sample :
            theSample = sample

    if theSample == None:
        raise NameError("Sample with name %s wasn't found" % (options.sample))

    if not theSample.Name == options.sample:
        raise NameError("The correct sample is not found %s !+ %s" % (sample.Name , options.sample) )
else:
    from tHqAnalyzer.HaNaMiniAnalyzer.Sample import *
    theSample = Sample( "Sync" , "Sync" , 100 , False , 0 , "" )
    theSample.Files = ['/store/group/phys_higgs/cmshgg/ferriff/flashgg/RunIIFall15DR76-1_3_0-25ns_ext1/1_3_1/VBFHToGG_M125_13TeV_amcatnlo_pythia8/RunIIFall15DR76-1_3_0-25ns_ext1-1_3_1-v0-RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/160127_024400/0000/myMicroAODOutputFile_1.root']
    options.nFilesPerJob = 1
    options.output = "out" 
    options.job = 0

process.tHq.sample = theSample.Name
process.tHq.LHE.useLHEW = theSample.LHEWeight
process.tHq.isData = theSample.IsData

if not ( options.job < theSample.MakeJobs( options.nFilesPerJob , options.output ) ):
    raise NameError("Job %d is not in the list of the jobs of sample %s with %d files per run" % (options.job , options.sample , options.nFilesPerJob ) )
job = theSample.Jobs[ options.job ]

process.source.fileNames.extend( job.Inputs )
process.TFileService.fileName = job.Output

process.maxEvents.input = options.maxEvents



process.load("flashgg.Taggers.flashggDiPhotonMVA_cfi")
process.load("flashgg.Taggers.flashggPreselectedDiPhotons_cfi")
process.load("flashgg.Taggers.flashggTags_cff")
process.load("flashgg.Taggers.flashggUpdatedIdMVADiPhotons_cfi")
process.flashggSeq = cms.Sequence( process.flashggUpdatedIdMVADiPhotons
                                   * process.flashggPreselectedDiPhotons
                                   * process.flashggDiPhotonMVA
                                   * process.flashggUnpackedJets )


#

if theSample.IsData :
    if os.environ["CMSSW_VERSION"].count("CMSSW_7_6"):
        process.GlobalTag = GlobalTag(process.GlobalTag, '76X_dataRun2_v15')
    elif os.environ["CMSSW_VERSION"].count("CMSSW_8_0"):
        process.GlobalTag = GlobalTag(process.GlobalTag,'80X_mcRun2_asymptotic_v11')
    else:
        raise Exception,"The default setup for microAODstd.py does not support releases other than 76X and 80X"

    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = (process.tHq.SetupDir.value() + '/JSON.txt')).getVLuminosityBlockRange()
    process.p = cms.Path( process.flashggSeq * process.tHq )
    for v in range(0 , 10 ):
        process.tHq.HLT.HLT_To_Or.append( 'HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v%d' % (v) )
        process.tHq.HLT.HLT_To_Or.append( 'HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v%d' % (v) )
        process.tHq.HLT.HLT_To_Or.append( 'HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v%d' % (v) )

else :
    if os.environ["CMSSW_VERSION"].count("CMSSW_7_6"):
        process.GlobalTag = GlobalTag(process.GlobalTag, '76X_mcRun2_asymptotic_v13')
    elif os.environ["CMSSW_VERSION"].count("CMSSW_8_0"):
        process.GlobalTag = GlobalTag(process.GlobalTag,'80X_mcRun2_asymptotic_v11')
    else:
        raise Exception,"The default setup for microAODstd.py does not support releases other than 76X and 80X"

    #process.GlobalTag.globaltag = '76X_dataRun2_16Dec2015_v0'
    #from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import *
    # process.patJetCorrFactorsReapplyJEC = updatedPatJetCorrFactors.clone(
    #     src = cms.InputTag("slimmedJets"),
    #     levels = ['L1FastJet', 
    #               'L2Relative', 
    #               'L3Absolute'],
    #     payload = 'AK4PFchs' ) # Make sure to choose the appropriate levels and payload here!

    # process.patJetsReapplyJEC = updatedPatJets.clone(
    #     jetSource = cms.InputTag("slimmedJets"),
    #     jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
    #     )
    #process.p = cms.Path( process.patJetCorrFactorsReapplyJEC + process.patJetsReapplyJEC + process.TTH + process.Hamb)
    process.p = cms.Path(process.flashggSeq *  process.tHq )
    if options.sync == 0 :
        for v in range(0 , 10 ):
            process.tHq.HLT.HLT_To_Or.append( 'HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v%d' % (v) )
            process.tHq.HLT.HLT_To_Or.append( 'HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v%d' % (v) )
            process.tHq.HLT.HLT_To_Or.append( 'HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v%d' % (v) )


process.outp1=cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string(job.Output2),
                               SelectEvents = cms.untracked.PSet(  SelectEvents = cms.vstring('p')  )
                               )
process.ep = cms.EndPath( process.outp1 )

