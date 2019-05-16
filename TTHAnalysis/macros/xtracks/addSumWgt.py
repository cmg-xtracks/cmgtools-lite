import glob
import pickle
import sys
from ROOT import *
from array import array


args = sys.argv[1:]
if len(args) != 3:
    print "Need three command line arguments -- sample folder, sample string and k-factor ID (0 for k-factor=1 , 1 for Z, 2 for W)"
    quit()

path   = args[0]
sample = args[1]
kid    = int(args[2])

if kid != 0 and kid != 1 and kid != 2 :
    print "Third should should be either 0, 1 or 2"
    quit()
if kid == 1 : 
    print "Adding NLO K-factors for Z+jets"
if kid == 2 : 
    print "Adding NLO K-factors for W+jets"

sumwgt = 0.0

pckfile  = path+sample+"/skimAnalyzerCount/SkimReport.pck"
pckobj   = pickle.load(open(pckfile,'r'))
counters = dict(pckobj)
sumwgt  += counters['Sum Weights']

kfactfile = TFile("KFactors/kfactors.root")
zknum = kfactfile.Get("EWKcorr/Z");
zkden = kfactfile.Get("ZJets_LO/inv_pt");
wknum = kfactfile.Get("EWKcorr/W");
wkden = kfactfile.Get("WJets_LO/inv_pt");

zkfact = zknum.Clone("zkfact");
wkfact = wknum.Clone("wkfact");
zkfact.Divide(zkden);
wkfact.Divide(wkden);

wgtsum = array( 'f', [ 0 ] )
kfact  = array( 'f', [ 0 ] )
wgtsum[0] = sumwgt
kfact[0] = 1.0    
print "Sum of weights for " + sample + ": " + str(wgtsum[0])

treefile = TFile(path+sample+"/treeProducerXtracks/tree.root", "update")
tree     = treefile.Get("tree")
entries  = tree.GetEntries()

bwgtsumexists = False
bkfactexists  = False
for branch in tree.GetListOfBranches():
    if( branch.GetName() == "wgtsum" ) :
        bwgtsumexists = True
        print "Branch wgtsum already exists, will not do anything to it"
    if( branch.GetName() == "kfact" ) :
        bkfactexists = True
        print "Branch kfact already exists, will not do anything to it"

bwgtsum = None
bkfact  = None
if not bwgtsumexists :
    bwgtsum = tree.Branch('wgtsum', wgtsum, 'wgtsum/F')
if not bkfactexists :
    bkfact  = tree.Branch('kfact' , kfact , 'kfact/F')

counter = 0
for entry in tree :
    if (counter % 10000 == 0) :
        print "Processing event : " + str(counter+1)

    kfact[0] = 1.0
    if kid != 0 :
        vpt = entry.lheVpt
        if vpt > 0. and vpt < 150.1 :
            vpt = 150.1
        if vpt > 1199.9 :
            vpt = 1199.9

        if vpt > 0. and kid == 1 :
            kfact[0] = zkfact.GetBinContent(zkfact.FindBin(vpt));
        if vpt > 0. and kid == 2 :  
            kfact[0] = wkfact.GetBinContent(wkfact.FindBin(vpt));

    if not bwgtsum == None :
        bwgtsum.Fill()
    if not bkfact == None :
        bkfact .Fill()
    counter = counter+1

print "Total events processed : " + str(counter)

treefile.Write()
treefile.Close()

kfactfile.Close()
