fitdir=SignalInjection/CS_All1p1AndOnly2p1_MX-1800_MY-200_workspace/SignalMC_XHY4b_area/
#root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI.txt")' -b -q
#root 'load_parameters.C("'$fitdir'/higgsCombiner_0.FitDiagnostics.mH125.123456.root", "test.txt", "reallyClean")' -b -q
#./run_signal_injection.sh --fitdir $fitdir -r 0  --numtoys 2 --paras para_SI.txt -l --seed 8
#python signal_injection.py -f $fitdir/higgsCombiner_0.FitDiagnostics.mH125.42.root -r 0 --title All1p1AndOnly2p1_MX-3500_MY-200 
#python signal_injection_grid.py -f $fitdir -r 0 --title All1p1AndOnly2p1_MX-3500_MY-200_grid 
#python signal_injection_grid.py -f $fitdir -r 3 --title All1p1AndOnly2p1_MX-3500_MY-200_grid 
#./run_signal_injection.sh --fitdir $fitdir -r 3 -l --numtoys 20 --paras para_SI.txt 
#python signal_injection.py -f $fitdir/higgsCombiner_0.FitDiagnostics.mH125.123456.root -r 3 --title All1p1AndOnly2p1_MX-3500_MY-200

#fitdir=SignalInjection/CS_All2p1AndOnly1p1_MX-3000_MY-800_workspace/SignalMC_XHY4b_area/
#python signal_injection_grid.py -f $fitdir -r 0 --title All2p1AndOnly1p1_MX-3000_MY-800_grid 
#python signal_injection_grid.py -f $fitdir -r 3 --title All2p1AndOnly1p1_MX-3000_MY-800_grid 
#root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI.txt")' -b -q
#./run_signal_injection.sh --fitdir $fitdir -r 0 -l --numtoys 100 --paras para_SI.txt
#python signal_injection.py -f $fitdir/higgsCombiner_0.FitDiagnostics.mH125.123456.root -r 0 --title All2p1AndOnly1p1_MX-3000_MY-800
#./run_signal_injection.sh --fitdir $fitdir -r 3 -l --numtoys 100 --paras para_SI.txt
#python signal_injection.py -f $fitdir/higgsCombiner_0.FitDiagnostics.mH125.123456.root -r 3 --title All2p1AndOnly1p1_MX-3000_MY-800

fitdir=SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/
python plot_bias_pull.py -f $fitdir -r 0 --title All1p1AndOnly2p1_MX-3500_MY-200_grid 
exit
python plot_bias_pull.py -f $fitdir -r 1 --title All1p1AndOnly2p1_MX-3500_MY-200_grid 
fitdir=SignalInjection/CS_All1p1AndOnly2p1_MX-1800_MY-200_workspace/SignalMC_XHY4b_area/
python plot_bias_pull.py -f $fitdir -r 0 --title All1p1AndOnly2p1_MX-1800_MY-200_grid 
python plot_bias_pull.py -f $fitdir -r 1 --title All1p1AndOnly2p1_MX-1800_MY-200_grid 


fitdir=SignalInjection/CS_All2p1AndOnly1p1_MX-3500_MY-800_workspace/SignalMC_XHY4b_area/
python plot_bias_pull.py -f $fitdir -r 0 --title All2p1AndOnly1p1_MX-3500_MY-800_grid 
python plot_bias_pull.py -f $fitdir -r 1 --title All2p1AndOnly1p1_MX-3500_MY-800_grid 
fitdir=SignalInjection/CS_All2p1AndOnly1p1_MX-1800_MY-800_workspace/SignalMC_XHY4b_area/
python plot_bias_pull.py -f $fitdir -r 0 --title All2p1AndOnly1p1_MX-1800_MY-800_grid 
python plot_bias_pull.py -f $fitdir -r 1 --title All2p1AndOnly1p1_MX-1800_MY-800_grid 
