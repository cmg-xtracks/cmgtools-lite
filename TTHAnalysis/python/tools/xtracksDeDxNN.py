from CMGTools.TTHAnalysis.treeReAnalyzer import *
from keras.models import load_model
import numpy as np

class NNVar:
    def __init__(self,name,func=None):
        self.name = name
        self.func = func
    def __call__(self,obj):
        return self.func(obj) if self.func else getattr(obj,self.name)

class NN:
    def __init__(self,name,modelfile,nnvars):
        self.name = name
        self.model = load_model(modelfile)
        self.nnvars = nnvars[:]
        self.indata = np.empty([1, len(self.nnvars)])
    def __call__(self,obj,debug=False):
        row = self.indata[0]
        for i,v in enumerate(self.nnvars):
            row[i] = v(obj)
        if debug: 
            print "   Input: ", row
        return self.model.predict(self.indata)[0]

class NNCollectionFriend:
    def __init__(self,collection,name,modelfile,nnvars,preselection=lambda x : True, nouts=1,nitems=10):
        self.name = name
        self.collection = collection
        self.preselection = preselection
        self._nouts = nouts
        if nouts != 1: raise RuntimeError("Watch out, code was not tested with nouts > 1")
        self._nn = NN(name,modelfile,nnvars)
        self._branches = [ ("n%s" % self.collection, "I") ]
        if self._nouts == 1:
            self._branches.append( ("%s_%s" % (self.collection, self.name), "F", nitems, "n%s" % self.collection) )
        else:
            for iout in xrange(self._nouts):
                self._branches.append( ("%s_%s_out%d" % (self.collection, self.name, iout+1), "F", nitems, "n%s" % self.collection) )
    def listBranches(self):
        return self._branches
    def __call__(self,event,debug=False):
        objs = Collection(event, self.collection)
        ret = { ("n%s" % self.collection) : len(objs) }
        outs = [ [ -99 for io in xrange(len(objs)) ] for i in xrange(self._nouts) ]
        for io,o in enumerate(objs):
            if debug: print "object #%d" % io
            if not self.preselection(o): continue
            ovals = self._nn(o,debug=debug)
            if debug: print "   Output: ", ovals
            for i in xrange(self._nouts):
                outs[i][io] = ovals[i]
        if self._nouts == 1:
            ret["%s_%s" % (self.collection, self.name)] = outs[0]
        else:
            for i in xrange(self._nouts):
                ret["%s_%s_out%d" % (self.collection, self.name, i+1)] = outs[i]
        return ret


MODULES = [
    ( 'dedxNN4h', lambda : NNCollectionFriend("IsoTrack","dedxNN4h","/afs/cern.ch/work/g/gpetrucc/SusyWithDeDx/CMSSW_9_4_6_patch1/src/CMGTools/TTHAnalysis/macros/xtracks/dedx_model.h5",[
                    NNVar("dedxByLayer0"), NNVar("dedxByLayer1"), NNVar("dedxByLayer2"), NNVar("dedxByLayer3"),
                    NNVar("sizeXbyLayer0"), NNVar("sizeXbyLayer1"), NNVar("sizeXbyLayer2"), NNVar("sizeXbyLayer3"),
                    NNVar("sizeYbyLayer0"), NNVar("sizeYbyLayer1"), NNVar("sizeYbyLayer2"), NNVar("sizeYbyLayer3"),
                    ], preselection = lambda x : x.pixelHits >= 4) ),
]
if __name__ == '__main__':
    from sys import argv
    import ROOT
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.nn = NNCollectionFriend("IsoTrack","dedxModel","/afs/cern.ch/work/g/gpetrucc/SusyWithDeDx/CMSSW_9_4_6_patch1/src/CMGTools/TTHAnalysis/macros/xtracks/dedx_model.h5",[
                    NNVar("dedxByLayer0"), NNVar("dedxByLayer1"), NNVar("dedxByLayer2"), NNVar("dedxByLayer3"),
                    NNVar("sizeXbyLayer0"), NNVar("sizeXbyLayer1"), NNVar("sizeXbyLayer2"), NNVar("sizeXbyLayer3"),
                    NNVar("sizeYbyLayer0"), NNVar("sizeYbyLayer1"), NNVar("sizeYbyLayer2"), NNVar("sizeYbyLayer3"),
                    ], preselection = lambda x : x.pixelHits >= 4)
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d" % (ev.run, ev.lumi, ev.evt)
            print self.nn(ev,debug=True)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
