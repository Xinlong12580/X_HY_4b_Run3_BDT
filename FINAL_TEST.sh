#python run_skim.py -d raw_nano/files/2023__SignalMC_XHY4b__MX-900_MY-500.txt -y 2023 -n 1 -i 0
#python run_selection_2p1_BDT.py -d skimmed_2023__SignalMC_XHY4b__MX-900_MY-500.txt_n-1_i-0.root -y 2023 -n 1 -i 0 -s nom
#python run_selection_1p1_BDT.py -d skimmed_2023__SignalMC_XHY4b__MX-900_MY-500.txt_n-1_i-0.root -y 2023 -n 1 -i 0 -s nom

#python run_skim.py -d raw_nano/files/2023__SignalMC_XHY4b__MX-3000_MY-1000.txt -y 2023 -n 1 -i 0
#python run_selection_2p1_BDT.py -d skimmed_2023__SignalMC_XHY4b__MX-3000_MY-1000.txt_n-1_i-0.root -y 2023 -n 1 -i 0 -s nom
#python run_selection_1p1_BDT.py -d skimmed_2023__SignalMC_XHY4b__MX-3000_MY-1000.txt_n-1_i-0.root -y 2023 -n 1 -i 0 -s nom


#python run_skim.py -d raw_nano/files/2024__SignalMC_XHY4b__MX-900_MY-500.txt -y 2024 -n 1 -i 0
#python run_selection_2p1_BDT.py -d skimmed_2024__SignalMC_XHY4b__MX-900_MY-500.txt_n-1_i-0.root -y 2024 -n 1 -i 0 -s nom
#python run_selection_1p1_BDT.py -d skimmed_2024__SignalMC_XHY4b__MX-900_MY-500.txt_n-1_i-0.root -y 2024 -n 1 -i 0 -s nom


#python run_skim.py -d raw_nano/files/2022__Data__JetMET__Run2022C-NanoAODv15-v1__NANOAOD.txt -y 2022 -n 1 -i 0
python run_selection_2p1_BDT.py -d masked_skimmed_2022__Data__JetMET__Run2022C-NanoAODv15-v1__NANOAOD.txt_n-1_i-0.root -y 2022 -n 1 -i 0 -s nom
#python run_selection_1p1_BDT.py -d masked_skimmed_2022__Data__JetMET__Run2022C-NanoAODv15-v1__NANOAOD.txt_n-1_i-0.root -y 2022 -n 1 -i 0 -s nom
ls -lh *root
