#include <vector>
#include <utility>

void addTemplate(string procname, RooArgList& varlist, RooWorkspace& ws, TH1F* hist) {
  RooDataHist rhist(procname.c_str(), "", varlist, hist);
  ws.import(rhist);
}

void makeBinList(string procname, RooRealVar& var, RooWorkspace& ws, TH1F* hist, RooArgList& binlist, bool setConst = false) {
  for (int i = 1; i <= hist->GetNbinsX(); i++) {
    stringstream binss;
    binss << procname << "_bin" << i;
    RooRealVar* binvar;
    if (!setConst) binvar = new RooRealVar(binss.str().c_str(), "", hist->GetBinContent(i), 0., hist->GetBinContent(i)*2.0);
    else           binvar = new RooRealVar(binss.str().c_str(), "", hist->GetBinContent(i));
    if (setConst)  binvar->setConstant(kTRUE);
    binlist.add(*binvar);
  }
  
  stringstream normss;
  normss << procname << "_norm";
  
  RooParametricHist phist(procname.c_str(), "", var, binlist, *hist);
  RooAddition norm(normss.str().c_str(), "", binlist);
  
  ws.import(phist,RooFit::RecycleConflictNodes());
  ws.import(norm, RooFit::RecycleConflictNodes());
  
}

void makeConnectedBinList(string procname, RooRealVar& var, RooWorkspace& ws, TH1F* rhist, vector<pair<RooRealVar*, TH1*> > syst, const RooArgList& srbinlist, RooArgList* crbinlist=NULL) {
  if (crbinlist == NULL) crbinlist = new RooArgList();
  
  for (int i = 1; i <= rhist->GetNbinsX(); i++) {
    stringstream rbinss;
    rbinss << "r_" << procname << "_bin" << i;
    RooRealVar* rbinvar = new RooRealVar(rbinss.str().c_str(), "", rhist->GetBinContent(i));
    
    stringstream rerrbinss;
    rerrbinss << procname << "_bin" << i << "_Runc";
    RooRealVar* rerrbinvar = new RooRealVar(rerrbinss.str().c_str(), "", 0., -5., 5.);
    
    stringstream binss;
    binss << procname << "_bin" << i;
    
    RooArgList fobinlist;
    fobinlist.add(srbinlist[i-1]);
    fobinlist.add(*rbinvar);
    fobinlist.add(*rerrbinvar);
    
    stringstream formss;
    formss << "@0/";
    formss << "(";
    formss << "@1";
    formss << "*(1+" << rhist->GetBinError(i)/rhist->GetBinContent(i) << "*@2)";
    for (int j = 0; j < syst.size(); j++) {
      stringstream systbinss;
      if (syst[j].first == NULL) {
        systbinss << procname << "_bin" << i << "_" << syst[j].second->GetName();
        RooRealVar* systbinvar = new RooRealVar(systbinss.str().c_str(), "", 0., -5., 5.);
        fobinlist.add(*systbinvar);
      }
      else {
        fobinlist.add(*syst[j].first);
      }
      formss << "*(1+" << syst[j].second->GetBinContent(i) << "*@" << j+3 << ")";
    }
    formss << ")";
    
    RooFormulaVar* binvar = new RooFormulaVar(binss.str().c_str(), "", formss.str().c_str(), RooArgList(fobinlist));
    crbinlist->add(*binvar);
  }
  
  stringstream normss;
  normss << procname << "_norm";
  
  RooParametricHist phist(procname.c_str(), "", var, *crbinlist, *rhist);
  RooAddition norm(normss.str().c_str(),"", *crbinlist);
  
  ws.import(phist,RooFit::RecycleConflictNodes());
  ws.import(norm, RooFit::RecycleConflictNodes());
}

void createWorkspace(std::map<std::string, TH1*> templates) {
  gSystem->Load("libHiggsAnalysisCombinedLimit.so");
  
  TFile *outfile = new TFile("workspace.root","RECREATE");
  RooWorkspace wspace("w","w");
  
  RooRealVar met("met","E_{T}^{miss}",200,1000);
  RooArgList vars(met);
  
  // ---------------------------- SIGNAL REGION -------------------------------------------------------------------//
  // Data
  addTemplate("data_obs_SR", vars, wspace, templates["data_SR"];
  
  // Signal shape
  addTemplate("DM_SR", vars, wspace, templates["Signal"]);
  
  // Znunu background
  TH1F* znn_SR_hist = templates["Zvv_SR"];
  RooArgList znn_SR_bins;
  makeBinList("Znunu_SR", met, wspace, znn_SR_hist, znn_SR_bins);
  
  // WJets background
  TH1F* wln_SR_hist = templates["Wlv_SR"];
  RooArgList wln_SR_bins;
  makeBinList("WJets_SR", met, wspace, wln_SR_hist, wln_SR_bins);
  
  // Other MC backgrounds
  addTemplate("ZJets_SR"     , vars, wspace, templates["Zll_SR"]);
  addTemplate("Top_SR"       , vars, wspace, templates["Top_SR"]);
  addTemplate("QCD_SR"       , vars, wspace, templates["QCD_SR"]);
  addTemplate("Dibosons_SR"  , vars, wspace, templates["VV_SR"]);
  
  // ---------------------------- CONTROL REGION (Dimuon) -----------------------------------------------------------------//
  addTemplate("data_obs_ZM", vars, wspace, templates["data_DM"]);
  vector<pair<RooRealVar*, TH1*> >   znn_ZM_syst;
  makeConnectedBinList("Znunu_ZM", met, wspace, templates["Zmm_TF"], znn_ZM_syst, znn_SR_bins);
  
  // Other MC backgrounds in dimuon control region
  addTemplate("WJets_ZM"     , vars, wspace, templates["Wlv_DM"]);
  addTemplate("Top_ZM"       , vars, wspace, templates["Top_DM"]);
  addTemplate("QCD_ZM"       , vars, wspace, templates["QCD_DM"]);
  addTemplate("Dibosons_ZM"  , vars, wspace, templates["VV_DM"]);
  
  // ---------------------------- CONTROL REGION (Dielectron) -----------------------------------------------------------------//
  addTemplate("data_obs_ZE"  , vars, wspace, templates["data_DE"]);
  vector<pair<RooRealVar*, TH1*> > znn_ZE_syst;
  makeConnectedBinList("Znunu_ZE", met, wspace, templates["Zee_TF"], znn_ZE_syst, znn_SR_bins);
  
  // Other MC backgrounds in dielectron control region
  addTemplate("WJets_ZE"     , vars, wspace, templates["Wlv_DE"]);
  addTemplate("Top_ZE"       , vars, wspace, templates["Top_DE"]);
  addTemplate("QCD_ZE"       , vars, wspace, templates["QCD_DE"]);
  addTemplate("Dibosons_ZE"  , vars, wspace, templates["VV_DE"]);
  
  // ---------------------------- CONTROL REGION (Single muon) -----------------------------------------------------------------//
  addTemplate("data_obs_WM"  , vars, wspace, templates["data_SM"]);
  vector<pair<RooRealVar*, TH1*> > wln_WM_syst;
  makeConnectedBinList("WJets_WM", met, wspace, templates["Wmv_TF"], wln_WM_syst, wln_SR_bins);
  
  // Other MC backgrounds in single muon control region
  addTemplate("ZJets_WM"     , vars, wspace, templates["Zll_SM"]);
  addTemplate("Top_WM"       , vars, wspace, templates["Top_SM"]);
  addTemplate("QCD_WM"       , vars, wspace, templates["QCD_SM"]);
  addTemplate("Dibosons_WM"  , vars, wspace, templates["VV_SM"]);
  
  // ---------------------------- CONTROL REGION (Single electron) -----------------------------------------------------------------//
  addTemplate("data_obs_WE"  , vars, wspace, templates["data_SE"]);
  vector<pair<RooRealVar*, TH1*> > wln_WE_syst;
  makeConnectedBinList("WJets_WE", met, wspace, templates["Wev_TF"], wln_WE_syst, wln_SR_bins);
  
  // Other MC backgrounds in single electron control region
  addTemplate("ZJets_WE"     , vars, wspace, templates["Zll_SE"]);
  addTemplate("Top_WE"       , vars, wspace, templates["Top_SE"]);
  addTemplate("QCD_WE"       , vars, wspace, templates["QCD_SE"]);
  addTemplate("Dibosons_WE"  , vars, wspace, templates["VV_SE"]);
  
  // ---------------------------- Write out the workspace -----------------------------------------------------------------//
  outfile->cd();
  wspace.Write();
  outfile->Close();
  
}


void createWorkspace(std::string filename = "templates.root") {
  
  std::map<std::string, TH1*> templates;
  TFile file(filename.c_str());
  
  templates["data_SR"] = (TH1*)file.Get("data_SR");
  templates["data_SM"] = (TH1*)file.Get("data_SM");
  templates["data_DM"] = (TH1*)file.Get("data_DM");
  templates["data_SE"] = (TH1*)file.Get("data_SE");
  templates["data_DE"] = (TH1*)file.Get("data_DE");
  
  templates["Zvv_SR"]  = (TH1*)file.Get("Zvv_SR");
  templates["Wlv_SR"]  = (TH1*)file.Get("Wlv_SR");
  templates["Zll_SR"]  = (TH1*)file.Get("Zll_SR");
  templates["Top_SR"]  = (TH1*)file.Get("Top_SR");
  templates["QCD_SR"]  = (TH1*)file.Get("QCD_SR");
  templates["VV_SR"]   = (TH1*)file.Get("VV_SR");
  
  templates["Zll_SM"]  = (TH1*)file.Get("Zll_SM");
  templates["Top_SM"]  = (TH1*)file.Get("Top_SM");
  templates["QCD_SM"]  = (TH1*)file.Get("QCD_SM");
  templates["VV_SM"]   = (TH1*)file.Get("VV_SM");
  
  templates["Zll_SE"]  = (TH1*)file.Get("Zll_SE");
  templates["Top_SE"]  = (TH1*)file.Get("Top_SE");
  templates["QCD_SE"]  = (TH1*)file.Get("QCD_SE");
  templates["VV_SE"]   = (TH1*)file.Get("VV_SE");
  
  templates["Wlv_DM"]  = (TH1*)file.Get("Wlv_DM");
  templates["Top_DM"]  = (TH1*)file.Get("Top_DM");
  templates["QCD_DM"]  = (TH1*)file.Get("QCD_DM");
  templates["VV_DM"]   = (TH1*)file.Get("VV_DM");
  
  templates["Wlv_DE"]  = (TH1*)file.Get("Wlv_DE");
  templates["Top_DE"]  = (TH1*)file.Get("Top_DE");
  templates["QCD_DE"]  = (TH1*)file.Get("QCD_DE");
  templates["VV_DE"]   = (TH1*)file.Get("VV_DE");
  
  templates["Zmm_TF"] = (TH1*)file.Get("Zmm_TF");
  templates["Zee_TF"] = (TH1*)file.Get("Zee_TF");
  templates["Wmv_TF"] = (TH1*)file.Get("Wmv_TF");
  templates["Wev_TF"] = (TH1*)file.Get("Wev_TF");
  
  templates["Signal"]  = (TH1*)file.Get("Signal");
  
  createWorkspace(templates);
}
