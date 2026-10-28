> impact_args.txt
i=1
ngroup=100
while (( i <= ngroup )); do
    #echo "SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/" $ngroup $i  >> impact_args.txt
    #echo "SignalInjection/CS_All1p1AndOnly2p1_MX-1800_MY-200_workspace/SignalMC_XHY4b_area/" $ngroup $i  >> impact_args.txt
    #echo "SignalInjection/CS_All1p1AndOnly2p1_MX-1000_MY-200_workspace/SignalMC_XHY4b_area/" $ngroup $i  >> impact_args.txt
    #echo "SignalInjection/CS_All2p1AndOnly1p1_MX-3500_MY-800_workspace/SignalMC_XHY4b_area/" $ngroup $i  >> impact_args.txt
    #echo "SignalInjection/CS_All2p1AndOnly1p1_MX-1800_MY-800_workspace/SignalMC_XHY4b_area/" $ngroup $i  >> impact_args.txt
    echo "SignalInjection/withfloor_CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/" $ngroup $i  >> impact_args.txt
    echo "SignalInjection/withfloor_CS_All1p1AndOnly2p1_MX-1800_MY-200_workspace/SignalMC_XHY4b_area/" $ngroup $i  >> impact_args.txt
    echo "SignalInjection/withfloor_CS_All2p1AndOnly1p1_MX-3500_MY-800_workspace/SignalMC_XHY4b_area/" $ngroup $i  >> impact_args.txt
    echo "SignalInjection/withfloor_CS_All2p1AndOnly1p1_MX-1800_MY-800_workspace/SignalMC_XHY4b_area/" $ngroup $i  >> impact_args.txt
    (( i++ ))
done
