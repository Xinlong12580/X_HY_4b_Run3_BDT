file_dir=/store/user/$USER/XHY4bRun3_impact_BDT/
files=$(eosls $file_dir)
for file in $files; do
    full_path=root://cmseos.fnal.gov/$file_dir/$file
    [[ "$file" == SignalInjection_*__higgsCombine*MultiDimFit*.root ]] || continue
    tmp="${file#SignalInjection_}"
    file_name="${tmp#*__}"
    path_part="${tmp%%__*}"

    path_part="${path_part/_workspace_SignalMC_/_workspace/SignalMC_}"

    base_path="IMPACT/${path_part}/"
    original_path="SignalInjection/${path_part}/"
    echo "$base_path"
    echo "$file_name"
    mkdir -p $base_path
    xrdcp -f $full_path $base_path/$file_name
    cp "$original_path/higgsCombine.AsymptoticLimits.mH125.123456.root" $base_path/base.root
done
