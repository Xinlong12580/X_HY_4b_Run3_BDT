#while IFS= read -r line; do
#    read MX MY <<< $line
#    python load_fit_TH.py --mx $MX --my $MY --mode 2p1 --type signal
#done < ../raw_nano/GoodMassPoints.txt
python load_fit_TH.py --mx $1 --my $2 --mode $3 --type all --Reg $4 --ngroup 7 --igroup 1
python load_fit_TH.py --mx $1 --my $2 --mode $3 --type all --Reg $4 --ngroup 7 --igroup 2
python load_fit_TH.py --mx $1 --my $2 --mode $3 --type all --Reg $4 --ngroup 7 --igroup 3
python load_fit_TH.py --mx $1 --my $2 --mode $3 --type all --Reg $4 --ngroup 7 --igroup 4
python load_fit_TH.py --mx $1 --my $2 --mode $3 --type all --Reg $4 --ngroup 7 --igroup 5
python load_fit_TH.py --mx $1 --my $2 --mode $3 --type all --Reg $4 --ngroup 7 --igroup 6
python load_fit_TH.py --mx $1 --my $2 --mode $3 --type all --Reg $4 --ngroup 7 --igroup 7

./hist_preprosessing.sh $1 $2
#./make_MCstats_templates.sh $1 $2
