mode=$1
year=$2
#rm datasets/*root
input_dir=/store/user/xinlong/XHY4bRun3_selection_"$mode"_BDT
output_dir="./datasets/"
eosmkdir -p "$output_dir"
echo "TEST!"
files=$( eosls $input_dir | grep "$year"_ | grep "nom" )
prefix=$eosprefix$input_dir/
declare -A classified_files
declare -A classified_file_idxs
for file in ${files[@]}; do
    if [[ $file == *"Template"* || $file != *"$year"_* || $file != *"nom"* ]]; then
        continue
    fi
    file_base="${file%%_n-*}"
    classified_files["$file_base"]="${classified_files["$file_base"]} $prefix$file"
    tmp="${file#*_i-}"
    file_idx="${tmp%%.root*}"
    #classfified_file_idxs["$file_base"]="${classfified_file_idxs["$file_base"]} $file_idx"
done

for file_base in ${!classified_files[@]}; do
    echo $file_base
    if [[ $file_base == *HT-100to* || $file_base == *HT-200to* || $file_base == *HT-400to* || $file_base == *HT-600to* ]]; then
        continue
    fi
    _files=${classified_files[$file_base]}  ###############REMOVE EMPTY FILES AT THE BEGINNING, or hadd will create empty files
    _files="${_files#* }"
    for f in ${classified_files[$file_base]}; do
        isempty=$(python check_empty.py -f $f)
        if [[ $isempty == 1 ]]; then
            _files="${_files#* }"
        else
            break
        fi
    done
    hadd "$output_dir""$file_base"_"$mode"_ALL.root $_files
    #fi
done


