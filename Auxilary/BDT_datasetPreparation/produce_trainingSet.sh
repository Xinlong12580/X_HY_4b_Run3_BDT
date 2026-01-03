mode=$1
./hadd_selection.sh $mode
python BDT_reweighting.py --mode $mode
BKG_files=$(find ./datasets -maxdepth 1 -type f -name "reweight*" -name "*$mode*" ! -name '*SignalMC*' ! -name '*Control*' -printf '%f\n')
file_string=" "
while IFS= read -r file; do
  file_string=$file_string" datasets/"$file
done <<< "$BKG_files"
echo $file_string
hadd datasets/BKGs_"$mode"_ALL.root $file_string

