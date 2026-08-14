modes="All1p1AndOnly2p1 All2p1AndOnly1p1"
#modes="All2p1AndOnly1p1"
#modes=All1p1AndOnly2p1
for mode in $modes; do
    base_All_mode=${mode#*All}     
    base_All_mode=${base_All_mode%%AndOnly*}
    base_Only_mode=${mode#*Only}
    All_mode=All$base_All_mode
    Only_mode=Only$base_Only_mode
    while IFS= read -r line; do
        read _Reg _mode _tf <<< "$line"
        echo python gof_grid.py --fitdir "${_Reg:0:1}"*_"$_mode"_workspace/SignalMC_XHY4b_"$_tf"_area --title "$_Reg$_mode$_tf"
        python gof_grid.py --fitdir "${_Reg:0:1}"*_"$_mode"_workspace/SignalMC_XHY4b_"$_tf"_area --title "$_Reg$_mode$_tf"
        
    done < BEST_TF.txt

    python gof_grid.py --fitdir CV_"$mode"_workspace/SignalMC_XHY4b_area/ --title "$mode"
done
