mode=$1
> args.txt

find datasets -type f | while IFS= read -r file; do
    if [[ $file != *"BDT_discrete_"* || $file != *"SignalMC"* || $file != *"$mode"* ]]; then
        continue
    fi
    file=$(basename "$file")
    echo -f $eosprefix$eospath/XHY4bRun3_BDT_Training/$file -b $eosprefix$eospath/XHY4bRun3_BDT_Training/BDT_discrete_BKGs_"$mode"_ALL.root >> args.txt
done
