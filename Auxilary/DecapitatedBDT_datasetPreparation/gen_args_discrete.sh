mode=$1
year=$2
MX=$3
MY=$4
> args.txt

find datasets -type f | while IFS= read -r file; do
    echo $file
    if [[ $file != *"BDT_discrete_"* || $file != *"SignalMC"* || $file != *"$mode"* || $file != *"$year"_* || $file != *MX"$MX"_MY"$MY"* ]]; then
        continue
    fi
    file=$(basename "$file")
    echo -f $eosprefix$eospath/XHY4bRun3_BDT_Training/$file -b $eosprefix$eospath/XHY4bRun3_BDT_Training/BDT_discrete_MX"$MX"_MY"$MY"_BKGs_RegSig_"$mode"_"$year"_ALL.root >> args.txt
done
