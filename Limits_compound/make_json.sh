#make json files 
mode=$1
Reg=$2
if [[ X$mode == X ]]; then
    echo "Must specify mode (1p1 or 2p1)" >&2
    exit 1
fi
if [[ $Reg == *"Signal"* ]]; then
    r_pass=SR_SR1_"${mode: -3}"    
    r_fail=SR_SB1_"${mode: -3}"    
elif [[ $Reg == *"Control"* ]]; then
    r_pass=CR_SR1_"${mode: -3}"    
    r_fail=CR_SB1_"${mode: -3}"    
elif [[ $Reg == *"Validation"* ]]; then
    r_pass=VR_SR1_"${mode: -3}"    
    r_fail=VR_SB1_"${mode: -3}"    
fi
if [[ $mode == *"1p1"* ]]; then
    basemode=1p1
    sed -e "s/R_PASS/$r_pass/g" -e "s/R_FAIL/$r_fail/g" -e "s/BASEMODE/$basemode/g" -e "s/MODE/$mode/g" -e "s/MREG/$Reg/g" -e "s/MBINS/B_$basemode/g"  XYH_1p1.json > XYH_"$r_pass"_"$r_fail".json
elif [[ $mode == *"2p1"* ]]; then
    basemode=2p1
    sed -e "s/R_PASS/$r_pass/g" -e "s/R_FAIL/$r_fail/g" -e "s/BASEMODE/$basemode/g" -e "s/MODE/$mode/g" -e "s/MREG/$Reg/g" -e "s/MBINS/B_$basemode/g" XYH_2p1.json > XYH_"$r_pass"_"$r_fail".json
fi
