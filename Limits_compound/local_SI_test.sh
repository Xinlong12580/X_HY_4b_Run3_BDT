fitdir=SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/
SEED=58
root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI.txt")' -b -q
#./GenerateToys_100x.sh $fitdir $SEED
#./run_signal_injection.sh --fitdir $fitdir -r 0  --numtoys 10 --paras para_SI.txt -l --seed $SEED 
#./run_signal_injection_100x.sh --fitdir $fitdir -r 0  --numtoys 10 --paras para_SI.txt -l --seed $SEED 
#./run_plot_grid_r_100x.sh 
./run_plot_grid_r.sh 
