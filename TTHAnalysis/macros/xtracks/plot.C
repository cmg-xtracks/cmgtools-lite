//#include "makePlot.h"
#include "trimplot.h"

void plot() {
  
  int region   =    1 ;
  
  int    nbins =   20 ;
  double xmin  =  200.;
  double xmax  = 1200.;
  
  std::string plotvar = "met";
  std::string xlabel  = "E_{T}^{miss} [GeV]";
  std::string ylabel  = "Events / 50 GeV";
  
  bool isLogY  = true;
  
  std::vector<std::string> cuts;
  cuts.push_back("hltmet > 0");
  cuts.push_back("nelecs == 0");
  cuts.push_back("ntaus == 0");
  cuts.push_back("j1pt > 100 && abs(j1eta) < 2.4 && j1chf > 0.1 && j1nhf < 0.8 && jetmetdphi > 0.5");
  cuts.push_back("nbjets == 0");
  if (region == 0) {
    cuts.push_back("nmuons == 0");
  }
  if (region == 1) {
    cuts.push_back("nmuons == 1");
    cuts.push_back("abs(m1id) == 3 && m1pt > 20");
    cuts.push_back("rmet > 50 && mt < 160");
  }
  if (region == 2) {
    cuts.push_back("nmuons == 2");
    cuts.push_back("(m1id * m2id == -3 || m1id * m2id == -9) && ((abs(m1id) == 3 && m1pt > 20.) || (abs(m2id) == 3 && m2pt > 20.))");
    cuts.push_back("mass > 60 && mass < 120");
  }
  cuts.push_back("nxtrks > 0");
  
  TH1F* dat = new TH1F("dat", "dat", nbins, xmin, xmax);
  TH1F* zll = new TH1F("zll", "zll", nbins, xmin, xmax);
  TH1F* wlv = new TH1F("wlv", "wlv", nbins, xmin, xmax);
  TH1F* top = new TH1F("top", "top", nbins, xmin, xmax);
  TH1F* dib = new TH1F("dib", "dib", nbins, xmin, xmax);
  TH1F* qcd = new TH1F("qcd", "qcd", nbins, xmin, xmax);
  
  std::vector<std::string> zllfiles;
  std::vector<std::string> wlvfiles;
  std::vector<std::string> topfiles;
  std::vector<std::string> dibfiles;
  std::vector<std::string> qcdfiles;
  std::vector<std::string> datfiles;
  
  zllfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/DYJetsM50_HT100to200"    ) + "/trim.root/tree");
  zllfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/DYJetsM50_HT200to400"    ) + "/trim.root/tree");
  zllfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/DYJetsM50_HT400to600"    ) + "/trim.root/tree");
  zllfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/DYJetsM50_HT600to800"    ) + "/trim.root/tree");
  zllfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/DYJetsM50_HT800to1200"   ) + "/trim.root/tree");
  zllfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/DYJetsM50_HT1200to2500"  ) + "/trim.root/tree");
  zllfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/DYJetsM50_HT2500toInf"   ) + "/trim.root/tree");
  
  wlvfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/WJets_HT100to200"        ) + "/trim.root/tree");
  wlvfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/WJets_HT200to400"        ) + "/trim.root/tree");
  wlvfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/WJets_HT400to600"        ) + "/trim.root/tree");
  wlvfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/WJets_HT600to800"        ) + "/trim.root/tree");
  wlvfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/WJets_HT800to1200"       ) + "/trim.root/tree");
  wlvfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/WJets_HT1200to2500"      ) + "/trim.root/tree");
  wlvfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/WJets_HT2500toInf"       ) + "/trim.root/tree");
  
  qcdfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/QCD_HT100to200"          ) + "/trim.root/tree");
  qcdfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/QCD_HT200to300"          ) + "/trim.root/tree");
  qcdfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/QCD_HT300to500"          ) + "/trim.root/tree");
  qcdfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/QCD_HT500to700"          ) + "/trim.root/tree");
  qcdfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/QCD_HT700to1000"         ) + "/trim.root/tree");
  qcdfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/QCD_HT1000to1500"        ) + "/trim.root/tree");
  qcdfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/QCD_HT1500to2000"        ) + "/trim.root/tree");
  qcdfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/QCD_HT2000toInf"         ) + "/trim.root/tree");
  
  topfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/TTHad"                   ) + "/trim.root/tree");
  topfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/TTSemi"                  ) + "/trim.root/tree");
  topfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/TTLep"                   ) + "/trim.root/tree");
  topfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/T_tWch"                  ) + "/trim.root/tree");
  topfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/T_tch"                   ) + "/trim.root/tree");
  topfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/TBar_tWch"               ) + "/trim.root/tree");
  topfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/TBar_tch"                ) + "/trim.root/tree");
  
  dibfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/WW"                      ) + "/trim.root/tree");
  dibfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/WZ"                      ) + "/trim.root/tree");
  dibfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_MC/ZZ"                      ) + "/trim.root/tree");
  
  datfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_DATA/MET_Run2017B_31Mar2018") + "/trim.root/tree");
  datfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_DATA/MET_Run2017C_31Mar2018") + "/trim.root/tree");
  datfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_DATA/MET_Run2017D_31Mar2018") + "/trim.root/tree");
  datfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_DATA/MET_Run2017E_31Mar2018") + "/trim.root/tree");
  datfiles.push_back(std::string("/media/Disk1/avartak/CMS/Data/XTracks/SR_DATA/MET_Run2017F_31Mar2018") + "/trim.root/tree");
  
  trimplot(zllfiles, zll, plotvar, cuts);
  trimplot(wlvfiles, wlv, plotvar, cuts);
  trimplot(topfiles, top, plotvar, cuts);
  trimplot(dibfiles, dib, plotvar, cuts);
  trimplot(qcdfiles, qcd, plotvar, cuts);
  trimplot(datfiles, dat, plotvar, cuts);
  
  zll->SetFillColor(kCyan-9);
  wlv->SetFillColor(kRed-10);
  top->SetFillColor(kYellow);
  dib->SetFillColor(kGreen+1);
  
  THStack* stk = new THStack("stk", "");
  stk->Add(qcd);
  stk->Add(dib);
  stk->Add(top);
  if (region == 1) {        
    stk->Add(zll);
    stk->Add(wlv);
  }
  if (region == 2) {        
    stk->Add(wlv);
    stk->Add(zll);
  }
  
  double ymin = stk->GetMinimum();
  double ymax = stk->GetMaximum();
  
  if (ymin > dat->GetMinimum()) ymin = dat->GetMinimum();
  if (ymax < dat->GetMaximum()) ymax = dat->GetMaximum();
  
  ymax *= 1.2;
  ymin *= 0.5;
  if (ymin == 0. && ymax > 1.) ymin = 0.0001;
  
  std::cout << ymin << " " << ymax << std::endl;
  
  TH1* frame = gPad->DrawFrame(xmin, ymin, xmax, ymax, "");
  frame->GetXaxis()->SetTitle(xlabel.c_str());
  gPad->SetRightMargin(0.075);
  gPad->SetTopMargin(0.06);
  frame->GetYaxis()->SetLabelSize(0.7*frame->GetYaxis()->GetLabelSize());
  frame->GetXaxis()->SetLabelSize(0.7*frame->GetXaxis()->GetLabelSize());
  frame->GetYaxis()->SetTitle(ylabel.c_str());
  
  frame->Draw();
  stk->Draw("HIST SAME");
  dat->Draw("PE   SAME");
  
  TLegend* leg = new TLegend(0.5, 0.7, 0.9, 0.9);
  leg->SetFillColor(0);
  leg->AddEntry(dat, "Data");
  if (region == 1) {        
    leg->AddEntry(wlv, "W+jets"     , "F");
    leg->AddEntry(zll, "Z+jets"     , "F");
  }
  if (region == 2) {        
    leg->AddEntry(zll, "Z(#mu#mu)"  , "F");
    leg->AddEntry(wlv, "W+jets"     , "F");
  }
  leg->AddEntry(top, "Top"        , "F");
  leg->AddEntry(dib, "Dibosons"   , "F");
  leg->AddEntry(qcd, "QCD"        , "F");
  
  leg->Draw("SAME");
  
  if (isLogY) gPad->SetLogy();
  gPad->RedrawAxis();
}