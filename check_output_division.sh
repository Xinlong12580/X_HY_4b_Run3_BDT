output=$1
process=""
#process=NanoAODv15
years=(2022__ 2022EE__ 2023__ 2023BPix__ 2024__ )

if [[ $output == "division_"*"_BDT" ]]; then
    echo $output
    amend_file=amend_division_args.txt
    > $amend_file
    input_file=division_combined_BDT_args.txt
    output_dir=/store/user/xinlong/XHY4bRun3_$output
    output_files=$(eosls $output_dir/*$process* | grep -v Template )
    declare -A classified_files
    for file in ${output_files[@]}; do
        for year in ${years[@]}; do
            if [[ $file == *"$year"* ]]; then
                classified_files["$year"]="${classified_files["$year"]} $file"        
                break
            fi
        done
    done
    #echo ${classified_files["2024__"]}
    while IFS= read -r line; do
        #echo $line
        if [[ $line != *$process* ]]; then
            continue
        fi
        input_arg=$(echo "$line" | awk '{print $2}')
        file_base=$(basename $input_arg)
        file_base="${file_base%.*}"_
        input_y=$(echo "$line" | awk '{print $4}')__
        input_n=$(echo "$line" | awk '{print $6}')
        input_i=$(echo "$line" | awk '{print $8}')
        n_base="n-"$input_n
        i_base="i-"$input_i
        found=0
        for file in ${classified_files["$input_y"]}; do
            #echo $file
            if [[ $file != *"Templates"* && $file == *"$file_base"* && $file == *"$n_base"* && $file == *"$i_base"* ]]; then
                #echo $file_base $file $n_base $i_base $JME_base $Reg_base
              
                found=1
                #classified_files["$input_y"]="${classified_files[$input_y]//$file/}"
                break
            fi
        done

        if [[ $found == 0 ]] ; then
            echo $file_base $n_base $i_base 
            echo Missing $line
            echo $line >> $amend_file
        fi
            
    done < $input_file
fi
