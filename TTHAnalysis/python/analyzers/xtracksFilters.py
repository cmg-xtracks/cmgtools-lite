from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.framework.event import Event
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.HeppyCore.utils.deltar import deltaR2
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

class xtracksFilters( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(xtracksFilters,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(xtracksFilters, self).declareHandles()

    def beginLoop(self,setup):
        super(xtracksFilters,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        if self.cfg_ana.region == "sr":
            count.register('pass jetPtCuts')
            count.register('pass met')
            count.register('pass metNoMu')
        elif self.cfg_ana.region == "cr1l":
            count.register('pass lep')
            count.register('pass lepTrigMatch')
            count.register('pass lepTrackPair')
        count.register('accepted events')


    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        #print "xtracksFilters "

        if self.cfg_ana.region == "sr":
            jets = getattr(event, self.cfg_ana.jets)
            for i,ptCut in enumerate(self.cfg_ana.jetPtCuts):
                if len(jets) <= i or jets[i].pt() <= ptCut:
                    return False
            self.counters.counter('events').inc('pass jetPtCuts')
            
            if float(self.cfg_ana.metCut) > 0 and event.met.pt() <= self.cfg_ana.metCut:
                return False
            self.counters.counter('events').inc('pass met')

            if float(self.cfg_ana.metNoMuCut) > 0 and event.metNoMu.pt() <= self.cfg_ana.metNoMuCut:
                return False
            self.counters.counter('events').inc('pass metNoMu')

        elif self.cfg_ana.region == "cr1l":
            #print "len(event.selectedLeptons) = " , len(event.selectedLeptons)
            if len(event.selectedLeptons) == 0: return False
            self.counters.counter('events').inc('pass lep')

            trigMatchLep = [ l for l in event.selectedLeptons if l.pt() > 27 and l.matchedTrgObjSingleLep ]
            if len(trigMatchLep) == 0: return False
            self.counters.counter('events').inc('pass lepTrigMatch')

            passPair = False
            for t in event.isoTracks:
                t.trigLepton = None
                for l in trigMatchLep:
                    if deltaR2(t,l) > 1.0:
                        passPair = True
                        t.trigLepton = l
                        break
            if not passPair: return False
            self.counters.counter('events').inc('pass lepTrackPair')

        self.counters.counter('events').inc('accepted events')
        return True
