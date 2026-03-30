modes=(1p1 2p1)
years=(2022 2022EE 2023 2023BPix 2024)
for mode in ${modes[@]}; do
    for year in ${years[@]}; do
        echo $mode $year
        cp dataset_"$mode"_"$year"_discrete/weights/TMVAClassification_BDTG_"$mode"_"$year".weights.xml ../../raw_nano/BDTs
    done
done
