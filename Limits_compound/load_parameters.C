void load_parameters(std::string in_file = "Control_MX-3000_MY-1000_workspace/SignalMC_XHY4b_1x1_area/higgsCombineSnapshot.MultiDimFit.mH125.root", std::string out_file = "control_parameters.txt", std::string snapshot = "MultiDimFit"){
    
	TFile *f_control = TFile::Open(in_file.c_str(), "READ");
	RooWorkspace w_control =* (RooWorkspace*) f_control->Get("w");
    w_control.loadSnapshot(snapshot.c_str());
	RooArgSet v_control = w_control.allVars();
    std::ofstream outfile(out_file.c_str());
    std::ofstream full_outfile((out_file.replace(out_file.find(".txt"), 4, "_full.txt")).c_str());
	for (auto* arg : v_control) {
    	if (auto* var = dynamic_cast<RooRealVar*>(arg)) {
        	std::cout << var->GetName() << " = " << var->getVal() << " +- " << var->getError() << std::endl;
            outfile << var->GetName() << " " << var->getVal() <<"\n";
            full_outfile << var->GetName() << " " << var->getVal() << " " << var->getError() <<"\n";
        }
	}




}
