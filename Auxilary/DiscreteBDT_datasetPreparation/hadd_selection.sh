mode=$1
#rm datasets/*root
input_dir=/store/user/xinlong/XHY4bRun3_selection_"$mode"_BDT
output_dir="./datasets/"
eosmkdir -p "$output_dir"
echo "TEST!"
files=$( eosls $input_dir | grep "2022EE" | grep "nom" )
prefix=$eosprefix$input_dir/
declare -A classified_files
declare -A classified_file_idxs
for file in ${files[@]}; do
    if [[ $file == *"Template"* || $file != *"2022EE"* || $file != *"nom"* ]]; then
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
    echo ${classified_files[$file_base]}
    hadd "$output_dir""$file_base"_"$mode"_ALL.root ${classified_files[$file_base]}
done


