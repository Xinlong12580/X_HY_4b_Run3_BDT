mode=$1
year=$2
MX=$3
MY=$4
echo max_config_MX"$MX"_MY"$MY"_"$mode"_"$year".txt
while IFS= read -r line; do
    echo $line 
    IFS="_" read -r Method NTree MinNodeSize Shrinkage BaggedSampleFraction nCuts MaxDepth <<< "$line" 
    echo 'BDT_Trainer_discrete.C("'$mode'","'$year'","'$MX'","'$MY'",'"$NTree,$MinNodeSize,$Shrinkage,$BaggedSampleFraction,$nCuts,$MaxDepth,100)"
    root -b -q 'BDT_Trainer_discrete.C("'$mode'","'$year'","'$MX'","'$MY'",'"$NTree,$MinNodeSize,$Shrinkage,$BaggedSampleFraction,$nCuts,$MaxDepth,99)"
    break
done < max_config_MX"$MX"_MY"$MY"_"$mode"_"$year".txt
