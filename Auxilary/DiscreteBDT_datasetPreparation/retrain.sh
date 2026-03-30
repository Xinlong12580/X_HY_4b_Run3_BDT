mode=$1
year=$2
MX=$3
MY=$4
echo max_config_"$mode"_"$year".txt
while IFS= read -r line; do
    echo $line 
    IFS="_" read -r Method NTree MinNodeSize Shrinkage BaggedSampleFraction nCuts MaxDepth <<< "$line" 
    echo 'BDT_Trainer_discrete.C("'$mode'","'$year'","'$MX'","'$MY'",'"$NTree,$MinNodeSize,$Shrinkage,$BaggedSampleFraction,$nCuts,$MaxDepth,100)"
    root -b -q 'BDT_Trainer_discrete.C("'$mode'","'$year'","'$MX'","'$MY'",'"$NTree,$MinNodeSize,$Shrinkage,$BaggedSampleFraction,$nCuts,$MaxDepth,70)"
    break
done < max_config_"$mode"_"$year".txt
