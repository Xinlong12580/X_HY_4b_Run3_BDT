find datasets -type f | while IFS= read -r file; do
    f_name=$(basename "$file")
    if [[ $f_name != *"Signal"* ]]; then
        continue
    fi
    echo "Processing: $f_name"
    python apply_MVA.py -f $f_name
    #break
done 
