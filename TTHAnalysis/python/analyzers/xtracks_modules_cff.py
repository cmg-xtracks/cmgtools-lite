##########################################################
##          SUSY COMMON MODULES ARE DEFINED HERE        ##
## skimming modules are configured to not cut anything  ##
##########################################################

import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.all import *
from PhysicsTools.Heppy.analyzers.objects.all import *
from PhysicsTools.Heppy.analyzers.gen.all import *
import os

PDFWeights = []
#PDFWeights = [ ("CT10",53), ("MSTW2008lo68cl",41), ("NNPDF21_100",101) ]

# Find the initial events before the skim
skimAnalyzer = cfg.Analyzer(
    SkimAnalyzerCount, name='skimAnalyzerCount',
    useLumiBlocks = False,
    )

# Pick individual events (normally not in the path)
eventSelector = cfg.Analyzer(
    EventSelector,name="EventSelector",
    toSelect = []  # here put the event numbers (actual event numbers from CMSSW)
    )

# Apply json file (if the dataset has one)
jsonAna = cfg.Analyzer(
    JSONAnalyzer, name="JSONAnalyzer",
    )

# Filter using the 'triggers' and 'vetoTriggers' specified in the dataset
triggerAna = cfg.Analyzer(
    TriggerBitFilter, name="TriggerBitFilter",
    )

# Create flags for trigger bits
triggerFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="TriggerFlags",
    processName = 'HLT',
    fallbackProcessName = 'HLT2',
    prescaleProcessName = 'PAT',
    prescaleFallbackProcessName = 'RECO',
    unrollbits = True,
    saveIsUnprescaled = False,
    checkL1prescale = False,
    triggerBits = {
        # "<name>" : [ 'HLT_<Something>_v*', 'HLT_<SomethingElse>_v*' ] 
    }
    )
# Create flags for MET filter bits
eventFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="EventFlags",
    processName = 'PAT',
    fallbackProcessName = 'RECO', 
    outprefix   = 'Flag',
    triggerBits = {
        "HBHENoiseFilter" : [ "Flag_HBHENoiseFilter" ],
        "HBHENoiseIsoFilter" : [ "Flag_HBHENoiseIsoFilter" ],
        "globalTightHalo2016Filter" : [ "Flag_globalTightHalo2016Filter" ],
        "EcalDeadCellTriggerPrimitiveFilter" : [ "Flag_EcalDeadCellTriggerPrimitiveFilter" ],
        "goodVertices" : [ "Flag_goodVertices" ],
        "eeBadScFilter" : [ "Flag_eeBadScFilter" ],
        "ecalBadCalibFilter" : [ "Flag_ecalBadCalibFilter" ],
        "BadPFMuonFilter" : [ "Flag_BadPFMuonFilter" ],
        "BadChargedCandidateFilter" : [ "Flag_BadChargedCandidateFilter" ],
        }
    )

from CMGTools.TTHAnalysis.analyzers.badChargedHadronAnalyzer import badChargedHadronAnalyzer
badChargedHadronAna = cfg.Analyzer(
    badChargedHadronAnalyzer, name = 'badChargedHadronAna',
    muons='slimmedMuons',
    packedCandidates = 'packedPFCandidates',
)

from CMGTools.TTHAnalysis.analyzers.badMuonAnalyzer import badMuonAnalyzer
badMuonAna = cfg.Analyzer(
    badMuonAnalyzer, name = 'badMuonAna',
    muons='slimmedMuons',
    packedCandidates = 'packedPFCandidates',
)

from CMGTools.TTHAnalysis.analyzers.badMuonAnalyzerMoriond2017 import badMuonAnalyzerMoriond2017
badCloneMuonAnaMoriond2017 = cfg.Analyzer(
    badMuonAnalyzerMoriond2017, name = 'badCloneMuonMoriond2017',
    muons = 'slimmedMuons',
    vertices         = 'offlineSlimmedPrimaryVertices',
    minMuPt = 20,
    selectClones = True,
    postFix = '',
)

badMuonAnaMoriond2017 = cfg.Analyzer(
    badMuonAnalyzerMoriond2017, name = 'badMuonMoriond2017',
    muons = 'slimmedMuons',
    vertices         = 'offlineSlimmedPrimaryVertices',
    minMuPt = 20,
    selectClones = False,
    postFix = '',
)


# Select a list of good primary vertices (generic)
vertexAna = cfg.Analyzer(
    VertexAnalyzer, name="VertexAnalyzer",
    vertexWeight = None,
    fixedWeight = 1,
    verbose = False
    )


# This analyzer actually does the pile-up reweighting (generic)
pileUpAna = cfg.Analyzer(
    PileUpAnalyzer, name="PileUpAnalyzer",
    true = True,  # use number of true interactions for reweighting
    makeHists=True
    )


## Gen Info Analyzer (generic, but should be revised)
genAna = cfg.Analyzer(
    GeneratorAnalyzer, name="GeneratorAnalyzer",
    # BSM particles that can appear with status <= 2 and should be kept
    stableBSMParticleIds = [ 1000022 ],
    # Particles of which we want to save the pre-FSR momentum (a la status 3).
    # Note that for quarks and gluons the post-FSR doesn't make sense,
    # so those should always be in the list
    savePreFSRParticleIds = [ 1,2,3,4,5, 11,12,13,14,15,16, 21,22 ],
    # Make also the list of all genParticles, for other analyzers to handle
    makeAllGenParticles = True,
    # Make also the splitted lists
    makeSplittedGenLists = True,
    allGenTaus = False,
    # Print out debug information
    verbose = False,
    )

genHFAna = cfg.Analyzer(
    GenHeavyFlavourAnalyzer, name="GenHeavyFlavourAnalyzer",
    status2Only = False,
    bquarkPtCut = 15.0,
)

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)

from PhysicsTools.Heppy.analyzers.gen.LHEAnalyzer import LHEAnalyzer 
lheAna = LHEAnalyzer.defaultConfig

# Lepton Analyzer (generic)
#
# -> this is the producer of event.selectedLeptons 
#
lepAna = cfg.Analyzer(
    LeptonAnalyzer, name="leptonAnalyzer",
    # input collections
    muons='slimmedMuons',
    electrons='slimmedElectrons',
    rhoMuon= 'fixedGridRhoFastjetAll',
    rhoElectron = 'fixedGridRhoFastjetAll',
    # energy scale corrections and ghost muon suppression (off by default)
    doMuonScaleCorrections=False,
    doElectronScaleCorrections=False, # "embedded" in 5.18 for regression
    doSegmentBasedMuonCleaning=False,
    # inclusive very loose muon selection
    inclusive_muon_id  = "POG_ID_Loose",
    inclusive_muon_pt  = 3,
    inclusive_muon_eta = 2.4,
    inclusive_muon_dxy = 0.5,
    inclusive_muon_dz  = 1.0,
    muon_dxydz_track = "innerTrack",
    # loose muon selection
    loose_muon_id     = "POG_ID_Loose",
    loose_muon_pt     = 10,
    loose_muon_eta    = 2.4,
    loose_muon_dxy    = 0.05,
    loose_muon_dz     = 0.1,
    loose_muon_relIso = 1e9,
    loose_muon_isoCut     = lambda muon : muon.relIso03 < 0.25,
    # inclusive very loose electron selection
    inclusive_electron_id  = "",
    inclusive_electron_pt  = 5,
    inclusive_electron_eta = 2.5,
    inclusive_electron_dxy = 0.5,
    inclusive_electron_dz  = 1.0,
    inclusive_electron_lostHits = 1.0,
    # loose electron selection
    loose_electron_id     = "POG_Cuts_ID_FALL17_94X_v1_ConvVetoDxyDz_Veto",
    loose_electron_pt     = 10,
    loose_electron_eta    = 2.5,
    loose_electron_dxy    = 0.5,
    loose_electron_dz     = 1.0,
    loose_electron_relIso = 1e9,
    loose_electron_isoCut = lambda elec : elec.relIso03 < 0.25,
    loose_electron_lostHits = 10.0,
    # muon isolation correction method (can be "rhoArea" or "deltaBeta")
    mu_isoCorr = "deltaBeta" ,
    mu_effectiveAreas = "Fall17", #(can be 'Data2012' or 'Phys14_25ns_v1' or 'Spring15_25ns_v1')
    # electron isolation correction method (can be "rhoArea" or "deltaBeta")
    ele_isoCorr = "rhoArea" ,
    ele_effectiveAreas = "Fall17" , #(can be 'Data2012' or 'Phys14_25ns_v1' or 'Spring15_25ns_v1')
    ele_tightId = "Cuts_FALL17_94X_v1_ConvVetoDxyDz" ,
    # Mini-isolation, with pT dependent cone: will fill in the miniRelIso, miniRelIsoCharged, miniRelIsoNeutral variables of the leptons (see https://indico.cern.ch/event/368826/ )
    doMiniIsolation = False, # off by default since it requires access to all PFCandidates 
    packedCandidates = 'packedPFCandidates',
    miniIsolationPUCorr = 'rhoArea', # Allowed options: 'rhoArea' (EAs for 03 cone scaled by R^2), 'deltaBeta', 'raw' (uncorrected), 'weights' (delta beta weights; not validated)
    miniIsolationVetoLeptons = None, # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
    doDirectionalIsolation = [], # calculate directional isolation with leptons (works only with doMiniIsolation, pass list of cone sizes)
    doFixedConeIsoWithMiniIsoVeto = False, # calculate fixed cone isolations with the same vetoes used for miniIso,
    # minimum deltaR between a loose electron and a loose muon (on overlaps, discard the electron)
    min_dr_electron_muon = 0.05,
    # do MC matching 
    do_mc_match = True, # note: it will in any case try it only on MC, not on data
    do_mc_match_photons = "all",
    match_inclusiveLeptons = False, # match to all inclusive leptons
    )

## Tau Analyzer (generic)
tauAna = cfg.Analyzer(
    TauAnalyzer, name="tauAnalyzer",
    # inclusive very loose hadronic tau selection
    inclusive_ptMin = 20,
    inclusive_etaMax = 2.3,
    inclusive_dxyMax = 1000.,
    inclusive_dzMax = 0.4,
    inclusive_vetoLeptons = False,
    inclusive_leptonVetoDR = 0.4,
    inclusive_decayModeID = "decayModeFindingNewDMs", # ignored if not set or ""
    inclusive_tauID = "decayModeFindingNewDMs",
    inclusive_vetoLeptonsPOG = False, # If True, the following two IDs are required
    inclusive_tauAntiMuonID = "",
    inclusive_tauAntiElectronID = "",
    # loose hadronic tau selection
    loose_ptMin = 18,
    loose_etaMax = 9999,
    loose_dxyMax = 1000.,
    loose_dzMax = 0.2,
    loose_vetoLeptons = True,
    loose_leptonVetoDR = 0.4,
    loose_decayModeID = "decayModeFindingNewDMs", # ignored if not set or ""
    loose_tauID = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    loose_vetoLeptonsPOG = False, # If True, the following two IDs are required
    loose_tauAntiMuonID = "againstMuonLoose3",
    loose_tauAntiElectronID = "againstElectronLooseMVA5",

)

## Jets Analyzer (generic)
jetAna = cfg.Analyzer(
    JetAnalyzer, name='jetAnalyzer',
    jetCol = 'slimmedJets',
    copyJetsByValue = True,      #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    genJetCol = 'slimmedGenJets',
    rho = ('fixedGridRhoFastjetAll','',''),
    jetPt = 25.,
    jetEta = 4.7,
    jetEtaCentral = 2.4,
    cleanJetsFromLeptons = True,
    jetLepDR = 0.4,
    jetLepArbitration = (lambda jet,lepton : lepton), # you can decide which to keep in case of overlaps; e.g. if the jet is b-tagged you might want to keep the jet
    cleanSelectedLeptons = True, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    minLepPt = 10,
    lepSelCut = lambda lep : True,
    relaxJetId = False,  
    doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True, #'MC', # True, False, 'MC', 'Data'
    applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK4PFchs",
    mcGT     = "Fall17_17Nov2017_V6_MC",
    dataGT   = [(1,"Fall17_17Nov2017B_V6_DATA"),(299337,"Fall17_17Nov2017C_V6_DATA"),(302030,"Fall17_17Nov2017D_V6_DATA"),(303435,"Fall17_17Nov2017E_V6_DATA"),(304911,"Fall17_17Nov2017F_V6_DATA")],
    jecPath = "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec/",
    shiftJEC = 0, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    addJECShifts = True, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    jetPtOrUpOrDnSelection = True, # if true, apply pt cut on the maximum among central, JECUp and JECDown values of corrected pt
    smearJets = False,
    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts  
    alwaysCleanPhotons = False,
    cleanGenJetsFromPhoton = False,
    cleanJetsFromFirstPhoton = False,
    cleanJetsFromTaus = False,
    cleanJetsFromIsoTracks = False,
    doQG = False,
    do_mc_match = True,
    collectionPostFix = "",
    calculateSeparateCorrections = True, # should be True if recalibrateJets is True, otherwise L1s will be inconsistent
    calculateType1METCorrection  = True,
    type1METParams = { 'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True },
    storeLowPtJets = False,
    )

## Jets Analyzer (generic)
jetAnaScaleUp = jetAna.clone(name='jetAnalyzerScaleUp',
    copyJetsByValue = True,
    jetCol = 'slimmedJets',
    shiftJEC = +1, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    collectionPostFix = "_jecUp",
    calculateType1METCorrection  = True,
    cleanSelectedLeptons = False,
   )

## Jets Analyzer (generic)
jetAnaScaleDown = jetAna.clone(name='jetAnalyzerScaleDown',
    copyJetsByValue = True,
    jetCol = 'slimmedJets',
    shiftJEC = -1, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    collectionPostFix = "_jecDown",
    calculateType1METCorrection  = True,
    cleanSelectedLeptons = False,
    )

metAna = cfg.Analyzer(
    METAnalyzer, name="metAnalyzer",
    metCollection     = "slimmedMETs",
    noPUMetCollection = "slimmedMETs",    
    copyMETsByValue = True,
    doTkMet = False,
    doPuppiMet = False,
    doMetNoPU = False,
    doMetNoMu = True,
    doMetNoEle = False,
    doMetNoPhoton = False,
    storePuppiExtra = False, # False for MC, True for re-MiniAOD
    recalibrate = "type1", # or False or True
    applyJetSmearing = False, # does nothing unless the jet smearing is turned on in the jet analyzer
    old74XMiniAODs = False, # set to True to get the correct Raw MET when running on old 74X MiniAODs
    jetAnalyzerPostFix = "",
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    dzMax = 0.1,
    collectionPostFix = "",
    )

metAnaScaleUp = metAna.clone(name="metAnalyzerScaleUp",
    jetAnalyzerPostFix = "_jecUp",
    collectionPostFix = "_jecUp",
    )

metAnaScaleDown = metAna.clone(name="metAnalyzerScaleDown",
    jetAnalyzerPostFix = "_jecDown",
    collectionPostFix = "_jecDown",
    )

## early skimming on jets
from CMGTools.TTHAnalysis.analyzers.ttHFastJetSkimmer import ttHFastJetSkimmer
fastJetSkim = cfg.Analyzer(ttHFastJetSkimmer, name="fastJetSkimmer",
    jets = 'slimmedJets',
    jetCut = lambda j : j.pt() > 80 and abs(j.eta()) < 2.4, # looser pt because of non-final JECs
    minJets = 1,
    )

#
## early skimming on isolated tracks
# -> this creates the collection: event.preselIsoTracks
#
from CMGTools.TTHAnalysis.analyzers.isoTrackFastSkimmer import isoTrackFastSkimmer
isoTrackFastSkim = cfg.Analyzer(isoTrackFastSkimmer, name="isoTrackFastSkim",
    cut = lambda t : (t.pt() > 50 and
                      abs(t.eta()) < 2.4 and
                      t.isHighPurityTrack() and
                      abs(t.dxy()) < 0.5 and abs(t.dz()) < 0.5 and
                      (t.miniPFIsolation().chargedHadronIso() < 1.0*t.pt() or t.pt() > 100))
)

## Lepton trigger match (for CR)
from PhysicsTools.Heppy.analyzers.core.TriggerMatchAnalyzer import TriggerMatchAnalyzer
lepTrigMatch = cfg.Analyzer(TriggerMatchAnalyzer, name="lepTrigMatch", 
    processName = 'PAT',
    fallbackProcessName = 'RECO',
    unpackPathNames = True,
    collToMatch = 'selectedLeptons',
    collMatchSelectors = [ lambda l,t : t.id(83) == (abs(l.pdgId()) == 13) ],
    trgObjSelectors = [ lambda t : t.path("HLT_IsoMu27_v*",1,0) or 
                                   t.path("HLT_Ele32_WPTight_Gsf_v*",1,0) or 
                                   t.path("HLT_Ele35_WPTight_Gsf_v*",1,0) ],
    label="SingleLep",
    collMatchDRCut = 0.2,
    univoqueMatching = True,
)

## late skimming on jets and MET
from CMGTools.TTHAnalysis.analyzers.xtracksFilters import xtracksFilters
eventSkim = cfg.Analyzer( xtracksFilters, name='xtracksSkim',
    region     = "sr",
    jets       = "cleanJets",
    jetPtCuts  = [ 90., ],
    metCut     =  0,
    metNoMuCut =  80,
)

## Full DeDx analyzer
from CMGTools.TTHAnalysis.analyzers.isoTrackDeDxAnalyzer import isoTrackDeDxAnalyzer
isoTrackDeDxAna = cfg.Analyzer(isoTrackDeDxAnalyzer, name="isoTrackDeDxAna",
    doDeDx = True, 
        # for 94X MiniAOD v2, just set it to True
        # for 94X MiniAOD v1, you have two options
        #  - set it to False, and have no DeDx
        #  - set it to "94XMiniAODv1-Hack" and follow step (1) of https://hypernews.cern.ch/HyperNews/CMS/get/physTools/3586/1/1/1/1.html 
    trackerTopology = ( "$CMSSW_BASE/src/CMGTools/RootTools/data/trackerTopology_2017.root", "TrackerTopology_2017" )
    )


## Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerXtracks import *

xtracks_sequence = [
    lheWeightAna,
    pileUpAna,
    skimAnalyzer,
    jsonAna,
    triggerAna,

    fastJetSkim,
    isoTrackFastSkim,

    genAna,
    genHFAna,
    lheAna,

    vertexAna,
    lepAna,
    lepTrigMatch,
    tauAna,
    jetAna,
    jetAnaScaleUp,
    jetAnaScaleDown,
    metAna,
    metAnaScaleUp,
    metAnaScaleDown,

    isoTrackDeDxAna,

    eventSkim,

    triggerFlagsAna,
    eventFlagsAna,
    
    treeProducer,
]

vertexAnaAOD = vertexAna.clone(
    allVertices = "offlinePrimaryVertices",
    )
from CMGTools.TTHAnalysis.analyzers.aodDeDxAnalyzer import aodDeDxAnalyzer
aodDeDxAna = cfg.Analyzer(aodDeDxAnalyzer, name="aodDeDxAna",
    trackerTopology = ( "$CMSSW_BASE/src/CMGTools/RootTools/data/trackerTopology_2017.root", "TrackerTopology_2017" )
    )

xtracks_sequence_AOD = [
    skimAnalyzer,
    jsonAna,
    vertexAnaAOD,
    aodDeDxAna,
    calibTreeProducer
]
