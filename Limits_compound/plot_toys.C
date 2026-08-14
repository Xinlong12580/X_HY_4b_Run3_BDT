void plot_toys()
{
   using namespace RooFit; // YVar(), Binning() calls

   TFile f("SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/higgsCombiner_0.GenerateOnly.mH125.1.root", "READ");
   TDirectoryFile *toys = f.Get<TDirectoryFile>("toys");
   RooDataSet *rds = toys->Get<RooDataSet>("toy_8");

   // set up binnings
   std::vector<double> x_bins_1p1{0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.3, 0.4, 0.5, 1.0};
   std::vector<double> y_bins_1p1{0.8, 0.9, 1.0,  1.2, 1.4, 1.7, 2.0, 2.5, 3.0, 5.0 };
   std::vector<double> x_bins_2p1{0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0};
   std::vector<double> y_bins_2p1{0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.7, 2.0, 2.5, 3.0, 4.0, 5.0 };

   RooBinning rb_y_1p1(y_bins_1p1.size() - 1, y_bins_1p1.data(), "rb_y");
   RooBinning rb_x_1p1(x_bins_1p1.size() - 1, x_bins_1p1.data(), "rb_x");
   RooBinning rb_y_2p1(y_bins_2p1.size() - 1, y_bins_2p1.data(), "rb_y");
   RooBinning rb_x_2p1(x_bins_2p1.size() - 1, x_bins_2p1.data(), "rb_x");

   // reduce the RooDataSets
   std::unique_ptr<RooAbsData> CR_SR1_1p1{rds->reduce("CMS_channel==CMS_channel::_CR_SR1_1p1_Region0")};
   std::unique_ptr<RooAbsData> CR_SB1_1p1{rds->reduce("CMS_channel==CMS_channel::_CR_SB1_1p1_Region0")};
   std::unique_ptr<RooAbsData> SR_SR1_1p1{rds->reduce("CMS_channel==CMS_channel::_SR_SR1_1p1_Region0")};
   std::unique_ptr<RooAbsData> SR_SB1_1p1{rds->reduce("CMS_channel==CMS_channel::_SR_SB1_1p1_Region0")};
   std::unique_ptr<RooAbsData> SR_SR1_2p1{rds->reduce("CMS_channel==CMS_channel::_SR_SR1_2p1_Region0")};
   std::unique_ptr<RooAbsData> SR_SB1_2p1{rds->reduce("CMS_channel==CMS_channel::_SR_SB1_2p1_Region0")};

   // make a histogram from one as a test
   RooArgSet const &dataVars = *rds->get();
   RooRealVar &xvar_1p1 = static_cast<RooRealVar &>(dataVars["M_JY_Region0_B_1p1"]);
   RooRealVar &yvar_1p1 = static_cast<RooRealVar &>(dataVars["M_JJ_B_1p1"]);
   RooRealVar &xvar_2p1 = static_cast<RooRealVar &>(dataVars["M_JY_Region0_B_2p1"]);
   RooRealVar &yvar_2p1 = static_cast<RooRealVar &>(dataVars["M_JJ_B_2p1"]);

   TH2 *h_CR_SR1_1p1 = dynamic_cast<TH2*> (CR_SR1_1p1->createHistogram("CR_SR1_1p1", xvar_1p1, YVar(yvar_1p1, Binning(rb_y_1p1)), Binning(rb_x_1p1)));
   TH2 *h_CR_SB1_1p1 = dynamic_cast<TH2*> (CR_SB1_1p1->createHistogram("CR_SB1_1p1", xvar_1p1, YVar(yvar_1p1, Binning(rb_y_1p1)), Binning(rb_x_1p1)));
   TH2 *h_SR_SR1_1p1 =dynamic_cast<TH2*> (SR_SR1_1p1->createHistogram("SR_SR1_1p1", xvar_1p1, YVar(yvar_1p1, Binning(rb_y_1p1)), Binning(rb_x_1p1)));
   TH2 *h_SR_SB1_1p1 = dynamic_cast<TH2*> (SR_SB1_1p1->createHistogram("SR_SB1_1p1", xvar_1p1, YVar(yvar_1p1, Binning(rb_y_1p1)), Binning(rb_x_1p1)));
   TH2 *h_SR_SR1_2p1 = dynamic_cast<TH2*> (SR_SR1_2p1->createHistogram("SR_SR1_2p1", xvar_2p1, YVar(yvar_2p1, Binning(rb_y_2p1)), Binning(rb_x_2p1)));
   TH2 *h_SR_SB1_2p1 = dynamic_cast<TH2*> (SR_SB1_2p1->createHistogram("SR_SB1_2p1", xvar_2p1, YVar(yvar_2p1, Binning(rb_y_2p1)), Binning(rb_x_2p1)) );

   auto c_CR_SR1_1p1  = new TCanvas();
   h_CR_SR1_1p1 ->Draw("COL Z");
   c_CR_SR1_1p1 ->SaveAs("TOYS/CR_SR1_1p1.png");
   auto c_CR_SR1_1p1_x  = new TCanvas();
   h_CR_SR1_1p1->ProjectionX("CR_SR1_1p1x") ->Draw("HIST");
   c_CR_SR1_1p1_x ->SaveAs("TOYS/CR_SR1_1p1x.png");
   auto c_CR_SR1_1p1_y  = new TCanvas();
   h_CR_SR1_1p1->ProjectionY("CR_SR1_1p1y") ->Draw("HIST");
   c_CR_SR1_1p1_y ->SaveAs("TOYS/CR_SR1_1p1y.png");

   auto c_CR_SB1_1p1  = new TCanvas();
   h_CR_SB1_1p1 ->Draw("COL Z");
   c_CR_SB1_1p1 ->SaveAs("TOYS/CR_SB1_1p1.png");
   auto c_CR_SB1_1p1_x  = new TCanvas();
   h_CR_SB1_1p1->ProjectionX("CR_SB1_1p1x") ->Draw("HIST");
   c_CR_SB1_1p1_x ->SaveAs("TOYS/CR_SB1_1p1x.png");
   auto c_CR_SB1_1p1_y  = new TCanvas();
   h_CR_SB1_1p1->ProjectionY("CR_SB1_1p1y") ->Draw("HIST");
   c_CR_SB1_1p1_y ->SaveAs("TOYS/CR_SB1_1p1y.png");


   auto c_SR_SR1_1p1  = new TCanvas();
   h_SR_SR1_1p1 ->Draw("COL Z");
   c_SR_SR1_1p1 ->SaveAs("TOYS/SR_SR1_1p1.png");
   auto c_SR_SR1_1p1_x  = new TCanvas();
   h_SR_SR1_1p1->ProjectionX("SR_SR1_1p1x") ->Draw("HIST");
   c_SR_SR1_1p1_x ->SaveAs("TOYS/SR_SR1_1p1x.png");
   auto c_SR_SR1_1p1_y  = new TCanvas();
   h_SR_SR1_1p1->ProjectionY("SR_SR1_1p1y") ->Draw("HIST");
   c_SR_SR1_1p1_y ->SaveAs("TOYS/SR_SR1_1p1y.png");

   auto c_SR_SB1_1p1  = new TCanvas();
   h_SR_SB1_1p1 ->Draw("COL Z");
   c_SR_SB1_1p1 ->SaveAs("TOYS/SR_SB1_1p1.png");
   auto c_SR_SB1_1p1_x  = new TCanvas();
   h_SR_SB1_1p1->ProjectionX("SR_SB1_1p1x") ->Draw("HIST");
   c_SR_SB1_1p1_x ->SaveAs("TOYS/SR_SB1_1p1x.png");
   auto c_SR_SB1_1p1_y  = new TCanvas();
   h_SR_SB1_1p1->ProjectionY("SR_SB1_1p1y") ->Draw("HIST");
   c_SR_SB1_1p1_y ->SaveAs("TOYS/SR_SB1_1p1y.png");
   
   auto c_SR_SR1_2p1  = new TCanvas();
   h_SR_SR1_2p1 ->Draw("COL Z");
   c_SR_SR1_2p1 ->SaveAs("TOYS/SR_SR1_2p1.png");
   auto c_SR_SR1_2p1_x  = new TCanvas();
   h_SR_SR1_2p1->ProjectionX("SR_SR1_2p1x") ->Draw("HIST");
   c_SR_SR1_2p1_x ->SaveAs("TOYS/SR_SR1_2p1x.png");
   auto c_SR_SR1_2p1_y  = new TCanvas();
   h_SR_SR1_2p1->ProjectionY("SR_SR1_2p1y") ->Draw("HIST");
   c_SR_SR1_2p1_y ->SaveAs("TOYS/SR_SR1_2p1y.png");

   auto c_SR_SB1_2p1  = new TCanvas();
   h_SR_SB1_2p1 ->Draw("COL Z");
   c_SR_SB1_2p1 ->SaveAs("TOYS/SR_SB1_2p1.png");
   auto c_SR_SB1_2p1_x  = new TCanvas();
   h_SR_SB1_2p1->ProjectionX("SR_SB1_2p1x") ->Draw("HIST");
   c_SR_SB1_2p1_x ->SaveAs("TOYS/SR_SB1_2p1x.png");
   auto c_SR_SB1_2p1_y  = new TCanvas();
   h_SR_SB1_2p1->ProjectionY("SR_SB1_2p1y") ->Draw("HIST");
   c_SR_SB1_2p1_y ->SaveAs("TOYS/SR_SB1_2p1y.png");
   


}
