#!/usr/bin/env bash
set -euo pipefail
base_dir=IMPACT
fitdir=$base_dir/CS_All1p1AndOnly2p1_MX-1800_MY-200_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/base.root","para_SI_impact.txt","clean")' -b -q
./plot_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./plot_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=$base_dir/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/base.root","para_SI_impact.txt","clean")' -b -q
./plot_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./plot_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=$base_dir/CS_All2p1AndOnly1p1_MX-1800_MY-800_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/base.root","para_SI_impact.txt","clean")' -b -q
./plot_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./plot_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=$base_dir/CS_All2p1AndOnly1p1_MX-3500_MY-800_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/base.root","para_SI_impact.txt","clean")' -b -q
./plot_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./plot_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=$base_dir/withfloor_CS_All1p1AndOnly2p1_MX-1800_MY-200_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/base.root","para_SI_impact.txt","clean")' -b -q
./plot_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./plot_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=$base_dir/withfloor_CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/base.root","para_SI_impact.txt","clean")' -b -q
./plot_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./plot_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=$base_dir/withfloor_CS_All2p1AndOnly1p1_MX-1800_MY-800_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/base.root","para_SI_impact.txt","clean")' -b -q
./plot_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./plot_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

fitdir=$base_dir/withfloor_CS_All2p1AndOnly1p1_MX-3500_MY-800_workspace/SignalMC_XHY4b_area/
root 'load_parameters.C("'$fitdir'/base.root","para_SI_impact.txt","clean")' -b -q
./plot_impact.sh --fitdir $fitdir -r 1 -l --paras para_SI_impact.txt 
./plot_impact.sh --fitdir $fitdir -r 0 -l --paras para_SI_impact.txt 

