mode="All1p1AndOnly2p1" 
mode="All2p1AndOnly1p1" 
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
echo $tf_VR_Allmode $tf_VR_Onlymode $tf_CR_Allmode $tf_CR_Onlymode
echo $Only_mode
tf=$tf_VR_Allmode
python modify_card.py --eff_file Templates/Templates_"$All_mode"_Validation_all.root --card_file Validation_"$All_mode"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$All_mode" --fail_name VR_"$All_mode" 

tf=$tf_VR_Onlymode
python modify_card.py --eff_file Templates/Templates_"$Only_mode"_Validation_all.root --card_file Validation_"$Only_mode"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$Only_mode" --fail_name VR_"$Only_mode"

tf=$tf_CR_Allmode
python modify_card.py --eff_file Templates/Templates_"$All_mode"_Control_all.root --card_file Control_"$All_mode"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$All_mode" --fail_name CR_"$All_mode"

tf=$tf_CR_Onlymode
python modify_card.py --eff_file Templates/Templates_"$Only_mode"_Control_all.root --card_file Control_"$Only_mode"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$Only_mode" --fail_name CR_"$Only_mode" 


if [[ $All_mode == *"2p1"* ]]; then 
./combine_channels.sh CV_"$mode"_workspace/SignalMC_XHY4b_area Validation_"$All_mode"_workspace/SignalMC_XHY4b_"$tf_VR_Allmode"_area VR_"$base_All_mode" Validation_"$Only_mode"_workspace/SignalMC_XHY4b_"$tf_VR_Onlymode"_area VR_"$base_Only_mode" Control_"$Only_mode"_workspace/SignalMC_XHY4b_"$tf_CR_Onlymode"_area CR_"$base_Only_mode" 


elif [[ $Only_mode == *"2p1"* ]]; then
./combine_channels.sh CV_"$mode"_workspace/SignalMC_XHY4b_area Validation_"$All_mode"_workspace/SignalMC_XHY4b_"$tf_VR_Allmode"_area VR_"$base_All_mode" Control_"$All_mode"_workspace/SignalMC_XHY4b_"$tf_CR_Allmode"_area CR_"$base_All_mode" Validation_"$Only_mode"_workspace/SignalMC_XHY4b_"$tf_VR_Onlymode"_area VR_"$base_Only_mode" 
fi

