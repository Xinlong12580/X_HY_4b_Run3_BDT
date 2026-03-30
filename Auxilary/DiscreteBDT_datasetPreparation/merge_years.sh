mode=$1
years=($2 $3 $4 $5 $6)
echo "Merging these years:"
for year in ${years[@]}; do
    echo $year
done

year_base=${years[0]}
echo $year_base
files=$(ls datasets/)
for f in $files; do
    if [[ $f == *"$year_base"_* && $f == *"$mode"* && $f != *"merged"* ]]; then
        f_allyears=""
        str_years=""
        for year in ${years[@]}; do
            new_f="${f//$year_base/$year}"
            f_allyears=$f_allyears" datasets/"$new_f
            str_years="$str_years""$year""_"
        done
        f_merge=${f//"$year_base"_/"$str_years"merged_}
        echo $f_merge
        echo $f_allyears
        hadd -f datasets/$f_merge $f_allyears
    fi
done

