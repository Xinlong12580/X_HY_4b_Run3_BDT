mode=All1p1AndOnly2p1
mode=All2p1AndOnly1p1
base_All_mode=${mode#*All}     
base_All_mode=${base_All_mode%%AndOnly*}
base_Only_mode=${mode#*Only}
All_mode=All$base_All_mode
Only_mode=Only$base_Only_mode
while IFS= read -r line; do
    read _Reg _mode _tf <<< "$line"
    echo $_Reg $_mode $_tf $All_mode
    if [[ $_Reg == "CR" && $_mode == $All_mode ]]; then
        tf_CR_Allmode=$_tf
    fi
    if [[ $_Reg == "CR" && $_mode == $Only_mode ]]; then
        tf_CR_Onlymode=$_tf
    fi
    if [[ $_Reg == "VR" && $_mode == $All_mode ]]; then
        tf_VR_Allmode=$_tf
    fi
    if [[ $_Reg == "VR" && $_mode == $Only_mode ]]; then
        tf_VR_Onlymode=$_tf
    fi
done < BEST_TF.txt

workdir=CV_"$mode"_workspace/SignalMC_XHY4b_area/
#./run_fit.sh --fitdir $workdir -b
#root 'load_parameters.C("'$workdir'/higgsCombineSnapshot.MultiDimFit.mH125.root", "parameters/'"$mode"'_control_parameters.txt")' -b -q
#./plot_postfit_combined.sh $workdir $tf_CR_Allmode _CR_SR1_$base_All_mode _CR_SB1_$base_All_mode $mode 1
#./plot_postfit_combined.sh $workdir $tf_CR_Onlymode _CR_SR1_$base_Only_mode _CR_SB1_$base_Only_mode $mode 0
#./plot_postfit_combined.sh $workdir $tf_VR_Allmode _VR_SR1_$base_All_mode _VR_SB1_$base_All_mode $mode 0
#./plot_postfit_combined.sh $workdir $tf_VR_Onlymode _VR_SR1_$base_Only_mode _VR_SB1_$base_Only_mode $mode 0
#python plot_nuisance.py --fname parameters/"$mode"_control_parameters_full.txt 
#python plot_correlation_matrix.py -f CV_"$mode"_workspace/SignalMC_XHY4b_area/multidimfitSnapshot.root --title "$mode"
#./run_GoF.sh --fitdir CV_"$mode"_workspace/SignalMC_XHY4b_area -b --ntoys 100
python gof.py --fitdir CV_"$mode"_workspace/SignalMC_XHY4b_area/ --title "$mode"
