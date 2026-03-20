mode=$1
year=$2
> args.txt

find datasets -type f | while IFS= read -r file; do
    if [[ $file != *"BDT_discrete_"* || $file != *"SignalMC"* || $file != *"$mode"* || $file != *"$year"_* ]]; then
        continue
    fi
    file=$(basename "$file")
    echo -f $eosprefix$eospath/XHY4bRun3_BDT_Training/$file -b $eosprefix$eospath/XHY4bRun3_BDT_Training/BDT_discrete_BKGs_RegSig_"$mode"_"$year"_ALL.root >> args.txt
done
