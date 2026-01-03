mode=$1
find datasets -type f | while IFS= read -r file; do
    if [[  $file != *"/BDT"*"1p1"* ]] ; then
        continue
    fi
    echo $file
    file_base=$( basename $file )
    xrdcp -f $file $eosprefix$eospath/XHY4bRun3_BDT_Training/$file_base 
done
