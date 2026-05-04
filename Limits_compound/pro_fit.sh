#./run_fit.sh --fitdir CV_All1p1_workspace/SignalMC_XHY4b_0x0_area/ -b
#root 'load_parameters.C("CV_All1p1_workspace/SignalMC_XHY4b_0x0_area/higgsCombineSnapshot.MultiDimFit.mH125.root")' -b -q
#./run_fit.sh --fitdir Control_All1p1_workspace/SignalMC_XHY4b_0x0_area/ -b
#root 'load_parameters.C("Control_All1p1_workspace/SignalMC_XHY4b_0x0_area/higgsCombineSnapshot.MultiDimFit.mH125.root","test.txt")' -b -q
./run_limits.sh --fitdir CS_All1p1_workspace/SignalMC_XHY4b_0x0_area/ -l
