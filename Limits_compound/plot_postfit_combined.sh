fit_dir=$1
tf=$2
pass_name=$3
fail_name=$4
mode=$5
do_loading=$6
curr_dir=$(pwd)
cp plotting/*py $fit_dir
cd $fit_dir
echo python plot_1d.py --tf $tf --pass_name "$pass_name"_Region0 --fail_name "$fail_name"_SB1_1p1_Region0
if [[ $do_loading == 1 ]]; then
    PostFit2DShapesFromWorkspace -w higgsCombineSnapshot.MultiDimFit.mH125.root --output postfitshapes_b.root -f multidimfitSnapshot.root:fit_mdf --postfit --samples 100 --print
fi
python plot_1d.py --tf $tf --pass_name "$pass_name"_Region0 --fail_name "$fail_name"_Region0 --title_extra $mode --method 1 
python plot_1d_perbin.py --tf $tf --pass_name "$pass_name"_Region0 --fail_name "$fail_name"_Region0 --title_extra $mode --method 1
cp "$mode"_"$fail_name"_Region0_"$tf"_mX.png  "$mode"_"$fail_name"_Region0_mX.png
cp "$mode"_"$fail_name"_Region0_"$tf"_mY.png  "$mode"_"$fail_name"_Region0_mY.png
cp "$mode"_"$pass_name"_Region0_"$tf"_mX.png  "$mode"_"$pass_name"_Region0_mX.png
cp "$mode"_"$pass_name"_Region0_"$tf"_mY.png  "$mode"_"$pass_name"_Region0_mY.png
cp perbin_"$mode"_"$fail_name"_Region0_"$tf"_mX.png  perbin_"$mode"_"$fail_name"_Region0_mX.png
cp perbin_"$mode"_"$fail_name"_Region0_"$tf"_mY.png  perbin_"$mode"_"$fail_name"_Region0_mY.png
cp perbin_"$mode"_"$pass_name"_Region0_"$tf"_mX.png  perbin_"$mode"_"$pass_name"_Region0_mX.png
cp perbin_"$mode"_"$pass_name"_Region0_"$tf"_mY.png  perbin_"$mode"_"$pass_name"_Region0_mY.png
cp log_"$mode"_"$fail_name"_Region0_"$tf"_mX.png  log_"$mode"_"$fail_name"_Region0_mX.png
cp log_"$mode"_"$fail_name"_Region0_"$tf"_mY.png  log_"$mode"_"$fail_name"_Region0_mY.png
cp log_"$mode"_"$pass_name"_Region0_"$tf"_mX.png  log_"$mode"_"$pass_name"_Region0_mX.png
cp log_"$mode"_"$pass_name"_Region0_"$tf"_mY.png  log_"$mode"_"$pass_name"_Region0_mY.png
cp log_perbin_"$mode"_"$fail_name"_Region0_"$tf"_mX.png  log_perbin_"$mode"_"$fail_name"_Region0_mX.png
cp log_perbin_"$mode"_"$fail_name"_Region0_"$tf"_mY.png  log_perbin_"$mode"_"$fail_name"_Region0_mY.png
cp log_perbin_"$mode"_"$pass_name"_Region0_"$tf"_mX.png  log_perbin_"$mode"_"$pass_name"_Region0_mX.png
cp log_perbin_"$mode"_"$pass_name"_Region0_"$tf"_mY.png  log_perbin_"$mode"_"$pass_name"_Region0_mY.png
cp *png ../../plotting/postfit_plots

cd $curr_dir

