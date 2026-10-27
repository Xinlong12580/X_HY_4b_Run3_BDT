cat selection_args_full.txt | grep -v -- '-v nom' | grep -v "TTBar"  > selection_args.txt
#grep -F -e '-v nom' -e 'TTBar' selection_args_full.txt | grep -v QCD  > selection_args.txt
#cat selection_args_full.txt | grep 2024 | grep -- '-v nom' | grep "Signal" | grep -v "SignalMC"   > selection_args.txt
cat selection_args_full.txt | grep -v "Signal" | grep "Data"  > selection_args.txt
cat selection_args_full.txt | grep  "Control"  | grep -v SignalMC >  selection_args.txt
cat selection_args_full.txt | grep  -E "MX-1600_MY-500|MX-1600_MY-300|QCD"  | grep -E -- '-r Signal' >  selection_args_forTraining.txt


#cat selection_args_full.txt | grep  "Control"  | grep -v SignalMC | grep MC | grep 2023_ >  selection_args.txt
n=$(wc -l < selection_args_full.txt)
half=$(( (n + 1) / 2 ))

#head -n "$half" selection_args_full.txt > selection_args.txt
tail -n "+$((half + 1))" selection_args_full.txt > selection_args.txt
