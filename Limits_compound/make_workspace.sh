#tfs=(0x0 1x0 0x1 "$tf" 1x2 2x1)
tf=0x0
MX=3000
MY=300
modes="All1p1 All2p1 Only1p1 Only2p1"
modes="All2p1 Only2p1"
#modes="Only2p1"
#Regs="Validation Control Signal"
Regs="Validation Control"
#Regs="Control Validation"
#Regs="Validation"
#Regs="Validation Control"
#Regs="Signal"
#modes="All2p1 All1p1"
#Regs="Control"
for mode in $modes; do
    for Reg in $Regs; do
        if [[  $Reg == "Control" && $mode == *"2p1"* ]]; then
            continue
        fi
        echo $mode $Reg 
        base_mode="${mode: -3}"
        hist_Reg="${Reg:0:1}"R
        ./make_json.sh "$mode" $Reg
        python XYH.py --mode "$base_mode" --tf $tf --sig $MX-$MY --r_fail "$hist_Reg"_SB1_$base_mode --r_pass "$hist_Reg"_SR1_$base_mode --make  --wsp "$Reg"_"$mode"
        #root_files=$(ls "$Reg"_"$mode"_workspace) 
        #if [[ $root_files != *"base_clean.root"* ]]; then
        #    echo TEST
        #    cp "$Reg"_"$mode"_workspace/base.root "$Reg"_"$mode"_workspace/base_clean.root
        #fi
        #cp "$Reg"_"$mode"_workspace/base_clean.root "$Reg"_"$mode"_workspace/base.root
        #python inject_MCstats_templates.py --input_file Templates/Templates_"$mode"_"$Reg"_all_MCstat.root  --target_file "$Reg"_"$mode"_workspace/base.root 
        #python XYH.py --mode "$base_mode" --tf $tf --sig $MX-$MY --r_fail "$hist_Reg"_SB1_$base_mode --r_pass "$hist_Reg"_SR1_$base_mode --makeCard --wsp "$Reg"_"$mode"
        #python modify_card.py --eff_file Templates/Templates_"$mode"_"$Reg"_all.root --card_file "$Reg"_"$mode"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$mode" --fail_name "$hist_Reg"_"$mode"
    done
done
