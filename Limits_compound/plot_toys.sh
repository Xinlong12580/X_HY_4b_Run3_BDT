toy_file=SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/higgsCombineAsimov_r_0.GenerateOnly.mH125.42.root
i=-1
while (( i < 0 )); do
    root -b -q -l 'plot_toys.C("'$toy_file'",'$i',"asimov")'
    (( i++ ))
done
