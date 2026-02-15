mode=$1
find datasets -type f | while IFS= read -r file; do
    if [[ ( $mode != "1p1" && $mode != "2p1" ) || ( $mode == "1p1" && $file != *"/BDT"*"1p1"* ) || ( $mode == "2p1" && $file != *"/BDT"*"2p1"* ) ]] ; then
        continue
    fi
    echo $file
    file_base=$( basename $file )
    xrdcp -f $file $eosprefix$eospath/XHY4bRun3_BDT_Training/$file_base 
done
