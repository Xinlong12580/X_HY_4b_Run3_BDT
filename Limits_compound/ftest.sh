#tfs=(0x0 1x0 0x1 "$tf" 1x2 2x1)
tf=1x1
tfs=(0x0 1x0 0x1 1x1 2x0 0x2)
modes="All1p1 All2p1 Only1p1 Only2p1"
Regs="Validation Control Signal"
modes="Only2p1"
Regs="Control"
#Regs="Control"
MX=3000
MY=300
for mode in $modes; do
    for Reg in $Regs; do
        for tf in "${tfs[@]}"; do
            base_mode="${mode: -3}"
            hist_Reg="${Reg:0:1}"R
            python XYH.py --mode "$base_mode" --tf $tf --sig $MX-$MY --r_fail "$hist_Reg"_SB1_$base_mode --r_pass "$hist_Reg"_SR1_$base_mode --makeCard --wsp "$Reg"_"$mode"
            python clean_card.py --eff_file Templates/Templates_"$mode"_"$Reg"_all.root --card_file "$Reg"_"$mode"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$mode" --fail_name "$hist_Reg"_"$mode"
            if [[ $Reg == "Control" ]]; then
                python modify_card.py --eff_file Templates/Templates_"$mode"_"$Reg"_all.root --card_file "$Reg"_"$mode"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$mode" --fail_name "$hist_Reg"_"$mode"
            fi
            ./run_fit.sh  --fitdir "$Reg"_"$mode"_workspace/SignalMC_XHY4b_"$tf"_area -b -v 3
            root 'load_parameters.C("'"$Reg"_"$mode"'_workspace/SignalMC_XHY4b_'$tf'_area/higgsCombineSnapshot.MultiDimFit.mH125.root", "parameters/'"$Reg"_"$mode"_$tf'_control_parameters.txt")' -b -q
            ./plot_postfit.sh "$Reg"_"$mode"_workspace/SignalMC_XHY4b_"$tf"_area $tf "$hist_Reg"_SR1_$base_mode "$hist_Reg"_SB1_$base_mode $mode
            ./run_GoF.sh  --fitdir "$Reg"_"$mode"_workspace/SignalMC_XHY4b_"$tf"_area -b -v 3
            
        done
        
        python ftest.py --tf1 0x0 --tf2 1x0 --work_dir "$Reg"_"$mode"_workspace/ --extra "$Reg"_$mode
        python ftest.py --tf1 0x0 --tf2 0x1 --work_dir "$Reg"_"$mode"_workspace/ --extra "$Reg"_$mode 
        python ftest.py --tf1 1x0 --tf2 1x1 --work_dir "$Reg"_"$mode"_workspace/ --extra "$Reg"_$mode
        python ftest.py --tf1 1x0 --tf2 2x0 --work_dir "$Reg"_"$mode"_workspace/ --extra "$Reg"_$mode
        python ftest.py --tf1 0x1 --tf2 1x1 --work_dir "$Reg"_"$mode"_workspace/ --extra "$Reg"_$mode 
        python ftest.py --tf1 0x1 --tf2 0x2 --work_dir "$Reg"_"$mode"_workspace/ --extra "$Reg"_$mode 
    done
done
