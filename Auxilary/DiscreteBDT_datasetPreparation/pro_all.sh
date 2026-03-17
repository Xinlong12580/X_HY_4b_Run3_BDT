#./produce_trainingSet.sh 1p1 2022
#./produce_trainingSet.sh 1p1 2022EE
#./produce_trainingSet.sh 1p1 2023
#./produce_trainingSet.sh 1p1 2023BPix
#./produce_trainingSet.sh 1p1 2024

#./optimize_hypeparameters.sh 1p1 2022 1600 300
#./optimize_hypeparameters.sh 1p1 2022EE 1600 300
#./optimize_hypeparameters.sh 1p1 2023 1600 300
#./optimize_hypeparameters.sh 1p1 2023BPix 1600 300
#./optimize_hypeparameters.sh 1p1 2024 1600 300

#python compare_AUCs_paraTuning.py --mode 1p1 --year 2022 
#python compare_AUCs_paraTuning.py --mode 1p1 --year 2022EE 
#python compare_AUCs_paraTuning.py --mode 1p1 --year 2023 
#python compare_AUCs_paraTuning.py --mode 1p1 --year 2023BPix
#python compare_AUCs_paraTuning.py --mode 1p1 --year 2024 


#python plot_ROCs_paraTuning.py --mode 1p1 --year 2022 
#python plot_ROCs_paraTuning.py --mode 1p1 --year 2022EE
#python plot_ROCs_paraTuning.py --mode 1p1 --year 2023BPix 
#python plot_ROCs_paraTuning.py --mode 1p1 --year 2023
#python plot_ROCs_paraTuning.py --mode 1p1 --year 2024 

#./retrain.sh 1p1 2022 1600 300
#./retrain.sh 1p1 2022EE 1600 300
#./retrain.sh 1p1 2023 1600 300
#./retrain.sh 1p1 2023BPix 1600 300
#./retrain.sh 1p1 2024 1600 300

python apply_MVA_discrete.py --mode 1p1 --year 2022
python apply_MVA_discrete.py --mode 1p1 --year 2022EE
python apply_MVA_discrete.py --mode 1p1 --year 2023
python apply_MVA_discrete.py --mode 1p1 --year 2023BPix
python apply_MVA_discrete.py --mode 1p1 --year 2024
