fitdir=SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/
#./run_signal_injection.sh --fitdir $fitdir -r 0 -b
#python signal_injection.py -f $fitdir/higgsCombiner_0.FitDiagnostics.mH125.123456.root -r 0 --title All1p1AndOnly2p1_MX-3500_MY-200
#./run_signal_injection.sh --fitdir $fitdir -r 3 -b
python signal_injection.py -f $fitdir/higgsCombiner_0.FitDiagnostics.mH125.123456.root -r 3 --title All1p1AndOnly2p1_MX-3500_MY-200

fitdir=SignalInjection/CS_All2p1AndOnly1p1_MX-3000_MY-800_workspace/SignalMC_XHY4b_area/
#./run_signal_injection.sh --fitdir $fitdir -r 0 -b
python signal_injection.py -f $fitdir/higgsCombiner_0.FitDiagnostics.mH125.123456.root -r 0 --title All2p1AndOnly1p1_MX-3000_MY-800
#./run_signal_injection.sh --fitdir $fitdir -r 3 -b
python signal_injection.py -f $fitdir/higgsCombiner_0.FitDiagnostics.mH125.123456.root -r 3 --title All2p1AndOnly1p1_MX-3000_MY-800
