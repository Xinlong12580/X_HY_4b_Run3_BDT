cat division_combined_BDT_args_full.txt | grep -v 'MX-300_' | grep -v 'MX-350_' | grep -v 'MX-400_' | grep -v 'MX-450_' | grep -v "MX-500_"  > division_combined_BDT_args.txt
cat division_combined_BDT_args_full.txt | grep -v SignalMC > division_combined_BDT_args.txt
#cat division_combined_BDT_args_full.txt | grep 'Data' | grep -v "RegSig"  > division_combined_BDT_args.txt
grep -Ev 'MX-(300|350|400|450|500|600|700|800|900)_' division_combined_BDT_args_full.txt > division_combined_BDT_args.txt
