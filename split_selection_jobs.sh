cat selection_args_full.txt | grep -v -- '-v nom' | grep -v "TTBar"  > selection_args.txt
#grep -F -e '-v nom' -e 'TTBar' selection_args_full.txt | grep -v QCD  > selection_args.txt
#cat selection_args_full.txt | grep 2024 | grep -- '-v nom' | grep "Signal" | grep -v "SignalMC"   > selection_args.txt
