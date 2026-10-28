while IFS= read -r line; do
    read _Reg _mode _tf <<< "$line"
    echo python gof_grid.py --fitdir "${_Reg:0:1}"*_"$_mode"_workspace/SignalMC_XHY4b_"$_tf"_area --title "$_Reg$_mode$_tf"
    python gof_grid.py --fitdir "${_Reg:0:1}"*_"$_mode"_workspace/SignalMC_XHY4b_"$_tf"_area --title "$_Reg$_mode$_tf"
    
done < BEST_TF.txt
