import os.path

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Electron import Electron

import ROOT
from CMGTools.RootTools.utils.trackerTopologyHelper import loadTrackerTopology


from PhysicsTools.HeppyCore.utils.deltar import deltaR, matchObjectCollection3

def leading(objs):
    if len(objs) == 0: return None
    return max(objs, key = lambda obj : obj.pt())
def closest(center, objs):
    if len(objs) == 0: return None
    return min(objs, key = lambda obj : deltaR(center.eta(), center.phi(), obj.eta(), obj.phi()))
def nearby(center, objs, dr):
    return [ o for o in objs if deltaR(center.eta(), center.phi(), o.eta(), o.phi()) < dr ]
def cleaned(center, objs, dr):
    return [ o for o in objs if deltaR(center.eta(), center.phi(), o.eta(), o.phi()) >= dr ]
def jetStats(objs):
    return dict( ht = sum((o.pt() for o in objs), 0),
                 num = len(objs) )



import random


import pandas as pd 

#
# Calibration of dE/dx for data
#

cmssw_base = os.getenv('CMSSW_BASE')
scale_file = cmssw_base + "/src/CMGTools/TTHAnalysis/data/scale_for_cmssw.txt"
scale_file_values = pd.read_csv(scale_file, delim_whitespace=True, comment='#', header = None)
scale_file_values.columns = ["pix", "layerorside", "ladderorblade", "etaMin", "etaMax", "irunMin", "irunMax", "value"]

def scaleDedx( dedx, pix, layerorside, ladderorblade, eta, irun) :
  scale = scaleFactor (pix, layerorside, ladderorblade, eta, irun)
  return dedx * scale

def scaleFactor( pix, layerorside, ladderorblade, eta, irun ) :
  df = scale_file_values
  df_result = df[ (pix == df['pix']) &   
                  (layerorside == df['layerorside']) &   
                  (ladderorblade == df['ladderorblade']) &   
                  (eta >= df['etaMin']) & (eta < df['etaMax']) &   
                  (irun >= df['irunMin']) & (irun < df['irunMax'])                  
                  ]
  if len(df_result.index) == 0 :
    # if not defined scale = 1
    #print " pix, layerorside, ladderorblade, eta, irun = ", pix, " ", layerorside, " ", ladderorblade, " ", eta, " ", irun, " ---> NONE " 
    return 1.0  
  else :
    #print " pix, layerorside, ladderorblade, eta, irun = ", pix, " ", layerorside, " ", ladderorblade, " ", eta, " ", irun, " ---> " , df_result.iloc[0]['value']
    return df_result.iloc[0]['value']


#
# Smearing of dE/dx for MC
#

smear_file = cmssw_base + "/src/CMGTools/TTHAnalysis/data/smear_for_cmssw.txt"
smear_file_values = pd.read_csv(smear_file, delim_whitespace=True, comment='#', header = None)
smear_file_values.columns = ["pix", "layerorside", "etaMin", "etaMax", "value", "iedge"]


def smearDedx( dedx, pix, layerorside, ladderorblade, eta) :
  sigmarel = smearFactor (pix, layerorside, eta)
  if sigmarel != 0:
    smearing = random.gauss(1.0, sigmarel)
  else :
    smearing = 1.0
  if smearing<=0: smearing = 1 # remove unphysical behaviour
  return dedx * smearing

def smearFactor( pix, layerorside, eta ) :
  df = smear_file_values
  df_result = df[ (pix == df['pix']) &   
                  (layerorside == df['layerorside']) &   
                  (eta >= df['etaMin']) & (eta < df['etaMax'])
                  ]
  if len(df_result.index) == 0 :
    # if not defined smear = 0
    return 0.0  
  else :
    return df_result.iloc[0]['value']






class isoTrackDeDxAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(isoTrackDeDxAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.topology = loadTrackerTopology(os.path.expandvars(cfg_ana.trackerTopology[0]), cfg_ana.trackerTopology[1])

    def declareHandles(self):
        super(isoTrackDeDxAnalyzer, self).declareHandles()
        self.handles['dedx'] = AutoHandle("isolatedTracks","edm::Association<reco::DeDxHitInfoCollection>")            
        self.handles['vertex'] = AutoHandle("offlineSlimmedPrimaryVertices","vector<reco::Vertex>")


    def beginLoop(self, setup):
        super(isoTrackDeDxAnalyzer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('selected iso track')
        count.register('accepted events')

    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        muons = []
        electrons = []
        for i,l in enumerate(event.selectedLeptons):
            l.index = i
            if abs(l.pdgId()) == 13: muons.append(l)
            if abs(l.pdgId()) == 11: electrons.append(l)

        for i,l in enumerate(event.selectedTaus):
            l.index = i

        for i,l in enumerate(event.cleanJets):
            l.index = i

        getDeDxRef = self.handles['dedx'].product().get
        if self.cfg_ana.doDeDx == "94XMiniAODv1-Hack":
            fixed = self.handles['dedx'].product().fixOffsets(-1)
            getDeDxRef = fixed.get
        
        event.isoTracks = []
        
        getVertexRef = self.handles['vertex'].product()

        vertex = None

        for v in getVertexRef:
          if(v.isFake() == 0 and v.ndof() > 4 and abs(v.z()) <= 24 and v.position().rho() < 2):
            vertex = v
            break

        if(vertex is None):
          print("ERROR: no primary vertex passing all cuts was found for the event!")
          event.vx = 999
          event.vy = 999
          event.vz = 999
        else:
          event.vx = vertex.x()
          event.vy = vertex.y()
          event.vz = vertex.z()

        pixelChargeToEnergyCoefficient = 3.61e-6
        stripChargeToEnergyCoefficient = 3.61e-6 * 265

        
        for t in event.preselIsoTracks:
            # add more variables
            t.leadAwayJet = leading(cleaned(t,  event.cleanJets, 0.4))
            t.awayJetInfo = jetStats(cleaned(t, event.cleanJets, 0.4))
            t.leadAwayMu  = leading(cleaned(t, muons, 0.4))
            t.leadAwayEle = leading(cleaned(t, electrons, 0.4))
            t.leadAwayTau = leading(cleaned(t, event.selectedTaus, 0.4))
            t.closestMu   = closest(t, nearby(t, muons, 0.4))
            t.closestEle  = closest(t, nearby(t, electrons, 0.4))
            t.closestTau  = closest(t, nearby(t, event.selectedTaus, 0.4))
            
            t.dedxByHit           = [0 for i in xrange(14)]
            t.deByHit             = [0 for i in xrange(14)]
            t.dxByHit             = [0 for i in xrange(14)]
            t.dedxUnSmearedByHit  = [0 for i in xrange(14)]    # unsmeared dedx. For MC the dedx is smeared according to data/mc discrepancy, but the unsmeared is kept for future use
            t.subDetIdByHit       = [0 for i in xrange(14)]
            t.pixByHit            = [0 for i in xrange(14)]    # 0 = strips, 1 = bpix, 2 = fpix
            t.layerOrSideByHit    = [0 for i in xrange(14)]
            t.ladderOrBladeByHit  = [0 for i in xrange(14)]
            t.diskByHit           = [0 for i in xrange(14)]
            t.sideByHit           = [0 for i in xrange(14)]
            t.moduleByHit         = [0 for i in xrange(14)]
            t.sizeXbyHit          = [0 for i in xrange(14)]
            t.sizeYbyHit          = [0 for i in xrange(14)]
            
            # get dedx
            if self.cfg_ana.doDeDx:
                ref = getDeDxRef(t.index)
                if ref.isNull():
                    print "ERROR: no dE/dx for track of pt %.2f, eta %.2f" % (t.pt(),t.eta())
                    continue
                dedx = ref.get(); 
                nhits = dedx.size()
                # this below is just dummy to give you a template
                mysum = 0

                for ih in xrange(min(nhits,len(t.dedxByHit))):
                    detid = dedx.detId(ih)
                    pixelCluster = dedx.pixelCluster(ih)
                    stripCluster = dedx.stripCluster(ih)
                    if pixelCluster:
                      t.dedxByHit[ih] = pixelCluster.charge()/dedx.pathlength(ih)
                      # convert number of electrons to MeV
                      t.dedxByHit[ih] *= pixelChargeToEnergyCoefficient

                      t.deByHit[ih] = (pixelCluster.charge()*pixelChargeToEnergyCoefficient)
                      t.dxByHit[ih] = dedx.pathlength(ih)
                      
                      t.sizeXbyHit[ih] = pixelCluster.sizeX()
                      t.sizeYbyHit[ih] = pixelCluster.sizeY()
                      
                      # barrel
                      if detid.subdetId() == 1:
                          t.layerOrSideByHit[ih] = self.topology.layer(detid)
                          t.ladderOrBladeByHit[ih] = self.topology.pxbLadder(detid)
                          t.pixByHit[ih] = 1
                     
                      # endcap
                      if detid.subdetId() == 2:
                          t.layerOrSideByHit[ih] = self.topology.pxfDisk(detid)
                          #t.layerOrSideByHit[ih] = 2*self.topology.side(detid)-3 # side is 2 for eta > 0, 1 for eta < 0 -> map to +1, -1
                          t.ladderOrBladeByHit[ih] = self.topology.pxfBlade(detid)
                          t.diskByHit[ih]          = self.topology.pxfDisk(detid)
                          t.sideByHit[ih] = 2*self.topology.side(detid)-3 # side is 2 for eta > 0, 1 for eta < 0 -> map to +1, -1
                          t.pixByHit[ih] = 2
                      t.moduleByHit[ih] = self.topology.module(detid)

                      mysum += pixelCluster.charge()

                      #
                      #  https://github.com/cms-sw/cmssw/blob/master/DataFormats/TrackReco/interface/DeDxHitInfo.h
                      #
                      #  dEdX object DeDxHitInfoCollection
                      #
                      #
                      #  https://github.com/cms-sw/cmssw/blob/master/DataFormats/SiPixelDetId/interface/PXBDetId.h
                      #  https://github.com/cms-sw/cmssw/blob/master/DataFormats/SiPixelDetId/interface/PXFDetId.h
                      #


                    # strips                      
                    if stripCluster:
                      t.dedxByHit[ih] = stripCluster.charge()/dedx.pathlength(ih)
                      # convert number of electrons to MeV
                      t.dedxByHit[ih] *= stripChargeToEnergyCoefficient
                      #t.sizeXbyHit[ih] = stripCluster.sizeX() --> 'SiStripCluster' object has no attribute 'sizeX'
                      t.layerOrSideByHit[ih] = self.topology.layer(detid)

                      t.deByHit[ih] = (stripCluster.charge()*stripChargeToEnergyCoefficient)
                      t.dxByHit[ih] = dedx.pathlength(ih)

                    
                    t.subDetIdByHit[ih] = detid.subdetId()

                    # save unsmeared and smear (for MC) and the un-scaled (for Data)
                    t.dedxUnSmearedByHit[ih] = t.dedxByHit[ih]
                    
                    if self.cfg_comp.isMC: # if MC
                      if pixelCluster: # if pixel
                        t.dedxByHit[ih] = smearDedx( t.dedxByHit[ih], t.pixByHit[ih], t.layerOrSideByHit[ih], t.ladderOrBladeByHit[ih], abs(t.eta()) )

                    #print " run = ", event.run 
                    if not self.cfg_comp.isMC: # if data
                      if self.cfg_ana.doCalibrateScaleDeDx: # if scale activated
                        if pixelCluster: # if pixel
                          t.dedxByHit[ih] = scaleDedx( t.dedxByHit[ih], t.pixByHit[ih], t.layerOrSideByHit[ih], t.ladderOrBladeByHit[ih], abs(t.eta()), event.run )


                   
                t.myDeDx = mysum
            else:
                t.myDeDx = 0

            # add a flag for bad ECAL channels in the way of the track
            t.channelsGoodECAL = 1
            for ie in t.crossedEcalStatus():
                if ie != 0: t.channelsGoodECAL = 0

            # add a flag for bad HCAL channels in the way of the track
            t.channelsGoodHCAL = 1
            for ih in t.crossedHcalStatus():
                if (ih & (1<<5)) != 0: t.channelsGoodHCAL = 0



            # add to the list
            event.isoTracks.append(t)

        if len(event.isoTracks) == 0: 
            return False
        self.counters.counter('events').inc('selected iso track')

        if self.cfg_comp.isMC: # do MC matching
            event.genCharginos = [ g for g in event.generatorSummary if abs(g.pdgId()) in (1000024,1000037)]
            for i,g in enumerate(event.genCharginos):
                g.index = i
                g.decayPoint = g.vertex()
                if g.numberOfDaughters() > 1:
                    for i in xrange(g.numberOfDaughters()):
                        dau = g.daughter(i)
                        if dau: 
                            g.decayPoint = dau.vertex()
                            break
                #print "GEN pdgId %+8d pt %7.1f eta %+6.2f phi %+6.2f status %3d daughters %d decay R %5.1f, z %+5.1f" % (g.pdgId(), g.pt(), g.eta(), g.phi(), g.status(), g.numberOfDaughters(), g.decayPoint.R(), g.decayPoint.Z())
            match = matchObjectCollection3(event.isoTracks, event.genCharginos, deltaRMax = 0.1)
            for t in event.isoTracks:
                t.mcMatch = match[t]
                #print "REC charge %+7d pt %7.1f eta %+6.2f phi %+6.2f" % (t.charge(), t.pt(), t.eta(), t.phi())
            #    for t in event.isoTracks:
            #        if deltaR(g,t) < 0.3:
            #            print " -> charge %+7d pt %7.1f eta %+6.2f phi %+6.2f   dr %.4f" % (t.charge(), t.pt(), t.eta(), t.phi(), deltaR(g,t))
            #print "\n"

            ## Now we add a generic match to charginos + prompt leptons + prompt taus + prompt photons
            anyMatchable = event.genCharginos[:]
            anyMatchable += [ x for x in event.genParticles if abs(x.pdgId()) in (11,13) and (x.isPromptFinalState() or x.isDirectPromptTauDecayProductFinalState()) ]
            anyMatchable += [ x for x in event.genParticles if abs(x.pdgId()) == 15 and x.isPromptDecayed() and x.pt() > 10 ]
            anyMatchable += [ x for x in event.genParticles if x.pdgId() == 22 and x.isPromptFinalState() and x.pt() > 20 ]
            matchAny = matchObjectCollection3(event.isoTracks, anyMatchable, deltaRMax = 0.2)
            for t in event.isoTracks:
                t.mcMatchAny = matchAny[t]


        # do any more event selection
        self.counters.counter('events').inc('accepted events')
        return True

