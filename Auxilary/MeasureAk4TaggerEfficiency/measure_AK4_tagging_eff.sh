years=(2022 2022EE 2023 2023BPix 2024)
for year in ${years[@]}; do
    while IFS= read -r line; do
        if [[ $line != *"$year"_* ]]; then
            continue
        fi
        #echo $line
        tmp="${line#*XHY4b__}"
        dataset="${tmp%%_n-*}"

        echo $year $dataset
        python measure_AK4_tagging_eff.py -y $year -d $dataset
    done < ../../outputList/output_btagging_2p1_BDT.txt
done 
