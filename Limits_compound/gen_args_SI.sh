> SI_args.txt
i=1
while (( i < 90 )); do
    echo "SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/" $i  >> SI_args.txt
    echo "SignalInjection/CS_All1p1AndOnly2p1_MX-1800_MY-200_workspace/SignalMC_XHY4b_area/" $i  >> SI_args.txt
    echo "SignalInjection/CS_All2p1AndOnly1p1_MX-3500_MY-800_workspace/SignalMC_XHY4b_area/" $i  >> SI_args.txt
    echo "SignalInjection/CS_All2p1AndOnly1p1_MX-1800_MY-800_workspace/SignalMC_XHY4b_area/" $i  >> SI_args.txt
    (( i++ ))
done
