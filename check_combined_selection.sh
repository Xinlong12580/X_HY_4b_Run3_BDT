#selection_args_set=('-d outputList/SKIM_masked_skimmed_2022EE__Data__JetMET__Run2022E-NanoAODv15-v1__NANOAOD.txt -y 2022EE -n 1 -i 18 -s nom -r Control')
#selection_args_set+=('-d outputList/SKIM_skimmed_2022EE__MC_TTBarJets__TTto4Q.txt -y 2022EE -n 1 -i 22 -s nom -r Control')
#selection_args_set+=('-d outputList/SKIM_masked_skimmed_2022EE__Data__JetMET__Run2022E-NanoAODv15-v1__NANOAOD.txt -y 2022EE -n 1 -i 18 -s nom -r Signal')
#selection_args_set+=('-d outputList/SKIM_skimmed_2022EE__MC_TTBarJets__TTto4Q.txt -y 2022EE -n 1 -i 22 -s nom -r Signal')
#selection_args_set+=('-d outputList/SKIM_masked_skimmed_2022EE__Data__JetMET__Run2022E-NanoAODv15-v1__NANOAOD.txt -y 2022EE -n 1 -i 18 -s nom -r Validation')
#selection_args_set+=('-d outputList/SKIM_skimmed_2022EE__MC_TTBarJets__TTto4Q.txt -y 2022EE -n 1 -i 22 -s nom -r Validation')
#selection_args_set=('-d outputList/SKIM_skimmed_2022EE__SignalMC_XHY4b__MX-3000_MY-500.txt -y 2022EE -n 10000 -i 0 -s JES__up -r Control')
selection_args_set=('-d outputList/SKIM_skimmed_2022EE__SignalMC_XHY4b__MX-3000_MY-500.txt -y 2022EE -n 10000 -i 0 -s JES__up -r Signal')
#selection_args_set+=('-d outputList/SKIM_skimmed_2022EE__SignalMC_XHY4b__MX-3000_MY-500.txt -y 2022EE -n 10000 -i 0 -s JES__up -r Validation')
echo $selections_args_set
for selection_args in "${selection_args_set[@]}"; do
    echo $selection_args
    #continue
    base_output=$(echo "$selection_args" | grep -oP 'SKIM.*?.txt')
    n_pre=0
    i_pre=0
    r_pre=0
    s_pre=0
    for part in $selection_args; do
        if [[ $n_pre == 1 ]]; then
            n=$part
            n_pre=0
        fi
        if [[ $i_pre == 1 ]]; then
            i=$part
            i_pre=0
        fi
        if [[ $r_pre == 1 ]]; then
            r=$part
            r_pre=0
        fi
        if [[ $s_pre == 1 ]]; then
            s=$part
            s_pre=0
        fi
        if [[ $part == "-n" ]]; then
            n_pre=1
        fi
        if [[ $part == "-i" ]]; then
            i_pre=1
        fi
        if [[ $part == "-r" ]]; then
            r_pre=1
        fi
        if [[ $part == "-s" ]]; then
            s_pre=1
        fi
    done
    #python run_selection_1p1_BDT.py $selection_args
    #python run_selection_2p1_BDT.py $selection_args
    python run_selection_combined_BDT.py $selection_args


    base_output="${base_output/.txt/_n-"$n"_i-"$i".root}"
    f_1p1="Reg"${r:0:3}"_"$s"_1p1_tagged_selected_"$base_output
    f_2p1="Reg"${r:0:3}"_"$s"_2p1_tagged_selected_"$base_output
    f_combined="Reg"${r:0:3}"_"$s"_combined_tagged_selected_"$base_output
    python check_combined.py --1p1 $f_1p1 --2p1 $f_2p1 --combined $f_combined
done
