#tfs=(0x0 1x0 0x1 "$tf" 1x2 2x1)
tf=1x1
tfs=(0x0 1x0 0x1 1x1 2x0 0x2 1x2 2x1 2x2 1x3 3x1 0x3 )
#tfs=(2x2 3x1)
#tfs=(1x0 0x1)
#tfs=(0x0)
modes="All1p1 All2p1 Only1p1 Only2p1"
modes="All2p1 Only1p1 Only2p1"
#modes="Only2p1"
#Regs="Validation Control Signal"
#modes="All2p1"
#Regs="Control"
#Regs="Signal"
Regs="Control Validation"
MX=3000
MY=300
for mode in $modes; do
    for Reg in $Regs; do
        if [[ $mode == *"2p1"* && $Reg == "Control" ]]; then
            continue
        fi
        for tf in "${tfs[@]}"; do
            base_mode="${mode: -3}"
            hist_Reg="${Reg:0:1}"R
            python plot_nuisance.py --fname parameters/"$Reg"_"$mode"_"$tf"_control_parameters_full.txt
        done
    done
done
