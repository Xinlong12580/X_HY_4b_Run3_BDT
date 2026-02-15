years=(2022 2022EE 2023 2023BPix)
modes=(1p1 2p1)
modes=(1p1 2p1)
processes=(JetMET)
processes=(MC_TTBarJets__TTto4Q JetMET)
for year in "${years[@]}"; do
    for mode in "${modes[@]}"; do
        for process in "${processes[@]}"; do
            python add_trigger.py -y $year -m $mode -p $process
        done
    done
done
