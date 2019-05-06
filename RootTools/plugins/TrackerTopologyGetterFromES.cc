#include <iostream>
#include <string>

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

//#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
//#include "Geometry/Records/interface/TrackerTopologyRcd.h"
#include "Geometry/Records/interface/PTrackerParametersRcd.h"
#include "CondFormats/GeometryObjects/interface/PTrackerParameters.h"
#include <TFile.h>


class TrackerTopologyGetterFromES: public edm::one::EDAnalyzer<>
{
public:
  explicit TrackerTopologyGetterFromES( const edm::ParameterSet & ) ;
  ~TrackerTopologyGetterFromES() override ;
  void analyze( const edm::Event &, const edm::EventSetup & ) override ;
  
private:
  std::string theOutputFileName;
  std::string theOutputObjectName;
  bool once_;
};

TrackerTopologyGetterFromES::TrackerTopologyGetterFromES( const edm::ParameterSet & conf ) :
theOutputFileName(conf.getUntrackedParameter<std::string>("outputFileName")),
theOutputObjectName(conf.getUntrackedParameter<std::string>("outputObjectName", "TrackerTopology")),
once_(true)
{
}

TrackerTopologyGetterFromES::~TrackerTopologyGetterFromES()
{
}

void
TrackerTopologyGetterFromES::analyze( const edm::Event & iEvent, const edm::EventSetup & iSetup ) 
{
  if (once_) {
    once_ = false;
    //edm::ESHandle<TrackerTopology> tTopoHandle;
    //iSetup.get<TrackerTopologyRcd>().get(tTopoHandle);
    edm::ESHandle<PTrackerParameters> tTopoHandle;
    iSetup.get<PTrackerParametersRcd>().get(tTopoHandle);
    TFile *fOut = TFile::Open(theOutputFileName.c_str(), "RECREATE");
    fOut->WriteObject(tTopoHandle.product(), theOutputObjectName.c_str());
    fOut->Close();
    std::cout << "Wrote output to " << theOutputFileName << std::endl;
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(TrackerTopologyGetterFromES);
