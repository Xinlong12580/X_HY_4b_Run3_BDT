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
cp *png ../../plotting/plots
cd $curr_dir

