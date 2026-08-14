fitdir=SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/

root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI_impact.txt")' -b -q
./run_impact.sh --fitdir $fitdir -r 3 -l --paras para_SI_impact.txt 

fitdir=SignalInjection/CS_All2p1AndOnly1p1_MX-3000_MY-800_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI_impact.txt")' -b -q
./run_impact.sh --fitdir $fitdir -r 3 -l --paras para_SI_impact.txt 
