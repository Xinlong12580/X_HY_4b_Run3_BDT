mode=$1
year=$2
mx_BDT=$3
my_BDT=$4
> args_P2F.txt

MX=200
while (( MX < 4000 )); do
    MY=40
    while (( MY < MX )); do
        echo $MX $MY
        echo --MX $MX --MY $MY -b $eosprefix$eospath/XHY4bRun3_BDT_Training/BDT_discrete_MX"$mx_BDT"_MY"$my_BDT"_BKGs_RegSig_"$mode"_"$year"_ALL.root >> args_P2F.txt
        (( MY = ( MY / 10 ) > 100 ? MY + 100 : ( MY + ( ( MY / 10 ) > 10 ? ( MY / 10 ) : 10 ) ) ))
    done
    (( MX = MX + 50 ))
done
