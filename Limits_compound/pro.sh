MX=$1
MY=$2
MX=3000
MY=300
tf="1x1"
base_All_mode="$base_All_mode"
base_Only_mode="$base_Only_mode"
All_mode=All$base_All_mode
Only_mode=Only$base_Only_mode
./make_json.sh "$All_mode" Control
python XYH.py --mode "$base_All_mode" --tf "$tf" --sig $MX-$MY --r_fail SB1 --r_pass SR1 --make --makeCard --wsp Control_"$All_mode"
python modify_card.py --eff_file Templates/Templates_"$All_mode"_Control_all.root --card_file Control_"$All_mode"/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$base_All_mode" --fail_name Con"$base_All_mode"

./make_json.sh "$Only_mode" Control
python XYH.py --mode "$base_Only_mode" --tf "$tf" --sig $MX-$MY --r_fail SB1 --r_pass SR1 --make --makeCard --wsp Control_"$Only_mode"
python modify_card.py --eff_file Templates/Templates_"$Only_mode"_Control_all.root --card_file Control_"$Only_mode"/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$base_Only_mode" --fail_name Con"$base_Only_mode"

./make_json.sh "$All_mode" AValidation
python XYH.py --mode "$base_All_mode" --tf "$tf" --sig $MX-$MY --r_fail SB1 --r_pass SR1 --make --makeCard --wsp Validation_"$All_mode"_MX-"$MX"_MY-"$MY"
python modify_card.py --eff_file Templates/Templates_"$All_mode"_AValidation_all.root --card_file Validation_"$All_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$base_All_mode" --fail_name Sig"$base_All_mode"

./make_json.sh "$Only_mode" AValidation
python XYH.py --mode "$base_Only_mode" --tf "$tf" --sig $MX-$MY --r_fail SB1 --r_pass SR1 --make --makeCard --wsp Validation_"$Only_mode"_MX-"$MX"_MY-"$MY"
python modify_card.py --eff_file Templates/Templates_All"$base_Only_mode"_AValidation_all.root --card_file Validation_"$Only_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$base_Only_mode" --fail_name Sig"$base_Only_mode"

./combine_channels.sh Validation_"$All_mode"And"$Only_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area Validation_"$All_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area VAL"$base_All_mode" Validation_"$Only_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area VAL"$base_Only_mode" Control_"$All_mode"/SignalMC_XHY4b_"$tf"_area CON"$base_All_mode" Control_"$Only_mode"/SignalMC_XHY4b_"$tf"_area COM"$base_Only_mode"


./run_fit.sh  --fitdir Validation_"$All_mode"And"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/ -b -v 3 

status=${PIPESTATUS[0]}
echo $status
control_file=Validation_"$All_mode"And"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/higgsCombineSnapshot.MultiDimFit.mH125.root
root -b -q load_parameters.C\(\"$control_file\",\"control_parameters_"$All_mode"And"$Only_mode".txt\"\)



./make_json.sh "$All_mode" Signal
python XYH.py --mode "$base_All_mode" --tf "$tf" --sig $MX-$MY --r_fail SB1 --r_pass SR1 --make --makeCard --wsp Signal_"$All_mode"_MX-"$MX"_MY-"$MY"
python modify_card.py --eff_file Templates/Templates_"$All_mode"_Signal_all.root --card_file Signal_"$All_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$base_All_mode" --fail_name Sig"$base_All_mode"

./make_json.sh "$Only_mode" Signal
python XYH.py --mode "$base_Only_mode" --tf "$tf" --sig $MX-$MY --r_fail SB1 --r_pass SR1 --make --makeCard --wsp Signal_"$Only_mode"_MX-"$MX"_MY-"$MY"
python modify_card.py --eff_file Templates/Templates_All"$base_Only_mode"_Signal_all.root --card_file Signal_"$Only_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$base_Only_mode" --fail_name Sig"$base_Only_mode"

./combine_channels.sh Signal_"$All_mode"And"$Only_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area Signal_"$All_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area SIG"$base_All_mode" Signal_"$Only_mode"_MX-"$MX"_MY-"$MY"/SignalMC_XHY4b_"$tf"_area SIG"$base_Only_mode" Control_"$All_mode"/SignalMC_XHY4b_"$tf"_area CON"$base_All_mode" Control_"$Only_mode"/SignalMC_XHY4b_"$tf"_area CON"$base_Only_mode"



./run_limits.sh --fitdir Signal_"$All_mode"And"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/ -l -v 2 --mode "$All_mode"And"$Only_mode"



