#ifndef TRIM_H
#define TRIM_H

void trim(std::string path, std::string sample, std::string outfilename, bool isMC) {
  
  std::cout << "Trimming sample : " << sample << std::endl;
  
  // PU reweighting  
  TFile filePUData("Pileup/pileup_data2017.root");
  TH1* histPUData = (TH1*)filePUData.Get("pileup");
  
  histPUData->SetName("histPUData");
  histPUData->Scale(1./histPUData->Integral());
  
  TH1* histPUMC = NULL;
  TFile* filePUMC = NULL;
  if (isMC) {
    filePUMC = TFile::Open((path+sample+"/PileUpAnalyzer/rawMCPU.root").c_str());
    histPUMC = (TH1*)filePUMC->Get("pileup");
    histPUMC->Scale(1./histPUMC->Integral());
  }
  TH1* puwgt = (TH1D*) histPUData->Clone("puwgt");
  if (isMC && histPUMC != NULL) puwgt->Divide(histPUMC);
  else puwgt->Divide(histPUData);
  
  // Muon ID, isolation scale factors
  TFile muoidfile("MuonIDIsoTrig/Muon_ID_SF_2017.root");
  TFile muisofile("MuonIDIsoTrig/Muon_Iso_SF_2017.root");
  TH2D* loosemuoidhist = (TH2D*)muoidfile.Get("NUM_LooseID_DEN_genTracks_pt_abseta");
  TH2D* loosemuisohist = (TH2D*)muisofile.Get("NUM_LooseRelIso_DEN_LooseID_pt_abseta");
  TH2D* tightmuoidhist = (TH2D*)muoidfile.Get("NUM_TightID_DEN_genTracks_pt_abseta");
  TH2D* tightmuisohist = (TH2D*)muisofile.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta");
  
  // Extract the TTree from file
  TFile* file = TFile::Open((path+sample+"/treeProducerXtracks/tree.root").c_str());
  if (file == NULL) {
    std::cout << "Unable to open file " << path+sample+"/treeProducerXtracks/tree.root" << " ... quitting\n";
  }
  
  TTreeReader reader("tree", file);
  
  const char* xsecstr = (isMC ? "xsec"     : "rho");
  const char* wsumstr = (isMC ? "wgtsum"   : "rho");
  const char* genwstr = (isMC ? "genWeight": "rho");
  const char* kfacstr = (isMC ? "kfact"    : "rho");
  const char* putrstr = (isMC ? "nTrueInt" : "rho");
  
  TFile* outfile = new TFile((path+sample+"/"+outfilename).c_str(), "RECREATE");
  TTree* outtree = new TTree("tree", "tree");
  
  TTreeReaderValue<Float_t> xsec  (reader, (xsecstr));
  TTreeReaderValue<Float_t> wsum  (reader, (wsumstr));
  TTreeReaderValue<Float_t> genwgt(reader, (genwstr));
  TTreeReaderValue<Float_t> kfac  (reader, (kfacstr));
  TTreeReaderValue<Float_t> putru (reader, (putrstr));
  
  TTreeReaderValue<Int_t>   mettrig      (reader, "HLT_BIT_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight");
  TTreeReaderValue<Int_t>   mutrig       (reader, "HLT_SingleMu"                                 );
  TTreeReaderValue<Int_t>   nvert        (reader, "nVert"                                        );
  
  TTreeReaderValue<Int_t>   flag_nvtx    (reader, "Flag_goodVertices"                            );
  TTreeReaderValue<Int_t>   flag_badmu   (reader, "Flag_BadPFMuonFilter"                         );
  TTreeReaderValue<Int_t>   flag_badch   (reader, "Flag_BadChargedCandidateFilter"               );
  TTreeReaderValue<Int_t>   flag_deadecal(reader, "Flag_EcalDeadCellTriggerPrimitiveFilter"      );
  TTreeReaderValue<Int_t>   flag_eesc    (reader, "Flag_eeBadScFilter"                           );
  TTreeReaderValue<Int_t>   flag_ecalcali(reader, "Flag_ecalBadCalibFilter"                      );
  TTreeReaderValue<Int_t>   flag_hbhe    (reader, "Flag_HBHENoiseFilter"                         );
  TTreeReaderValue<Int_t>   flag_hbheiso (reader, "Flag_HBHENoiseIsoFilter"                      );
  TTreeReaderValue<Int_t>   flag_halo    (reader, "Flag_globalTightHalo2016Filter"               );
  
  TTreeReaderValue<Int_t>   nLep         (reader, "nLepGood"                                     );
  TTreeReaderValue<Int_t>   nTau         (reader, "nTauGood"                                     );
  
  TTreeReaderArray<Int_t>   lep_pdgId    (reader, "LepGood_pdgId"                                );
  TTreeReaderArray<Int_t>   lep_tightId  (reader, "LepGood_tightId"                              );
  TTreeReaderArray<Float_t> lep_iso      (reader, "LepGood_relIso04"                             );
  TTreeReaderArray<Float_t> lep_pt       (reader, "LepGood_pt"                                   );
  TTreeReaderArray<Float_t> lep_eta      (reader, "LepGood_eta"                                  );
  TTreeReaderArray<Float_t> lep_phi      (reader, "LepGood_phi"                                  );
  
  TTreeReaderArray<Float_t> tau_pt       (reader, "TauGood_pt"                                   );
  TTreeReaderArray<Float_t> tau_eta      (reader, "TauGood_eta"                                  );
  TTreeReaderArray<Float_t> tau_phi      (reader, "TauGood_phi"                                  );
  TTreeReaderArray<Int_t>   tau_mvaid    (reader, "TauGood_idMVANewDM"                           );
  
  TTreeReaderValue<Int_t>   nJet         (reader, "nJet"                                         );
  TTreeReaderValue<Int_t>   nJetFwd      (reader, "nJetFwd"                                      );
  
  TTreeReaderArray<Float_t> jet_pt       (reader, "Jet_pt"                                       );
  TTreeReaderArray<Float_t> jet_eta      (reader, "Jet_eta"                                      );
  TTreeReaderArray<Float_t> jet_phi      (reader, "Jet_phi"                                      );
  TTreeReaderArray<Float_t> jet_mass     (reader, "Jet_mass"                                     );
  TTreeReaderArray<Float_t> jet_chf      (reader, "Jet_chHEF"                                    );
  TTreeReaderArray<Float_t> jet_nhf      (reader, "Jet_neHEF"                                    );
  TTreeReaderArray<Float_t> jet_btag     (reader, "Jet_btagDeepCSV"                              );
  
  TTreeReaderArray<Float_t> jetfwd_pt    (reader, "JetFwd_pt"                                    );
  TTreeReaderArray<Float_t> jetfwd_eta   (reader, "JetFwd_eta"                                   );
  TTreeReaderArray<Float_t> jetfwd_phi   (reader, "JetFwd_phi"                                   );
  TTreeReaderArray<Float_t> jetfwd_mass  (reader, "JetFwd_mass"                                  );
  TTreeReaderArray<Float_t> jetfwd_chf   (reader, "JetFwd_chHEF"                                 );
  TTreeReaderArray<Float_t> jetfwd_nhf   (reader, "JetFwd_neHEF"                                 );
  
  TTreeReaderValue<Int_t>   nIso         (reader, "nIsoTrack"                                    );
  TTreeReaderArray<Float_t> iso_pt       (reader, "IsoTrack_pt"                                  );
  TTreeReaderArray<Float_t> iso_eta      (reader, "IsoTrack_eta"                                 );
  TTreeReaderArray<Float_t> iso_phi      (reader, "IsoTrack_phi"                                 );
  TTreeReaderArray<Float_t> iso_dxy      (reader, "IsoTrack_dxy"                                 );
  TTreeReaderArray<Float_t> iso_dz       (reader, "IsoTrack_dz"                                  );
  TTreeReaderArray<Float_t> iso_chiso    (reader, "IsoTrack_dR03IsoCH"                           );
  TTreeReaderArray<Float_t> iso_nhiso    (reader, "IsoTrack_dR03IsoNH"                           );
  TTreeReaderArray<Float_t> iso_phiso    (reader, "IsoTrack_dR03IsoPH"                           );
  TTreeReaderArray<Float_t> iso_puiso    (reader, "IsoTrack_dR03IsoPU"                           );
  TTreeReaderArray<Int_t>   iso_hp       (reader, "IsoTrack_highPurity"                          );
  TTreeReaderArray<Int_t>   iso_trklayers(reader, "IsoTrack_trackerLayers"                       );
  TTreeReaderArray<Int_t>   iso_pixlayers(reader, "IsoTrack_pixelLayers"                         );
  TTreeReaderArray<Int_t>   iso_pixhits  (reader, "IsoTrack_pixelHits"                           );
  TTreeReaderArray<Int_t>   iso_trkhits  (reader, "IsoTrack_trackerHits"                         );
  TTreeReaderArray<Int_t>   iso_mitkhits (reader, "IsoTrack_missingInnerTrackerHits"             );
  TTreeReaderArray<Int_t>   iso_mmtkhits (reader, "IsoTrack_missingMiddleTrackerHits"            );
  TTreeReaderArray<Int_t>   iso_motkhits (reader, "IsoTrack_missingOuterTrackerHits"             );
  TTreeReaderArray<Float_t> iso_dedxl0   (reader, "IsoTrack_dedxByLayer0"                        );
  TTreeReaderArray<Float_t> iso_dedxl1   (reader, "IsoTrack_dedxByLayer1"                        );
  TTreeReaderArray<Float_t> iso_dedxl2   (reader, "IsoTrack_dedxByLayer2"                        );
  TTreeReaderArray<Float_t> iso_dedxl3   (reader, "IsoTrack_dedxByLayer3"                        );
  TTreeReaderArray<Float_t> iso_dedxl4   (reader, "IsoTrack_dedxByLayer4"                        );
  TTreeReaderArray<Float_t> iso_dedxl5   (reader, "IsoTrack_dedxByLayer5"                        );
  
  
  TTreeReaderValue<Float_t> etm          (reader, "metNoMu_pt"                                   );
  TTreeReaderValue<Float_t> etm_phi      (reader, "metNoMu_phi"                                  );
  TTreeReaderValue<Float_t> retm         (reader, "met_pt"                                       );
  TTreeReaderValue<Float_t> retm_phi     (reader, "met_phi"                                      );
  
  
  Float_t       mcweight     =  1.0;
  Float_t       puweight     =  1.0;
  Float_t       idweight     =  1.0;
  Float_t       trweight     =  1.0;
  Float_t       kfact        =  1.0;
  
  UChar_t       nvtx         =  0  ;
  Float_t       putrue       =  0  ;
  
  UChar_t       flags        =  0  ;
  
  UChar_t       hltmet       =  0  ;
  UChar_t       hlt1m        =  0  ;
  
  Float_t       met          =  0.0;
  Float_t       metphi       =  0.0;
  Float_t       rmet         =  0.0;
  Float_t       rmetphi      =  0.0;
  
  UChar_t       nmuons       =  0  ;
  UChar_t       nelecs       =  0  ;
  UChar_t       ntaus        =  0  ;
  
  Char_t        m1id         =  0  ;
  Float_t       m1iso        =  0.0;
  Float_t       m1pt         =  0.0;
  Float_t       m1eta        =  0.0;
  Float_t       m1phi        =  0.0;
  Char_t        m2id         =  0  ;
  Float_t       m2iso        =  0.0;
  Float_t       m2pt         =  0.0;
  Float_t       m2eta        =  0.0;
  Float_t       m2phi        =  0.0;
  
  Float_t       mmpt         =  0.0;
  Float_t       mmeta        =  0.0;
  Float_t       mmphi        =  0.0;
  Float_t       mass         =  0.0;
  Float_t       mt           =  0.0;
  
  Float_t       x1pt         =  0.0;
  Float_t       x1eta        =  0.0;
  Float_t       x1phi        =  0.0;
  Float_t       x1mt         =  0.0;
  UChar_t       x1hits       =  0  ;
  UChar_t       x1layers     =  0  ;
  Float_t       x2pt         =  0.0;
  Float_t       x2eta        =  0.0;
  Float_t       x2phi        =  0.0;
  Float_t       x2mt         =  0.0;
  UChar_t       x2hits       =  0  ;
  UChar_t       x2layers     =  0  ;
  UChar_t       ntracks      =  0  ;
  UChar_t       nxtrks       =  0  ;
  
  Float_t       j1pt         =  0.0;
  Float_t       j1eta        =  0.0;
  Float_t       j1phi        =  0.0;
  Float_t       j1m          =  0.0;
  Float_t       j1chf        =  0.0;
  Float_t       j1nhf        =  0.0;
  Float_t       jetmetdphi   = -1.0;
  Float_t       jetrmetdphi  = -1.0;
  
  UChar_t       nbjets       =  0  ;
  UChar_t       ncjets       =  0  ;
  UChar_t       nfjets       =  0  ;
  
  outtree->Branch("mcweight"    , &mcweight    , "mcweight/F"    );
  outtree->Branch("puweight"    , &puweight    , "puweight/F"    );
  outtree->Branch("idweight"    , &idweight    , "idweight/F"    );
  outtree->Branch("trweight"    , &trweight    , "trweight/F"    );
  outtree->Branch("kfact"       , &kfact       , "kfact/F"       );
  
  outtree->Branch("hltmet"      , &hltmet      , "hltmet/b"      );
  outtree->Branch("hlt1m"       , &hlt1m       , "hlt1m/b"       );
  outtree->Branch("flags"       , &flags       , "flags/b"       );
  outtree->Branch("nvtx"        , &nvtx        , "nvtx/b"        );
  outtree->Branch("putrue"      , &putrue      , "putrue/F"      );
  
  outtree->Branch("met"         , &met         , "met/F"         );
  outtree->Branch("metphi"      , &metphi      , "metphi/F"      );
  outtree->Branch("rmet"        , &rmet        , "rmet/F"        );
  outtree->Branch("rmetphi"     , &rmetphi     , "rmetphi/F"     );
  
  outtree->Branch("nmuons"      , &nmuons      , "nmuons/b"      );
  outtree->Branch("nelecs"      , &nelecs      , "nelecs/b"      );
  outtree->Branch("ntaus"       , &ntaus       , "ntaus/b"       );
  
  outtree->Branch("m1pt"        , &m1pt        , "m1pt/F"        );
  outtree->Branch("m1eta"       , &m1eta       , "m1eta/F"       );
  outtree->Branch("m1phi"       , &m1phi       , "m1phi/F"       );
  outtree->Branch("m1id"        , &m1id        , "m1id/B"        );
  outtree->Branch("m1iso"       , &m1iso       , "m1iso/F"       );
  outtree->Branch("m2pt"        , &m2pt        , "m2pt/F"        );
  outtree->Branch("m2eta"       , &m2eta       , "m2eta/F"       );
  outtree->Branch("m2phi"       , &m2phi       , "m2phi/F"       );
  outtree->Branch("m2id"        , &m2id        , "m2id/B"        );
  outtree->Branch("m2iso"       , &m2iso       , "m2iso/F"       );
  
  outtree->Branch("mmpt"        , &mmpt        , "mmpt/F"        );
  outtree->Branch("mmeta"       , &mmeta       , "mmeta/F"       );
  outtree->Branch("mmphi"       , &mmphi       , "mmphi/F"       );
  outtree->Branch("mass"        , &mass        , "mass/F"        );
  outtree->Branch("mt"          , &mt          , "mt/F"          );
  
  outtree->Branch("j1pt"        , &j1pt        , "j1pt/F"        );
  outtree->Branch("j1eta"       , &j1eta       , "j1eta/F"       );
  outtree->Branch("j1phi"       , &j1phi       , "j1phi/F"       );
  outtree->Branch("j1m"         , &j1m         , "j1m/F"         );
  outtree->Branch("j1chf"       , &j1chf       , "j1chf/F"       );
  outtree->Branch("j1nhf"       , &j1nhf       , "j1nhf/F"       );
  outtree->Branch("jetmetdphi"  , &jetmetdphi  , "jetmetdphi/F"  );
  outtree->Branch("jetrmetdphi" , &jetrmetdphi , "jetrmetdphi/F" );
  
  outtree->Branch("x1pt"        , &x1pt        , "x1pt/F"        );
  outtree->Branch("x1eta"       , &x1eta       , "x1eta/F"       );
  outtree->Branch("x1phi"       , &x1phi       , "x1phi/F"       );
  outtree->Branch("x1mt"        , &x1mt        , "x1mt/F"        );
  outtree->Branch("x1hits"      , &x1hits      , "x1hits/b"      );
  outtree->Branch("x1layers"    , &x1layers    , "x1layers/b"    );
  outtree->Branch("x2pt"        , &x2pt        , "x2pt/F"        );
  outtree->Branch("x2eta"       , &x2eta       , "x2eta/F"       );
  outtree->Branch("x2phi"       , &x2phi       , "x2phi/F"       );
  outtree->Branch("x2mt"        , &x2mt        , "x2mt/F"        );
  outtree->Branch("x2hits"      , &x2hits      , "x2hits/b"      );
  outtree->Branch("x2layers"    , &x2layers    , "x2layers/b"    );
  outtree->Branch("ntracks"     , &ntracks     , "ntracks/b"    );
  outtree->Branch("nxtrks"      , &nxtrks      , "nxtrks/b"      );
  
  outtree->Branch("ncjets"      , &ncjets      , "ncjets/b"      );
  outtree->Branch("nfjets"      , &nfjets      , "nfjets/b"      );
  outtree->Branch("nbjets"      , &nbjets      , "nbjets/b"      );
  
  
  while (reader.Next()) {
    
    kfact  = (isMC ? *kfac  : 1.0);
    putrue = (isMC ? *putru : 1.0);
    
    nvtx  = *nvert;
    hltmet = (*mettrig > 0 ? 1 : 0); 
    hlt1m  = (*mutrig  > 0 ? 1 : 0); 
    
    flags = 0;
    if (*flag_halo     == 0) flags +=   1;
    if (*flag_hbhe     == 0) flags +=   2;
    if (*flag_hbheiso  == 0) flags +=   4;
    if (*flag_deadecal == 0) flags +=   8;
    if (*flag_badmu    == 0) flags +=  16;
    if (*flag_badch    == 0) flags +=  32;
    if (*flag_eesc     == 0) flags +=  64;
    if (*flag_ecalcali == 0) flags += 128;
    
    met     = *etm; 
    metphi  = *etm_phi; 
    rmet    = *retm; 
    rmetphi = *retm_phi; 
    TLorentzVector  metv;
    TLorentzVector rmetv;
    metv .SetPtEtaPhiM( met, 0.,  metphi, 0.);
    rmetv.SetPtEtaPhiM(rmet, 0., rmetphi, 0.);
    
    std::vector<TLorentzVector> electrons;
    std::vector<TLorentzVector> taus;
    std::vector<TLorentzVector> muons;
    std::vector<unsigned> midx;
    
    for (int i = 0; i < (*nLep); i++) {
      if (abs(lep_pdgId[i]) == 11) {
        TLorentzVector electron;
        electron.SetPtEtaPhiM(lep_pt[i], lep_eta[i], lep_phi[i], 5.11e-4);
        electrons.push_back(electron);
      }                
      if (abs(lep_pdgId[i]) == 13) {
        midx.push_back(i);
        TLorentzVector muon;
        muon.SetPtEtaPhiM(lep_pt[i], lep_eta[i], lep_phi[i], 0.1057);
        muons.push_back(muon);
      }
    }
    for (int i = 0; i < (*nTau); i++) {
      TLorentzVector tau;
      tau.SetPtEtaPhiM(tau_pt[i], tau_eta[i], tau_phi[i], 1.77);
      bool overlap = false;
      for (std::size_t j = 0; j < muons.size(); j++) {
        if (tau.DeltaR(muons[j]) < 0.4) overlap = true;
      }
      for (std::size_t j = 0; j < electrons.size(); j++) {
        if (tau.DeltaR(electrons[j]) < 0.4) overlap = true;
      }
      if (overlap) continue;
      if (tau_mvaid[i] < 2) continue;
      taus.push_back(tau);                               
    }
    
    ntaus  = taus.size();
    nelecs = electrons.size();
    nmuons = muons.size();
    
    mt    = 0.0;
    mass  = 0.0;
    mmpt  = 0.0;
    mmeta = 0.0;
    mmphi = 0.0;
    if (midx.size() == 1) {
      m1pt  = muons[0].Pt();
      m1eta = muons[0].Eta();
      m1phi = muons[0].Phi();
      
      m1iso = lep_iso[midx[0]];
      m1id  = 1 * lep_pdgId[midx[0]] / abs(lep_pdgId[midx[0]]);
      if (lep_tightId[midx[0]] == 1 && lep_iso[midx[0]] < 0.15) m1id *= 3;
      
      mt = sqrt(2.0 * lep_pt[midx[0]] * rmetv.Pt() * (1. - cos(rmetv.DeltaPhi(muons[0]))));
    }
    if (midx.size() == 2) {
      m1pt  = muons[0].Pt();
      m1eta = muons[0].Eta();
      m1phi = muons[0].Phi();
      
      m1iso = lep_iso[midx[0]];
      m1id  = 1 * lep_pdgId[midx[0]] / abs(lep_pdgId[midx[0]]);
      if (lep_tightId[midx[0]] == 1 && lep_iso[midx[0]] < 0.15) m1id *= 3;
      
      m2pt  = muons[1].Pt();
      m2eta = muons[1].Eta();
      m1phi = muons[1].Phi();
      
      m2iso = lep_iso[midx[1]];
      m2id  = 1 * lep_pdgId[midx[1]] / abs(lep_pdgId[midx[1]]);
      if (lep_tightId[midx[1]] == 1 && lep_iso[midx[1]] < 0.15) m2id *= 3;
      
      TLorentzVector dimuon;
      dimuon += muons[0];
      dimuon += muons[1];
      mass  = dimuon.M();
      mmpt  = dimuon.Pt();
      mmeta = dimuon.Eta();
      mmphi = dimuon.Phi();
    }
    
    ntracks = 0;
    std::vector<TLorentzVector> tracks;
    std::vector<int> tklayers;
    std::vector<int> tkhits;
    for (std::size_t i = 0; i < *nIso; i++) {
      TLorentzVector tk;
      tk.SetPtEtaPhiM(iso_pt[i], iso_eta[i], iso_phi[i], 0.);
      bool overlap = false;
      for (std::size_t j = 0; j < muons.size(); j++) {
        if (tk.DeltaR(muons[j]) < 0.4) overlap = true;
      }
      for (std::size_t j = 0; j < electrons.size(); j++) {
        if (tk.DeltaR(electrons[j]) < 0.4) overlap = true;
      }
      if (overlap) continue;
      if (tk.Pt() < 50.0) continue;
      if (fabs(tk.Eta()) > 2.1) continue;
      ntracks++;
      
      if (iso_hp[i] == 0) continue;
      if (fabs(iso_dxy[i]) > 0.02) continue;
      if (fabs(iso_dz[i] ) > 0.50) continue;
      
      double iso = iso_nhiso[i] + iso_phiso[i] - 0.5*iso_puiso[i];
      if (iso < 0.) iso = 0.;
      iso += iso_chiso[i];
      iso /= iso_pt[i];
      if (iso > 0.15) continue;
      
      if (iso_mitkhits[i] != 0) continue;
      if (iso_mmtkhits[i] != 0) continue;
      if (iso_pixhits[i] < 3) continue;
      if (iso_pixlayers[i] < 3) continue;
      if (iso_pixhits[i] != iso_trkhits[i]) continue;
      
      tracks.push_back(tk);
      tklayers.push_back(iso_trklayers[i]);
      tkhits.push_back(iso_trkhits[i]);
    }
    nxtrks = tracks.size();
    
    x1pt     = 0.0;
    x1eta    = 0.0;
    x1phi    = 0.0;
    x1hits   = 0  ;
    x1layers = 0 ;
    
    x2pt     = 0.0;
    x2eta    = 0.0;
    x2phi    = 0.0;
    x2hits   = 0  ;
    x2layers = 0 ;
    
    if (nxtrks > 0) {
      x1pt     = tracks[0].Pt();
      x1eta    = tracks[0].Eta();
      x1phi    = tracks[0].Phi();
      x1hits   = tkhits[0];
      x1layers = tklayers[0];
      x1mt     = sqrt(2.0 * x1pt * met * (1. - cos(tracks[0].DeltaPhi(metv))));
    }
    
    if (nxtrks > 1) {
      x2pt     = tracks[1].Pt();
      x2eta    = tracks[1].Eta();
      x2phi    = tracks[1].Phi();
      x2hits   = tkhits[1];
      x2layers = tklayers[1];
      x2mt     = sqrt(2.0 * x2pt * met * (1. - cos(tracks[1].DeltaPhi(metv))));
    }
    
    
    std::vector<TLorentzVector> jets;
    std::vector<double> jchf;
    std::vector<double> jnhf;
    
    jetmetdphi    = -1.0;
    jetrmetdphi   = -1.0;
    
    nbjets = 0;
    ncjets = 0;
    nfjets = 0;
    
    for (std::size_t i = 0; i < *nJet; i++) {
      TLorentzVector jv;
      jv.SetPtEtaPhiM(jet_pt[i], jet_eta[i], jet_phi[i], jet_mass[i]);
      if (jv.Pt() < 30.0) continue;
      if (fabs(jv.Eta()) > 4.7) continue;
      bool overlap = false;
      for (std::size_t j = 0; j < muons.size(); j++) {
        if (jv.DeltaR(muons[j]) < 0.4) overlap = true;
      }
      for (std::size_t j = 0; j < electrons.size(); j++) {
        if (jv.DeltaR(electrons[j]) < 0.4) overlap = true;
      }
      for (std::size_t j = 0; j < tracks.size(); j++) {
        if (jv.DeltaR(tracks[j]) < 0.4) overlap = true;
      }
      if (overlap) continue;
      jets.push_back(jv);
      jchf.push_back(jet_chf[i]);
      jnhf.push_back(jet_nhf[i]);
      if (jetmetdphi  < 0. || fabs(jv.DeltaPhi( metv)) <  jetmetdphi)  jetmetdphi = fabs(jv.DeltaPhi( metv));
      if (jetrmetdphi < 0. || fabs(jv.DeltaPhi(rmetv)) < jetrmetdphi) jetrmetdphi = fabs(jv.DeltaPhi(rmetv));
      if (jet_btag[i] > 0.4941) nbjets++;
      ncjets++;
    }
    for (std::size_t i = 0; i < *nJetFwd; i++) {
      TLorentzVector jv;
      jv.SetPtEtaPhiM(jetfwd_pt[i], jetfwd_eta[i], jetfwd_phi[i], jetfwd_mass[i]);
      if (jv.Pt() < 30.0) continue;
      if (fabs(jv.Eta()) > 4.7) continue;
      bool overlap = false;
      for (std::size_t j = 0; j < muons.size(); j++) {
        if (jv.DeltaR(muons[j]) < 0.4) overlap = true;
      }
      for (std::size_t j = 0; j < electrons.size(); j++) {
        if (jv.DeltaR(electrons[j]) < 0.4) overlap = true;
      }
      for (std::size_t j = 0; j < tracks.size(); j++) {
        if (jv.DeltaR(tracks[j]) < 0.4) overlap = true;
      }
      if (overlap) continue;
      jets.push_back(jv);
      jchf.push_back(jet_chf[i]);
      jnhf.push_back(jet_nhf[i]);
      if (jetmetdphi  < 0. || fabs(jv.DeltaPhi( metv)) <  jetmetdphi)  jetmetdphi = fabs(jv.DeltaPhi( metv));
      if (jetrmetdphi < 0. || fabs(jv.DeltaPhi(rmetv)) < jetrmetdphi) jetrmetdphi = fabs(jv.DeltaPhi(rmetv));
      ncjets++;
    }
    
    int jet1idx = -1;
    j1pt   =  0.0;
    j1eta  = -5.0;
    j1phi  = -5.0;
    j1m    = -5.0;
    j1chf  =  0.0;
    j1nhf  =  0.0;
    
    ncjets = 0;
    nfjets = 0;
    
    for (std::size_t i = 0; i < jets.size(); i++) {
      if (jets[i].Pt() > j1pt) {
        jet1idx = i;
        j1pt  = jets[i].Pt();
        j1eta = jets[i].Eta();
        j1phi = jets[i].Phi();
        j1m   = jets[i].M();
      }
    }
    j1chf = (jet1idx >= 0 ? jchf[jet1idx] : 0.);
    j1nhf = (jet1idx >= 0 ? jnhf[jet1idx] : 0.);
    
    mcweight = 1.0;
    puweight = 1.0;
    idweight = 1.0;
    trweight = 1.0;
    
    if (isMC) {
      double truepu = putrue;
      if (truepu > 99.9) truepu = 99.9;
      puweight *= puwgt->GetBinContent(puwgt->FindBin(truepu));
      
      for (std::size_t i = 0; i < muons.size(); i++) {
        double mupt  = muons[i].Pt();
        double mueta = fabs(muons[i].Eta());
        
        if (mupt > 119.9) mupt = 119.9;
        if (mupt <  20.0) mupt = 20.0;
        
        bool isTight = false;
        if (lep_tightId[midx[i]] == 1 && lep_iso[midx[i]] < 0.15) isTight = true;
        
        if (not isTight) {
          idweight *= loosemuoidhist->GetBinContent(loosemuoidhist->FindBin(mupt, mueta));
          idweight *= loosemuisohist->GetBinContent(loosemuisohist->FindBin(mupt, mueta));
        }
        else {
          idweight *= tightmuoidhist->GetBinContent(tightmuoidhist->FindBin(mupt, mueta));
          idweight *= tightmuisohist->GetBinContent(tightmuisohist->FindBin(mupt, mueta));
        }
        
      }
      double lumi   = 41.37 * 1000.;
      mcweight = lumi * (*xsec) * (*genwgt) * kfact * puweight * idweight * trweight/ (*wsum);
      
    }
    outtree->Fill();
  }
  
  file->Close();
  filePUData.Close();
  if (isMC && filePUMC != NULL) filePUMC->Close();
  
  outtree->Write();
  outfile->Close();
  
  delete outfile;
}

#endif
