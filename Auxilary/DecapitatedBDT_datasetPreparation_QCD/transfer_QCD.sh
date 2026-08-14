dir1=$eospath/XHY4bRun3_QCD_selection
dir2=$eospath/XHY4bRun3_selection_combined_BDT/
files=$(eosls $dir1)
for f in $files; do
    echo $dir1/$f
    eosmv $dir1/$f $dir2
done
