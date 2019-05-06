##########################################################
##       CONFIGURATION FOR SUSY STOP SOFT B TREES       ##
##########################################################
#
# 2018 data and MC
#
#
#

import PhysicsTools.HeppyCore.framework.config as cfg
import re, sys

#-------- LOAD ALL ANALYZERS -----------
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from CMGTools.RootTools.samples.configTools import *
from CMGTools.RootTools.samples.autoAAAconfig import *

from CMGTools.TTHAnalysis.analyzers.xtracks_modules_cff import *

## Configuration that depends on the region
region = getHeppyOption("region","sr") # use 'sr', 'cr1l'

fastJetSkim.minJets = 1 if region =="sr" else 0
eventSkim.region = region

## Sample production and setup
### Trigger
#
# FIXME fix 2018 triggers
#
from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import *
triggerFlagsAna.triggerBits = {
    'SingleMu' : triggers_1mu_iso,
    'SingleEl' : triggers_1e_iso + triggers_1e_noniso,
    'MET'      : triggers_SOS_highMET
}

### MC
from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18MiniAOD import *

Wino_M_300_cTau_3  = kreator.makeMCComponentFromEOS("Wino_M_300_cTau_3",  "Wino_M_300_cTau_3",  "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_300_cTau_10 = kreator.makeMCComponentFromEOS("Wino_M_300_cTau_10", "Wino_M_300_cTau_10", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_300_cTau_30 = kreator.makeMCComponentFromEOS("Wino_M_300_cTau_30", "Wino_M_300_cTau_30", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_500_cTau_10 = kreator.makeMCComponentFromEOS("Wino_M_500_cTau_10", "Wino_M_500_cTau_10", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_650_cTau_10 = kreator.makeMCComponentFromEOS("Wino_M_650_cTau_10", "Wino_M_650_cTau_10", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_800_cTau_10 = kreator.makeMCComponentFromEOS("Wino_M_800_cTau_10", "Wino_M_800_cTau_10", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_1000_cTau_10 = kreator.makeMCComponentFromEOS("Wino_M_1000_cTau_10", "Wino_M_1000_cTau_10", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_500_cTau_20 = kreator.makeMCComponentFromEOS("Wino_M_500_cTau_20", "Wino_M_500_cTau_20", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_650_cTau_20 = kreator.makeMCComponentFromEOS("Wino_M_650_cTau_20", "Wino_M_650_cTau_20", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_800_cTau_20 = kreator.makeMCComponentFromEOS("Wino_M_800_cTau_20", "Wino_M_800_cTau_20", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)
Wino_M_1000_cTau_20 = kreator.makeMCComponentFromEOS("Wino_M_1000_cTau_20", "Wino_M_1000_cTau_20", "/store/cmst3/user/gpetrucc/SusyWithDeDx/%s.merged", ".*root", 1)

Winos = [ Wino_M_300_cTau_3  , Wino_M_300_cTau_10 , Wino_M_300_cTau_30 , Wino_M_500_cTau_10, Wino_M_650_cTau_10, Wino_M_800_cTau_10, Wino_M_1000_cTau_10, Wino_M_500_cTau_20, Wino_M_650_cTau_20, Wino_M_800_cTau_20, Wino_M_1000_cTau_20 ]

Top = [
  TTJets
       # TTLep
       #, TTHad
       #, TTSemi
       ] + Ts
VV  = [ WW,
        WZ,
        ZZ 
      ]

Zll = [
    DYJetsM50_HT100to200,  
    DYJetsM50_HT200to400,  
    DYJetsM50_HT400to600,  
    DYJetsM50_HT600to800,
    DYJetsM50_HT800to1200,
    #DYJetsM50_HT1200to2500,
    #DYJetsM50_HT2500toInf,
]


#SelectedSamples = [
    ##QCD_HT100to200,
    ##TTSemi,
    ##TBar_tch,
    #WJets_HT100to200,
    #WJets_HT600to800,
    #ZvvJets_HT600to800,
#]


if region == "sr":   
    mcSamples =  ( 
      #SelectedSamples
                   QCD
                 + Ws
                 + Zvv
                 + Zll 
                 + VV
                 + Top
                 )
    mcSignals = Winos
    mcTriggers = triggers_SOS_highMET[:] 
elif region == "cr1l": 
    mcSamples =  (
                   #QCD
                 #+ Ws
                 Zll 
                 #+ VV
                 #+ Top
                 )
    mcTriggers = triggers_1mu_iso + triggers_1e_iso + triggers_1e_noniso
    mcSignals = []

autoAAA(mcSamples)
cropToLumi(mcSamples, 10*41.7)
for c in mcSamples + mcSignals:
    c.triggers = mcTriggers

## Data
from CMGTools.RootTools.samples.samples_13TeV_DATA2018 import *
if region == "sr":   
    datasetsAndTriggers = [ ("MET", triggers_SOS_highMET) ]
elif region == "cr1l":   
    datasetsAndTriggers = [ ("SingleMuon", triggers_1mu_iso) #,
                            #("SingleElectron", triggers_1e_iso + triggers_1e_noniso)
                          ]

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
dataSamples = []; vetoTriggers = []
for (pdname, trigs) in datasetsAndTriggers:
    for d in dataSamples_1Apr2019:
        if pdname in d.name:
            d.json = json
            d.triggers = trigs[:]
            d.vetoTriggers = vetoTriggers[:]
            dataSamples.append(d)
    vetoTriggers += trigs

run = getHeppyOption("run","all")
if run == "all":    selectedComponents = mcSamples + dataSamples + mcSignals
elif run == "data": selectedComponents = dataSamples
elif run == "mc":   selectedComponents = mcSamples
elif run == "sig":  selectedComponents = mcSignals
elif run == "aod":
    from CMGTools.RootTools.samples.samples_13TeV_DATA2017_AOD import dataSamples_17Nov2017_AOD
    selectedComponents = [ d for d in dataSamples_17Nov2017_AOD 
                           if "DoubleMuon" in d.name or "ZeroBias" in d.name ]

if run == "sig" or run == "mc" : isoTrackDeDxAna.doDeDx = True

# apply de/dx calibration if run on data
if run == "data" :
    isoTrackDeDxAna.doCalibrateScaleDeDx = True



if run == "data":
    for c in  selectedComponents:
       c.splitFactor = len(c.files)/3

if run == "mc":
    for c in  selectedComponents:
       c.splitFactor = len(c.files)/2

if run == "aod":
    prescaleComponents(selectedComponents, int(getHeppyOption("prescale","1")))
    configureSplittingFromTime(selectedComponents, 50, 2.5, maxFiles=4)

#-------- SEQUENCE -----------
sequence = cfg.Sequence( xtracks_sequence )
if run == "aod":
    sequence = cfg.Sequence( xtracks_sequence_AOD )


#
# Updates for 2018 data/MC
#

#
# electron id updated to MVA WP tight
#
lepAna.loose_electron_id = "POG_Cuts_ID_FALL17_94X_v1_ConvVetoDxyDz_Veto"  # is this actually used anywhere??
lepAna.ele_tightId = "Cuts_FALL17_94X_v1_ConvVetoDxyDz"     # in 2017 it was "Cuts_FALL17_94X_v1_ConvVetoDxyDz"
#lepAna.ele_tightId = "MVA"     # in 2017 it was "Cuts_FALL17_94X_v1_ConvVetoDxyDz"
#     by setting to "MVA", you get: "POG_MVA_ID_Trig_full5x5" from LeptonAnalyzer.py
#        that means, from Electron.py: "self.mvaIDTight(full5x5=True)"
#        that is actually defined here: https://github.com/CERN-PH-CMG/cmg-cmssw/blob/0fdfc10e2a2d4732cbb5d540b46543498cb6d006/PhysicsTools/Heppy/python/physicsutils/ElectronMVAID.py
#            https://github.com/CERN-PH-CMG/cmg-cmssw/blob/0fdfc10e2a2d4732cbb5d540b46543498cb6d006/PhysicsTools/Heppy/python/physicsutils/ElectronMVAID.py#L62-L68
#            ---> EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigV0_Cat1.weights.xml.gz and similar
# BUT
#
#    EgammaAnalysis/ElectronTools/data/ is EMPTY!
#



#-------- HOW TO RUN -----------
test = getHeppyOption('test')
if test == "1":
    if getHeppyOption("sample"):
        selected = [ s for s in selectedComponents if getHeppyOption("sample") == s.name ]
        if not selected:
            print "Sample %s not found. Known samples are: %s" % [ getHeppyOption("sample"), ", ".join(sorted(s.name for s in selectedComponents)) ]
            sys.exit(1)
        selectedComponents = selected
    print "The test wil use %s " % selectedComponents[0].name
    selectedComponents = doTest1(selectedComponents[0], sequence=sequence, cache=True )
    print "The test wil use file %s " % selectedComponents[0].files[0]
elif test == "1S":
    comp = selectedComponents[0]
    comp.name = "Signal"
    comp.files = [ '/eos/cms/store/cmst3/user/gpetrucc/SusyWithDeDx/Wino_M_500_cTau_10.merged/Wino_M_500_cTau_10.MiniAODv2_job1.root' ]
    selectedComponents = doTest1(comp, sequence=sequence, cache=False )
    print "The test wil use file %s " % comp.files[0]
    fastJetSkim.minJets = 0
    isoTrackDeDxAna.doDeDx = True
    comp.triggers = []
elif test == "1D":
    comp = dataSamples[0]
    #comp.files = [ ': /store/data/Run2017D/DoubleEG/MINIAOD/31Mar2018-v1/00000/C0914411-F636-E811-8796-44A84225D36F.root ' ]
    comp.files = [ '/tmp/amassiro/test3.root ' ]
    selectedComponents = doTest1(comp, sequence=sequence, cache=False )
    print "The test wil use file %s " % comp.files[0]
    fastJetSkim.minJets = 0
    isoTrackDeDxAna.doDeDx = True
    isoTrackDeDxAna.doCalibrateScaleDeDx = True
    comp.triggers = []
elif test == "1E": 
    comp = mcSamples[0]
    #comp.files = [ ': /store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/90000/FB3B40F9-0C73-C144-BB08-8E2DFB7AD448.root ' ]
    comp.files = [ '/tmp/amassiro/FB3B40F9-0C73-C144-BB08-8E2DFB7AD448.root' ]
    selectedComponents = doTest1(comp, sequence=sequence, cache=False )
    print "###########################"
    print "Test 1E "
    print "The test wil use file %s " % comp.files[0]
    fastJetSkim.minJets = 0
    isoTrackDeDxAna.doDeDx = True
    isoTrackDeDxAna.doCalibrateScaleDeDx = True
    comp.triggers = [] 
elif test == "1A":
    comp = dataSamples[0]
    comp.name = "AOD"
    comp.files = [ '/eos/cms/store/cmst3/user/gpetrucc/Run2017D_ZeroBias_17Nov2017_AOD.root' ]
    comp.triggers = []
    sequence = cfg.Sequence( xtracks_sequence_AOD )
    selectedComponents = doTest1(comp, sequence=sequence, cache=False )
    print "The test wil use file %s " % comp.files[0]
elif test in ('2','3','5s'):
    doTestN(test,selectedComponents)

print " sequence = " , sequence
print " run = " , run
print " selectedComponents = " , selectedComponents
print " region = " , region


printSummary(selectedComponents)
if getHeppyOption("justSummary",False): sys.exit(0)
config = autoConfig(selectedComponents, sequence)


