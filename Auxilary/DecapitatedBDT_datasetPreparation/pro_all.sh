MX=1600
MY=300
mode=1p1
#./produce_trainingSet.sh $mode 2022
#./produce_trainingSet.sh $mode 2022EE
#./produce_trainingSet.sh $mode 2023
#./produce_trainingSet.sh $mode 2023BPix
#./produce_trainingSet.sh $mode 2024
#./merge_years.sh $mode 2022 2022EE 2023 2023BPix 2024
python merge_years.py --mode $mode --years "2022;2022EE;2023;2023BPix;2024"

#./optimize_hypeparameters.sh $mode 2022 $MX $MY
#./optimize_hypeparameters.sh $mode 2022EE $MX $MY
#./optimize_hypeparameters.sh $mode 2023 $MX $MY
#./optimize_hypeparameters.sh $mode 2023BPix $MX $MY
#./optimize_hypeparameters.sh $mode 2024 $MX $MY
./optimize_hypeparameters.sh $mode 2022_2022EE_2023_2023BPix_2024_merged $MX $MY 

#python compare_AUCs_paraTuning.py --mode $mode --year 2022 --mx $MX --my $MY 
#python compare_AUCs_paraTuning.py --mode $mode --year 2022EE --mx $MX --my $MY
#python compare_AUCs_paraTuning.py --mode $mode --year 2023 --mx $MX --my $MY
#python compare_AUCs_paraTuning.py --mode $mode --year 2023BPix --mx $MX --my $MY
#python compare_AUCs_paraTuning.py --mode $mode --year 2024 --mx $MX --my $MY
python compare_AUCs_paraTuning.py --mode $mode --year 2022_2022EE_2023_2023BPix_2024_merged --mx $MX --my $MY


#python plot_ROCs_paraTuning.py --mode $mode --year 2022 --mx $MX --my $MY
#python plot_ROCs_paraTuning.py --mode $mode --year 2022EE --mx $MX --my $MY
#python plot_ROCs_paraTuning.py --mode $mode --year 2023BPix --mx $MX --my $MY
#python plot_ROCs_paraTuning.py --mode $mode --year 2023 --mx $MX --my $MY
#python plot_ROCs_paraTuning.py --mode $mode --year 2024 --mx $MX --my $MY
python plot_ROCs_paraTuning.py --mode $mode --year 2022_2022EE_2023_2023BPix_2024_merged --mx $MX --my $MY

#./retrain.sh $mode 2022 $MX $MY
#./retrain.sh $mode 2022EE $MX $MY
#./retrain.sh $mode 2023 $MX $MY
#./retrain.sh $mode 2023BPix $MX $MY
#./retrain.sh $mode 2024 $MX $MY
./retrain.sh $mode 2022_2022EE_2023_2023BPix_2024_merged $MX $MY

#python plot_BDTG.py --mode $mode --year 2022 --mx $MX --my $MY
#python plot_BDTG.py --mode $mode --year 2022EE --mx $MX --my $MY
#python plot_BDTG.py --mode $mode --year 2023BPix --mx $MX --my $MY
#python plot_BDTG.py --mode $mode --year 2023 --mx $MX --my $MY
#python plot_BDTG.py --mode $mode --year 2024 --mx $MX --my $MY
python plot_BDTG.py --mode $mode --year 2022_2022EE_2023_2023BPix_2024_merged --mx $MX --my $MY

#python apply_MVA_discrete.py --mode $mode --year 2022 --mx $MX --my $MY
#python apply_MVA_discrete.py --mode $mode --year 2022EE --mx $MX --my $MY
#python apply_MVA_discrete.py --mode $mode --year 2023 --mx $MX --my $MY
#python apply_MVA_discrete.py --mode $mode --year 2023BPix --mx $MX --my $MY
#python apply_MVA_discrete.py --mode $mode --year 2024 --mx $MX --my $MY
python apply_MVA_discrete.py --mode $mode --year 2022_2022EE_2023_2023BPix_2024_merged --mx $MX --my $MY

#python make_BKG_template.py --mode $mode --year 2022
#python make_BKG_template.py --mode $mode --year 2022EE
#python make_BKG_template.py --mode $mode --year 2023
#python make_BKG_template.py --mode $mode --year 2023BPix
#python make_BKG_template.py --mode $mode --year 2024
