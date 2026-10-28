#!/usr/bin/env bash
set -euo pipefail
fitdir=SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI_impact.txt","clean")' -b -q
./run_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt --ngroup 100 --igroup 11 -v 99 --tol 0.2
exit
fitdir=SignalInjection/CS_All1p1AndOnly2p1_MX-1800_MY-200_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI_impact.txt","clean")' -b -q
./run_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./run_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI_impact.txt","clean")' -b -q
./run_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./run_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=SignalInjection/CS_All2p1AndOnly1p1_MX-1800_MY-800_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI_impact.txt","clean")' -b -q
./run_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./run_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=SignalInjection/CS_All2p1AndOnly1p1_MX-3500_MY-800_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI_impact.txt","clean")' -b -q
./run_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./run_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

