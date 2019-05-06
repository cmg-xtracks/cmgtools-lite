#!/bin/env python
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer import *  
from PhysicsTools.Heppy.analyzers.core.autovars import *  
from PhysicsTools.Heppy.analyzers.objects.autophobj import  *
from math import *

##------------------------------------------  
## LEPTON
##------------------------------------------  

leptonTypeXtracks = NTupleObjectType("leptonXtracks", baseObjectTypes = [ leptonType ], variables = [
    NTupleVariable("etaSc", lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),
    NTupleVariable("mcMatchPdgId",  lambda x : x.mcLep.pdgId() if getattr(x,'mcLep',None)!=None else -99, int, mcOnly=True, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z): pdgId of the matched gen-level lepton, zero if non-prompt or fake"),
    NTupleVariable("mcPromptGamma", lambda x : x.mcPho.isPromptFinalState() if getattr(x,"mcPho",None) else 0, int, mcOnly=True, help="Photon isPromptFinalState"),
    NTupleVariable("triggerMatched", lambda x : 1 if x.matchedTrgObjSingleLep else 0, int, mcOnly=False, help="Is the lepton matched to a single lepton trigger"),
])
leptonTypeXtracks.removeVariable("relIsoAn04")
leptonTypeXtracks.removeVariable("eleCutIdSpring15_25ns_v1")
leptonTypeXtracks.removeVariable("ICHEPsoftMuonId")
leptonTypeXtracks.removeVariable("ICHEPmediumMuonId")

##------------------------------------------  
## TAU
##------------------------------------------  

tauTypeXtracks = NTupleObjectType("tauXtracks",  baseObjectTypes = [ tauType ], variables = [
     NTupleVariable("idMVAdR03", lambda x : x.idMVAdR03, int, help="1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the IsolationMVArun2v1DBdR03oldDMwLT discriminator"),
])
tauTypeXtracks.removeVariable("idMVANewDM")
tauTypeXtracks.removeVariable("idCI3hit")


jetTypeXtracks = NTupleObjectType("jetXtracks",  baseObjectTypes = [ jetTypeExtra ], variables = [
    NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
])
jetTypeXtracks.removeVariable("btagCMVA")
jetTypeXtracks.removeVariable("nLeptons")

jetTypeXtracksFwd = NTupleObjectType("jetFwd",  baseObjectTypes = [ jetType ], variables = [
    NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
])
jetTypeXtracks.removeVariable("btagCMVA")
jetTypeXtracksFwd.removeVariable("nLeptons")

##------------------------------------------  
## MET
##------------------------------------------  
  
metTypeXtracks = NTupleObjectType("metXtracks", baseObjectTypes = [ metType ], variables = [
])

metTypeXtracksBasic = NTupleObjectType("metXtracksBasic", baseObjectTypes = [ fourVectorType ], variables = [
])

##------------------------------------------  
## IsoTrackDeDx
##------------------------------------------

def _isoDBeta(x):
    return x.chargedHadronIso() + max(x.neutralHadronIso()+x.photonIso()-0.5*x.puChargedHadronIso(), 0)

hitPatternType = NTupleObjectType("hitPatternType", baseObjectTypes = [], variables = [
    NTupleVariable("trackerLayers", lambda x : x.hitPattern().trackerLayersWithMeasurement(), int, help="Tracker Layers"),
    NTupleVariable("pixelLayers", lambda x : x.hitPattern().pixelLayersWithMeasurement(), int, help="Pixel Layers"),
    NTupleVariable("trackerHits", lambda x : x.hitPattern().numberOfValidTrackerHits(), int, help="Tracker hits"),
    NTupleVariable("pixelHits", lambda x : x.hitPattern().numberOfValidPixelHits(), int, help="Pixel hits"),
    NTupleVariable("missingInnerPixelHits", lambda x : x.hitPattern().numberOfLostPixelHits(1), int, help="Missing inner pixel hits"),
    NTupleVariable("missingOuterPixelHits", lambda x : x.hitPattern().numberOfLostPixelHits(2), int, help="Missing outer pixel hits"),
    NTupleVariable("missingInnerStripHits", lambda x : x.hitPattern().numberOfLostStripHits(1), int, help="Missing inner strips hits"),
    NTupleVariable("missingOuterStripHits", lambda x : x.hitPattern().numberOfLostStripHits(2), int, help="Missing outer strips hits"),
    NTupleVariable("missingInnerTrackerHits", lambda x : x.hitPattern().numberOfLostTrackerHits(1), int, help="Missing inner tracker hits"),
    NTupleVariable("missingOuterTrackerHits", lambda x : x.hitPattern().numberOfLostTrackerHits(2), int, help="Missing outer tracker hits"),
    NTupleVariable("missingMiddleTrackerHits", lambda x : x.hitPattern().numberOfLostTrackerHits(0), int, help="Missing tracker hits in the middle of the track"),
])
hitDeDxType = NTupleObjectType("hitDeDxType", baseObjectTypes = [], variables = [
    NTupleVariable("dedxByHit0", lambda x : x.dedxByHit[0]),
    NTupleVariable("dedxByHit1", lambda x : x.dedxByHit[1]),
    NTupleVariable("dedxByHit2", lambda x : x.dedxByHit[2]),
    NTupleVariable("dedxByHit3", lambda x : x.dedxByHit[3]),
    NTupleVariable("dedxByHit4", lambda x : x.dedxByHit[4]),
    NTupleVariable("dedxByHit5", lambda x : x.dedxByHit[5]),
    NTupleVariable("dedxByHit6", lambda x : x.dedxByHit[6]),
    NTupleVariable("dedxByHit7", lambda x : x.dedxByHit[7]),
    NTupleVariable("dedxByHit8", lambda x : x.dedxByHit[8]),
    NTupleVariable("dedxByHit9", lambda x : x.dedxByHit[9]),
    NTupleVariable("dedxByHit10", lambda x : x.dedxByHit[10]),
    NTupleVariable("dedxByHit11", lambda x : x.dedxByHit[11]),
    NTupleVariable("dedxByHit12", lambda x : x.dedxByHit[12]),
    NTupleVariable("dedxByHit13", lambda x : x.dedxByHit[13]),

    NTupleVariable("dedxUnSmearedByHit0", lambda x : x.dedxUnSmearedByHit[0]),
    NTupleVariable("dedxUnSmearedByHit1", lambda x : x.dedxUnSmearedByHit[1]),
    NTupleVariable("dedxUnSmearedByHit2", lambda x : x.dedxUnSmearedByHit[2]),
    NTupleVariable("dedxUnSmearedByHit3", lambda x : x.dedxUnSmearedByHit[3]),
    NTupleVariable("dedxUnSmearedByHit4", lambda x : x.dedxUnSmearedByHit[4]),
    NTupleVariable("dedxUnSmearedByHit5", lambda x : x.dedxUnSmearedByHit[5]),
    NTupleVariable("dedxUnSmearedByHit6", lambda x : x.dedxUnSmearedByHit[6]),
    NTupleVariable("dedxUnSmearedByHit7", lambda x : x.dedxUnSmearedByHit[7]),
    NTupleVariable("dedxUnSmearedByHit8", lambda x : x.dedxUnSmearedByHit[8]),
    NTupleVariable("dedxUnSmearedByHit9", lambda x : x.dedxUnSmearedByHit[9]),
    NTupleVariable("dedxUnSmearedByHit10", lambda x : x.dedxUnSmearedByHit[10]),
    NTupleVariable("dedxUnSmearedByHit11", lambda x : x.dedxUnSmearedByHit[11]),
    NTupleVariable("dedxUnSmearedByHit12", lambda x : x.dedxUnSmearedByHit[12]),
    NTupleVariable("dedxUnSmearedByHit13", lambda x : x.dedxUnSmearedByHit[13]),
    
    #-------------------------------------------
    
    NTupleVariable("deByHit0", lambda x : x.deByHit[0]),
    NTupleVariable("deByHit1", lambda x : x.deByHit[1]),
    NTupleVariable("deByHit2", lambda x : x.deByHit[2]),
    NTupleVariable("deByHit3", lambda x : x.deByHit[3]),
    NTupleVariable("deByHit4", lambda x : x.deByHit[4]),
    NTupleVariable("deByHit5", lambda x : x.deByHit[5]),
    NTupleVariable("deByHit6", lambda x : x.deByHit[6]),
    NTupleVariable("deByHit7", lambda x : x.deByHit[7]),
    NTupleVariable("deByHit8", lambda x : x.deByHit[8]),
    NTupleVariable("deByHit9", lambda x : x.deByHit[9]),
    NTupleVariable("deByHit10", lambda x : x.deByHit[10]),
    NTupleVariable("deByHit11", lambda x : x.deByHit[11]),
    NTupleVariable("deByHit12", lambda x : x.deByHit[12]),
    NTupleVariable("deByHit13", lambda x : x.deByHit[13]),

    NTupleVariable("dxByHit0", lambda x : x.dxByHit[0]),
    NTupleVariable("dxByHit1", lambda x : x.dxByHit[1]),
    NTupleVariable("dxByHit2", lambda x : x.dxByHit[2]),
    NTupleVariable("dxByHit3", lambda x : x.dxByHit[3]),
    NTupleVariable("dxByHit4", lambda x : x.dxByHit[4]),
    NTupleVariable("dxByHit5", lambda x : x.dxByHit[5]),
    NTupleVariable("dxByHit6", lambda x : x.dxByHit[6]),
    NTupleVariable("dxByHit7", lambda x : x.dxByHit[7]),
    NTupleVariable("dxByHit8", lambda x : x.dxByHit[8]),
    NTupleVariable("dxByHit9", lambda x : x.dxByHit[9]),
    NTupleVariable("dxByHit10", lambda x : x.dxByHit[10]),
    NTupleVariable("dxByHit11", lambda x : x.dxByHit[11]),
    NTupleVariable("dxByHit12", lambda x : x.dxByHit[12]),
    NTupleVariable("dxByHit13", lambda x : x.dxByHit[13]),

    #-------------------------------------------

    NTupleVariable("subDetIdByHit0", lambda x : x.subDetIdByHit[0], int),
    NTupleVariable("subDetIdByHit1", lambda x : x.subDetIdByHit[1], int),
    NTupleVariable("subDetIdByHit2", lambda x : x.subDetIdByHit[2], int),
    NTupleVariable("subDetIdByHit3", lambda x : x.subDetIdByHit[3], int),
    NTupleVariable("subDetIdByHit4", lambda x : x.subDetIdByHit[4], int),
    NTupleVariable("subDetIdByHit5", lambda x : x.subDetIdByHit[5], int),
    NTupleVariable("subDetIdByHit6", lambda x : x.subDetIdByHit[6], int),
    NTupleVariable("subDetIdByHit7", lambda x : x.subDetIdByHit[7], int),
    NTupleVariable("subDetIdByHit8", lambda x : x.subDetIdByHit[8], int),
    NTupleVariable("subDetIdByHit9", lambda x : x.subDetIdByHit[9], int),
    NTupleVariable("subDetIdByHit10", lambda x : x.subDetIdByHit[10], int),
    NTupleVariable("subDetIdByHit11", lambda x : x.subDetIdByHit[11], int),
    NTupleVariable("subDetIdByHit12", lambda x : x.subDetIdByHit[12], int),
    NTupleVariable("subDetIdByHit13", lambda x : x.subDetIdByHit[13], int),

    NTupleVariable("sizeXbyHit0", lambda x : x.sizeXbyHit[0], int),
    NTupleVariable("sizeXbyHit1", lambda x : x.sizeXbyHit[1], int),
    NTupleVariable("sizeXbyHit2", lambda x : x.sizeXbyHit[2], int),
    NTupleVariable("sizeXbyHit3", lambda x : x.sizeXbyHit[3], int),
    NTupleVariable("sizeXbyHit4", lambda x : x.sizeXbyHit[4], int),
    NTupleVariable("sizeXbyHit5", lambda x : x.sizeXbyHit[5], int),
    NTupleVariable("sizeXbyHit6", lambda x : x.sizeXbyHit[6], int),
    NTupleVariable("sizeXbyHit7", lambda x : x.sizeXbyHit[7], int),
    NTupleVariable("sizeXbyHit8", lambda x : x.sizeXbyHit[8], int),
    NTupleVariable("sizeXbyHit9", lambda x : x.sizeXbyHit[9], int),
    NTupleVariable("sizeXbyHit10", lambda x : x.sizeXbyHit[10], int),
    NTupleVariable("sizeXbyHit11", lambda x : x.sizeXbyHit[11], int),
    NTupleVariable("sizeXbyHit12", lambda x : x.sizeXbyHit[12], int),
    NTupleVariable("sizeXbyHit13", lambda x : x.sizeXbyHit[13], int),
                                                                                                         
    NTupleVariable("sizeYbyHit0", lambda x : x.sizeYbyHit[0], int),
    NTupleVariable("sizeYbyHit1", lambda x : x.sizeYbyHit[1], int),
    NTupleVariable("sizeYbyHit2", lambda x : x.sizeYbyHit[2], int),
    NTupleVariable("sizeYbyHit3", lambda x : x.sizeYbyHit[3], int),
    NTupleVariable("sizeYbyHit4", lambda x : x.sizeYbyHit[4], int),
    NTupleVariable("sizeYbyHit5", lambda x : x.sizeYbyHit[5], int),
    NTupleVariable("sizeYbyHit6", lambda x : x.sizeYbyHit[6], int),
    NTupleVariable("sizeYbyHit7", lambda x : x.sizeYbyHit[7], int),
    NTupleVariable("sizeYbyHit8", lambda x : x.sizeYbyHit[8], int),
    NTupleVariable("sizeYbyHit9", lambda x : x.sizeYbyHit[9], int),
    NTupleVariable("sizeYbyHit10", lambda x : x.sizeYbyHit[10], int),
    NTupleVariable("sizeYbyHit11", lambda x : x.sizeYbyHit[11], int),
    NTupleVariable("sizeYbyHit12", lambda x : x.sizeYbyHit[12], int),
    NTupleVariable("sizeYbyHit13", lambda x : x.sizeYbyHit[13], int),
    
    NTupleVariable("layerOrSideByHit0", lambda x : x.layerOrSideByHit[0], int),
    NTupleVariable("layerOrSideByHit1", lambda x : x.layerOrSideByHit[1], int),
    NTupleVariable("layerOrSideByHit2", lambda x : x.layerOrSideByHit[2], int),
    NTupleVariable("layerOrSideByHit3", lambda x : x.layerOrSideByHit[3], int),
    NTupleVariable("layerOrSideByHit4", lambda x : x.layerOrSideByHit[4], int),
    NTupleVariable("layerOrSideByHit5", lambda x : x.layerOrSideByHit[5], int),
    NTupleVariable("layerOrSideByHit6", lambda x : x.layerOrSideByHit[6], int),
    NTupleVariable("layerOrSideByHit7", lambda x : x.layerOrSideByHit[7], int),
    NTupleVariable("layerOrSideByHit8", lambda x : x.layerOrSideByHit[8], int),
    NTupleVariable("layerOrSideByHit9", lambda x : x.layerOrSideByHit[9], int),
    NTupleVariable("layerOrSideByHit10", lambda x : x.layerOrSideByHit[10], int),
    NTupleVariable("layerOrSideByHit11", lambda x : x.layerOrSideByHit[11], int),
    NTupleVariable("layerOrSideByHit12", lambda x : x.layerOrSideByHit[12], int),
    NTupleVariable("layerOrSideByHit13", lambda x : x.layerOrSideByHit[13], int),

    NTupleVariable("ladderOrBladeByHit0", lambda x : x.ladderOrBladeByHit[0], int),
    NTupleVariable("ladderOrBladeByHit1", lambda x : x.ladderOrBladeByHit[1], int),
    NTupleVariable("ladderOrBladeByHit2", lambda x : x.ladderOrBladeByHit[2], int),
    NTupleVariable("ladderOrBladeByHit3", lambda x : x.ladderOrBladeByHit[3], int),
    NTupleVariable("ladderOrBladeByHit4", lambda x : x.ladderOrBladeByHit[4], int),
    NTupleVariable("ladderOrBladeByHit5", lambda x : x.ladderOrBladeByHit[5], int),
    NTupleVariable("ladderOrBladeByHit6", lambda x : x.ladderOrBladeByHit[6], int),
    NTupleVariable("ladderOrBladeByHit7", lambda x : x.ladderOrBladeByHit[7], int),
    NTupleVariable("ladderOrBladeByHit8", lambda x : x.ladderOrBladeByHit[8], int),
    NTupleVariable("ladderOrBladeByHit9", lambda x : x.ladderOrBladeByHit[9], int),
    NTupleVariable("ladderOrBladeByHit10", lambda x : x.ladderOrBladeByHit[10], int),
    NTupleVariable("ladderOrBladeByHit11", lambda x : x.ladderOrBladeByHit[11], int),
    NTupleVariable("ladderOrBladeByHit12", lambda x : x.ladderOrBladeByHit[12], int),
    NTupleVariable("ladderOrBladeByHit13", lambda x : x.ladderOrBladeByHit[13], int),

    NTupleVariable("sideByHit0", lambda x : x.sideByHit[0], int),
    NTupleVariable("sideByHit1", lambda x : x.sideByHit[1], int),
    NTupleVariable("sideByHit2", lambda x : x.sideByHit[2], int),
    NTupleVariable("sideByHit3", lambda x : x.sideByHit[3], int),
    NTupleVariable("sideByHit4", lambda x : x.sideByHit[4], int),
    NTupleVariable("sideByHit5", lambda x : x.sideByHit[5], int),
    NTupleVariable("sideByHit6", lambda x : x.sideByHit[6], int),
    NTupleVariable("sideByHit7", lambda x : x.sideByHit[7], int),
    NTupleVariable("sideByHit8", lambda x : x.sideByHit[8], int),
    NTupleVariable("sideByHit9", lambda x : x.sideByHit[9], int),
    NTupleVariable("sideByHit10", lambda x : x.sideByHit[10], int),
    NTupleVariable("sideByHit11", lambda x : x.sideByHit[11], int),
    NTupleVariable("sideByHit12", lambda x : x.sideByHit[12], int),
    NTupleVariable("sideByHit13", lambda x : x.sideByHit[13], int),



    #NTupleVariable("moduleByHit0", lambda x : x.moduleByHit[0], int),        # not used so far
    #NTupleVariable("moduleByHit1", lambda x : x.moduleByHit[1], int),        # not used so far
    #NTupleVariable("moduleByHit2", lambda x : x.moduleByHit[2], int),        # not used so far
    #NTupleVariable("moduleByHit3", lambda x : x.moduleByHit[3], int),        # not used so far
    #NTupleVariable("moduleByHit4", lambda x : x.moduleByHit[4], int),        # not used so far
    #NTupleVariable("moduleByHit5", lambda x : x.moduleByHit[5], int),        # not used so far
    #NTupleVariable("moduleByHit6", lambda x : x.moduleByHit[6], int),        # not used so far
    #NTupleVariable("moduleByHit7", lambda x : x.moduleByHit[7], int),        # not used so far
    #NTupleVariable("moduleByHit8", lambda x : x.moduleByHit[8], int),        # not used so far
    #NTupleVariable("moduleByHit9", lambda x : x.moduleByHit[9], int),        # not used so far
    #NTupleVariable("moduleByHit10", lambda x : x.moduleByHit[10], int),      # not used so far
    #NTupleVariable("moduleByHit11", lambda x : x.moduleByHit[11], int),      # not used so far
    #NTupleVariable("moduleByHit12", lambda x : x.moduleByHit[12], int),      # not used so far
    #NTupleVariable("moduleByHit13", lambda x : x.moduleByHit[13], int),      # not used so far

    NTupleVariable("pixByHit0", lambda x : x.pixByHit[0], int),
    NTupleVariable("pixByHit1", lambda x : x.pixByHit[1], int),
    NTupleVariable("pixByHit2", lambda x : x.pixByHit[2], int),
    NTupleVariable("pixByHit3", lambda x : x.pixByHit[3], int),
    NTupleVariable("pixByHit4", lambda x : x.pixByHit[4], int),
    NTupleVariable("pixByHit5", lambda x : x.pixByHit[5], int),
    NTupleVariable("pixByHit6", lambda x : x.pixByHit[6], int),
    NTupleVariable("pixByHit7", lambda x : x.pixByHit[7], int),
    NTupleVariable("pixByHit8", lambda x : x.pixByHit[8], int),
    NTupleVariable("pixByHit9", lambda x : x.pixByHit[9], int),
    NTupleVariable("pixByHit10", lambda x : x.pixByHit[10], int),
    NTupleVariable("pixByHit11", lambda x : x.pixByHit[11], int),
    NTupleVariable("pixByHit12", lambda x : x.pixByHit[12], int),
    NTupleVariable("pixByHit13", lambda x : x.pixByHit[13], int),


])

isoTrackTypeDeDx = NTupleObjectType("isoTrackTypeDeDx", baseObjectTypes = [ particleType, hitPatternType, hitDeDxType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    NTupleVariable("dxy",   lambda x : x.dxy(), help="d_{xy} with respect to PV, in cm (with sign)"),
    NTupleVariable("dz",    lambda x : x.dz() , help="d_{z} with respect to PV, in cm (with sign)"),
    NTupleVariable("edxy",  lambda x : x.dxyError(), help="#sigma(d_{xy}) with respect to PV, in cm"),
    NTupleVariable("edz", lambda x : x.dzError(), help="#sigma(d_{z}) with respect to PV, in cm"),    


    NTupleVariable("highPurity", lambda x : x.isHighPurityTrack(), int, help="High purity"),

    NTupleVariable("miniIsoCH",   lambda x : x.miniPFIsolation().chargedHadronIso(), help="Charged hadron mini-isolation"),
    NTupleVariable("miniIsoNH",   lambda x : x.miniPFIsolation().neutralHadronIso(), help="Neutral hadron mini-isolation"),
    NTupleVariable("miniIsoPH",   lambda x : x.miniPFIsolation().photonIso(), help="Photon mini-isolation"),
    NTupleVariable("miniIsoPU",   lambda x : x.miniPFIsolation().puChargedHadronIso(), help="Pileup charged hadron mini-isolation"),
    NTupleVariable("miniRelIso",   lambda x : _isoDBeta(x.miniPFIsolation())/x.pt(), help="mini-isolation (relative, PU-corrected using dBeta)"),
    NTupleVariable("dR03IsoCH",   lambda x : x.pfIsolationDR03().chargedHadronIso(), help="Charged hadron isolation dR=0.3"),
    NTupleVariable("dR03IsoNH",   lambda x : x.pfIsolationDR03().neutralHadronIso(), help="Neutral hadron isolation dR=0.3"),
    NTupleVariable("dR03IsoPH",   lambda x : x.pfIsolationDR03().photonIso(), help="Photon isolation = dR=0.3"),
    NTupleVariable("dR03IsoPU",   lambda x : x.pfIsolationDR03().puChargedHadronIso(), help="Pileup charged hadron isolation dR=0.3"),
    NTupleVariable("relIso03",   lambda x : _isoDBeta(x.pfIsolationDR03())/x.pt(), help="relative isolation dR=0.3 (PU-corrected using dBeta)"),
    NTupleVariable("caloEmEnergy",   lambda x : x.matchedCaloJetEmEnergy(), help="Energy in the ECAL behind the track"),
    NTupleVariable("caloHadEnergy",   lambda x : x.matchedCaloJetHadEnergy(), help="Energy in the HCAL behind the track"),
    NTupleVariable("channelsGoodECAL", lambda x : x.channelsGoodECAL, int, help="Flag set to 1 when the track extrapolates to all good ECAL channels"),
    NTupleVariable("channelsGoodHCAL", lambda x : x.channelsGoodHCAL, int, help="Flag set to 1 when the track extrapolates to all good HCAL channels"),

    NTupleVariable("awayJet_idx", lambda x : x.leadAwayJet.index if x.leadAwayJet else -1, int),
    NTupleVariable("awayJet_pt", lambda x : x.leadAwayJet.pt() if x.leadAwayJet else 0),
    NTupleVariable("awayJet_dr", lambda x : deltaR(x, x.leadAwayJet) if x.leadAwayJet else 0),

    NTupleVariable("awayNJet", lambda x : x.awayJetInfo['num'], int),
    NTupleVariable("awayHTJet", lambda x : x.awayJetInfo['ht']),

    NTupleVariable("awayMu_idx", lambda x : x.leadAwayMu.index if x.leadAwayMu else -1, int),
    NTupleVariable("awayMu_dr", lambda x : deltaR(x, x.leadAwayMu) if x.leadAwayMu else 0),
    NTupleVariable("awayMu_mll", lambda x : (x.leadAwayMu.p4()+x.p4()).M() if x.leadAwayMu else 0),

    NTupleVariable("awayEle_idx", lambda x : x.leadAwayEle.index if x.leadAwayEle else -1, int),
    NTupleVariable("awayEle_dr", lambda x : deltaR(x, x.leadAwayEle) if x.leadAwayEle else 0),
    NTupleVariable("awayEle_mll", lambda x : (x.leadAwayEle.p4()+x.p4()).M() if x.leadAwayEle else 0),

    NTupleVariable("closestMu_idx", lambda x : x.closestMu.index if x.closestMu else -1, int),
    NTupleVariable("closestEle_idx", lambda x : x.closestEle.index if x.closestEle else -1, int),
    NTupleVariable("closestTau_idx", lambda x : x.closestTau.index if x.closestTau else -1, int),

    NTupleVariable("trigLepton_idx", lambda x : x.trigLepton.index if getattr(x, 'trigLepton', None) else -1, int),

    NTupleVariable("myDeDx", lambda x : x.myDeDx),
    NTupleVariable("mcMatch", lambda x : x.mcMatch.index if x.mcMatch else -1, int, mcOnly=True),
    NTupleVariable("mcMatchAnyId", lambda x : x.mcMatchAny.pdgId()*(1+99*x.mcMatchAny.isDirectPromptTauDecayProductFinalState()) if x.mcMatchAny else 0, int, mcOnly=True, help="MC pdgId of the matched gen lepton, tau, photon or chargino (for leptons from tau, it's pdgId*100)"),
    NTupleVariable("mcMatchAnyPt", lambda x : x.mcMatchAny.pt() if x.mcMatchAny else 0, int, mcOnly=True, help="MC pt of the matched gen lepton, tau, photon or chargino"),
]
)

calibTrackTypeDeDx = NTupleObjectType("calibTrackTypeDeDx", baseObjectTypes = [ hitPatternType, hitDeDxType ], variables = [
    NTupleVariable("pt",   lambda x : x.pt()),
    NTupleVariable("eta",   lambda x : x.eta()),
    NTupleVariable("phi",   lambda x : x.phi()),
    NTupleVariable("p",   lambda x : x.p()),
    NTupleVariable("charge",   lambda x : x.charge(), int),
    NTupleVariable("dxy",   lambda x : x.dxy, help="d_{xy} with respect to PV, in cm (with sign)"),
    NTupleVariable("dz",    lambda x : x.dz , help="d_{z} with respect to PV, in cm (with sign)"),
    NTupleVariable("edxy",  lambda x : x.dxyError(), help="#sigma(d_{xy}) with respect to PV, in cm"),
    NTupleVariable("edz", lambda x : x.dzError(), help="#sigma(d_{z}) with respect to PV, in cm"),    
    NTupleVariable("highPurity", lambda x : x.quality(x.highPurity), int, help="High purity"),
    NTupleVariable("dedxPrescale", lambda x : x.dedxPrescale, int, help="Prescale factor applied when selecting this track to save dE/dx"),
    NTupleVariable("stripDeDx", lambda x : x.stripDeDx.dEdx(), help="dE/dx in the strip detector (harmonic2 estimator)"),
    NTupleVariable("stripDeDxErr", lambda x : x.stripDeDx.dEdxError(), help="dE/dx uncertainty in the strip detector (harmonic2 estimator)"),
    NTupleVariable("stripDeDxN", lambda x : x.stripDeDx.numberOfMeasurements(), help="number of dE/dx measurements in the strip detector"),
])


##------------------------------------------  
## genCharginoType
##------------------------------------------  
genCharginoType  = NTupleObjectType("genCharginoType", baseObjectTypes = [ genParticleWithMotherId ], variables = [
    NTupleVariable("beta", lambda x : x.p()/x.energy()),
    NTupleVariable("decayR", lambda x : x.decayPoint.R()),
    NTupleVariable("decayZ", lambda x : x.decayPoint.Z()),
])

## Tree Producer
treeProducer = cfg.Analyzer(
    AutoFillTreeProducer, name='treeProducerXtracks',
    vectorTree = True, saveTLorentzVectors = False,  defaultFloatType = 'F', PDFWeights = [],
    globalVariables = [
        NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
        NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),
        NTupleVariable("vertex_x",  lambda ev: ev.vx, float, help="Primary vertex x"),
        NTupleVariable("vertex_y",  lambda ev: ev.vy, float, help="Primary vertex y"),
        NTupleVariable("vertex_z",  lambda ev: ev.vz, float, help="Primary vertex z"),
        
        NTupleVariable("nJet30", lambda ev: sum([j.pt() > 30 for j in ev.cleanJets]), int, help="Number of jets with pt > 30, |eta|<2.4"),
        NTupleVariable("nJet30a", lambda ev: sum([j.pt() > 30 for j in ev.cleanJetsAll]), int, help="Number of jets with pt > 30, |eta|<4.7"),

        ## ------- lheHT, needed for merging HT binned samples
        NTupleVariable("lheHT", lambda ev : getattr(ev,"lheHT",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer"),
        NTupleVariable("lheHTIncoming", lambda ev : getattr(ev,"lheHTIncoming",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer (only LHE status<0 as mothers)"),
        NTupleVariable("lheVpt", lambda ev : getattr(ev,"lheV_pt",-999), mcOnly=True, help="p_{T} of the V boson at LHE level"),
        ],
    globalObjects = {
        "met"             : NTupleObject("met", metTypeXtracks, help="PF E_{T}^{miss}"),
        "metNoMu"         : NTupleObject("metNoMu", metTypeXtracksBasic, help="PF E_{T}^{miss} without muons"),
        "met_jecUp"       : NTupleObject("met_jecUp", metTypeXtracks, help="PF E_{T}^{miss}, after type 1 corrections (JEC plus 1sigma)"),
        "metNoMu_jecUp"   : NTupleObject("metNoMu_jecUp", metTypeXtracksBasic, help="PF E_{T}^{miss} without muons, after type 1 corrections (JEC plus 1sigma)"),
        "met_jecDown"     : NTupleObject("met_jecDown", metTypeXtracks, help="PF E_{T}^{miss}, after type 1 corrections (JEC minus 1sigma)"),
        "metNoMu_jecDown" : NTupleObject("metNoMu_jecUp", metTypeXtracksBasic, help="PF E_{T}^{miss} without muons, after type 1 corrections (JEC minus 1sigma)"),
        },
    collections = {
        ##--------------------------------------------------
        "selectedTaus"    : NTupleCollection("TauGood",  tauTypeXtracks, 8, help="Taus after the preselection"),
        "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeXtracks, 8, help="Leptons after the preselection"),
        ##------------------------------------------------
        "cleanJets"       : NTupleCollection("Jet",     jetTypeXtracks, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
        "cleanJetsFwd"    : NTupleCollection("JetFwd",  jetTypeXtracksFwd,  6, help="Forward jets after full selection and cleaning, sorted by pt"),
        ##------------------------------------------------
        "isoTracks"       : NTupleCollection("IsoTrack",  isoTrackTypeDeDx, 4, help="Isolated tracks"),
        ##------------------------------------------------
        "genCharginos"    : NTupleCollection("GenChargino",  genCharginoType, 4, mcOnly=True, help="Gen chargino"),
        },
    )

## Tree Producer
calibTreeProducer = cfg.Analyzer(
    AutoFillTreeProducer, name='treeProducerXtracks',
    vectorTree = True, saveTLorentzVectors = False,  defaultFloatType = 'F', PDFWeights = [],
    globalVariables = [
        NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
        NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),
        ],
    collections = {
       "tracks" : NTupleCollection("Track",  calibTrackTypeDeDx, 4, help="Isolated tracks"),
       }
   )
