#while IFS= read -r line; do
#    read MX MY <<< $line
#    python load_fit_TH.py --mx $MX --my $MY --mode 2p1 --type signal
#done < ../raw_nano/GoodMassPoints.txt
rm Templates/*
#python load_fit_TH.py --mx $1 --my $2 --mode All1p1 --type all --Reg Signal
#python load_fit_TH.py --mx $1 --my $2 --mode All2p1 --type all --Reg Signal
#python load_fit_TH.py --mx $1 --my $2 --mode Only1p1 --type all --Reg Signal
#python load_fit_TH.py --mx $1 --my $2 --mode Only2p1 --type all --Reg Signal

python load_fit_TH.py --mx $1 --my $2 --mode All1p1 --type all --Reg Control
python load_fit_TH.py --mx $1 --my $2 --mode All2p1 --type all --Reg Control
python load_fit_TH.py --mx $1 --my $2 --mode Only1p1 --type all --Reg Control
python load_fit_TH.py --mx $1 --my $2 --mode Only2p1 --type all --Reg Control

python load_fit_TH.py --mx $1 --my $2 --mode All1p1 --type all --Reg Validation
python load_fit_TH.py --mx $1 --my $2 --mode All2p1 --type all --Reg Validation
python load_fit_TH.py --mx $1 --my $2 --mode Only1p1 --type all --Reg Validation
python load_fit_TH.py --mx $1 --my $2 --mode Only2p1 --type all --Reg Validation

./hist_preprosessing.sh $1 $2
