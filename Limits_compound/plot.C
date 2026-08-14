void plot()
{
   using namespace RooFit; // YVar(), Binning() calls

   TFile f("./higgsCombine_gof_toys.GoodnessOfFit.mH120.123456.root", "READ");
   TDirectoryFile *toys = f.Get<TDirectoryFile>("toys");
   RooDataSet *rds = toys->Get<RooDataSet>("toy_1");

   // set up binnings
   std::vector<double> y_bins{625,725,825,925,1025,1125,1225,1325,1425,1525};
   std::vector<double> x_bins{25,75,125,175,225,275,325,375,425,475,525,575,625,675,725,775,825};
   RooBinning rb_y(y_bins.size() - 1, y_bins.data(), "rb_y");
   RooBinning rb_x(x_bins.size() - 1, x_bins.data(), "rb_x");

   // reduce the RooDataSets
   std::unique_ptr<RooAbsData> low{rds->reduce("CMS_channel==CMS_channel::SR_pass_LOW")};
   std::unique_ptr<RooAbsData> sig{rds->reduce("CMS_channel==CMS_channel::SR_pass_SIG")};
   std::unique_ptr<RooAbsData> high{rds->reduce("CMS_channel==CMS_channel::SR_pass_HIGH")};

   // make a histogram from one as a test
   RooArgSet const &dataVars = *rds->get();
   RooRealVar &xvarLow = static_cast<RooRealVar &>(dataVars["smass_LOW_default"]);
   RooRealVar &xvarSig = static_cast<RooRealVar &>(dataVars["smass_SIG_default"]);
   RooRealVar &xvarHigh = static_cast<RooRealVar &>(dataVars["smass_HIGH_default"]);
   RooRealVar &yvar = static_cast<RooRealVar &>(dataVars["tpmass_default"]);
   TH1 *h_low = low->createHistogram("myhist_low", xvarLow, YVar(yvar, Binning(rb_y)), Binning(rb_x));
   TH1 *h_sig = sig->createHistogram("myhist_sig", xvarSig, YVar(yvar, Binning(rb_y)), Binning(rb_x));
   TH1 *h_high = high->createHistogram("myhist_high", xvarHigh, YVar(yvar, Binning(rb_y)), Binning(rb_x));

   auto c1 = new TCanvas();
   h_low->Draw("COL Z");
   h_sig->Draw("SAME COL Z");
   h_high->Draw("SAME COL Z");
   c1->SaveAs("plot.png");
}
