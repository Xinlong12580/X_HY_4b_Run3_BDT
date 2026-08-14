output=$1
process=$2
years=(2022__ 2022EE__ 2023__ 2023BPix__ 2024__ )

if [[ $output == "selection_"*"_BDT" ]]; then
    echo $output
    amend_file=amend_selection_args.txt
    > $amend_file
    input_file=selection_args.txt
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
        input_process=$process
        if  [[ $process == *"Reg"* ]]; then
            input_process=' '"${process:3:6}"
        fi
        if [[ $line != *$input_process* ]]; then
            continue
        fi
        #echo $line
        #echo $line
        input_arg=$(echo "$line" | awk '{print $2}')
        file_base=$(basename $input_arg)
        file_base="${file_base%.*}"_
        input_y=$(echo "$line" | awk '{print $4}')__
        input_n=$(echo "$line" | awk '{print $6}')
        input_i=$(echo "$line" | awk '{print $8}')
        JME_base=$(echo "$line" | awk '{print $10}')
        Reg_base=$(echo "$line" | awk '{print $12}')
        #echo $Reg_base
        Reg_base=Reg"${Reg_base:0:3}"
        n_base="n-"$input_n
        i_base="i-"$input_i
        found=0
        for file in ${classified_files["$input_y"]}; do
            
            #echo $file
            if [[ $file != *"Templates"* && $file == *"$file_base"* && $file == *"$n_base"* && $file == *"$i_base"* && $file == *"$JME_base"* && $file == $Reg_base* ]]; then
                #echo $file_base $file $n_base $i_base $JME_base $Reg_base
              
                #echo $file
                found=1
                #classified_files["$input_y"]="${classified_files[$input_y]//$file/}"
                break
            fi
        done

        if [[ $found == 0 ]] ; then
            echo $file_base $n_base $i_base $JME_base $Reg_base
            echo Missing $line
            echo $line >> $amend_file
        fi
            
    done < $input_file
fi
