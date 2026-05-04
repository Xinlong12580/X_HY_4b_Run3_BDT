position=0
target_dir=""
isDir=0
combine_arg=""
for arg in "$@"; do
    (( position ++ ))
    if [[ $position == 1 ]]; then
        mkdir -p $arg
        target_dir=$arg
    else
        (( isDir = 1-isDir ))
        if [[ $isDir == 1 ]]; then
            source_dir=$arg 
        else
            cp $source_dir/card.txt $target_dir/card_"$arg".txt
            cp $source_dir/../base.root $target_dir/../base_"$arg".root
            sed -i 's/base.root/'base_"$arg".root'/g' $target_dir/card_"$arg".txt
            combine_arg=$combine_arg" "$args"="card_"$arg".txt
        fi
    fi
done
cd $target_dir
combineCards.py $combine_arg > card.txt
cd ../..
