i=1
while (( i < 2 )); do
    ./GenerateToys.sh SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/ $i
    (( i++ ))
done
