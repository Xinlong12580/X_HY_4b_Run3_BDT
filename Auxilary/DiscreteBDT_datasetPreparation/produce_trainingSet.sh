mode=$1
year=$2
./hadd_selection.sh $mode $year
python BDT_reweighting.py --mode $mode --year $year
BKG_files=$(find ./datasets -maxdepth 1 -type f -name "reweight*" -name "*$mode*" -name *"$year"_* ! -name '*SignalMC*' ! -name '*Data*' ! -name '*RegCon*' -printf '%f\n')
file_string=" "
while IFS= read -r file; do
  file_string=$file_string" datasets/"$file
done <<< "$BKG_files"
echo $file_string
hadd -f datasets/BKGs_RegSig_"$mode"_"$year"_ALL.root $file_string

