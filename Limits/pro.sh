MX=$1
MY=$2
MX=4000
MY=2000
tf="1x1"
#./clearworkspace.sh
./make_json.sh 2p1 Control
python XYH.py --tf "$tf" --sig $MX-$MY --r_fail SB1 --r_pass SR1 --make --makeCard --wsp Control_MX-"$MX"_MY-"$MY"
#python XYH.py --tf 1x1 --sig $MX-$MY --r_fail SB1 --r_pass SR1 --fit --plot --wsp Control_MX-"$MX"_MY-"$MY"

./run_fit.sh  --fitdir Control_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/ -b -v 3 
#./run_fit_diagnostics.sh --fitdir Control_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_1x1_area/ -b -v 3 

status=${PIPESTATUS[0]}
echo $status
control_file=Control_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_1x1_area/higgsCombineSnapshot.MultiDimFit.mH125.root
control_file=Control_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/higgsCombineSnapshot.MultiDimFit.mH125.root
root -b -q load_parameters.C\(\"$control_file\"\)

./make_json.sh 2p1 Signal
#python XYH.py --tf 1x1 --sig $MX-$MY --r_fail SB1 --r_pass SR1 --make --makeCard --wsp Loose_MX-"$MX"_MY-"$MY"
#python XYH.py --tf "$tf" --sig $MX-$MY --r_fail SB1 --r_pass SR1 --make --makeCard --wsp Loose_MX-"$MX"_MY-"$MY"
#./run_limits.sh --fitdir Loose_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_1x1_area/ -l -v 2
#./run_limits.sh --fitdir Loose_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/ -l -v 2

####################################f test###########################################################
#tfs=(0x0 1x0 0x1 1x1 1x2 2x1)
tfs=(1x1)
tfs=()
for tf in "${tfs[@]}"; do
    python XYH.py --tf $tf --sig $MX-$MY --r_fail VB1 --r_pass VS1 --makeCard --wsp Control_MX-"$MX"_MY-"$MY"
    ./run_GoF.sh  --fitdir Control_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/ -b -v 3 
    
done

#./run_signal_injection.sh  --fitdir Loose_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_1x1_area/ -b -v 3 -r 0
