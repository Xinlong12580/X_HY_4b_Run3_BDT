input_dir=/store/user/xinlong/XHY4bRun3_SI_BDT
output_dir="./datasets/"
datapoint=CS_All2p1AndOnly1p1_MX-2000_MY-800_workspace_SignalMC_XHY4b_area__higgsCombiner_0
eosmkdir -p "$output_dir"
echo "TEST!"

files=$( eosls $input_dir | grep $datapoint )
safe_files=""
for file in $files; do
    f=$eosprefix$input_dir/$file
    echo $f
    #isempty=$(python check_empty.py -f $f -t limit )    
    isempty=0
    if [[  $isempty != 1 ]] ; then
        echo test
        safe_files=$safe_files" "$f
    fi
done
echo hadd "$datapoint".root $safe_files
hadd -f "$datapoint".root $safe_files
