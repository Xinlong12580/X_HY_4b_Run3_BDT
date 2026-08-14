> GOF_args.txt
i=0

while (( i < 100 )); do
    echo "CV_All1p1AndOnly2p1_workspace/SignalMC_XHY4b_area/" $i  >> GOF_args.txt
    echo "CV_All2p1AndOnly1p1_workspace/SignalMC_XHY4b_area/" $i  >> GOF_args.txt
    (( i++ ))
done
while IFS= read -r line; do
    read _Reg _mode _tf <<< "$line"
    i=0
    while (( i < 100 )); do
        echo "${_Reg:0:1}"*_"$_mode"_workspace/SignalMC_XHY4b_"$_tf"_area $i >> GOF_args.txt
        (( i++ ))
    done
done < BEST_TF.txt
