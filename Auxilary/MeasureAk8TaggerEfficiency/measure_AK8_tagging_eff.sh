years=(2022 2022EE 2023 2023BPix 2024)
for year in ${years[@]}; do
    while IFS= read -r line; do
        if [[ $line != *"$year"_* || $line == *"Template"* ]]; then
            continue
        fi
        #echo $line
        tmp="${line#*XHY4b__}"
        dataset="${tmp%%_n-*}"

        echo $year $dataset
        #python measure_AK8_tagging_eff.py -y $year -d $dataset -m 2p1
        python measure_AK8_tagging_eff.py -y $year -d $dataset -m 1p1
    done < ../../outputList/output_Xbbtagging_2p1_BDT.txt
done 
