#ifndef TRIMPLOT_H
#define TRIMPLOT_H

void trimplot(std::vector<std::string> trees, TH1F* hist, std::string plotvar, std::vector<std::string> cuts) {
  
  TChain* chain = new TChain("chain");
  
  std::cout << "Analyzing samples : " << std::endl;
  for (std::size_t i = 0; i < trees.size(); i++) {
    std::cout << trees[i] << std::endl;
    chain->Add(trees[i].c_str());
  }
  std::cout << std::endl;
  
  std::string cutstr = "";
  if (cuts.size() == 0) cutstr  = "";
  if (cuts.size() == 1) cutstr += cuts[0];
  if (cuts.size() >  1) {
    for (std::size_t i = 0; i < cuts.size()-1; i++) cutstr += "(" + cuts[i] + ") && ";
    cutstr += "(" + cuts[cuts.size()-1] + ")";
  }
  cutstr = std::string("mcweight*puweight*idweight*trweight*(") + cutstr + ")";            
  
  std::string drawstr = plotvar + ">>" + hist->GetName();
  chain->Draw(drawstr.c_str(), cutstr.c_str());
  
  delete chain;
}

#endif
