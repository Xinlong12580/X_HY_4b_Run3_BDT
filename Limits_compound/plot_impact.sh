#!/bin/bash 
set -euo pipefail
##############################################################################
# Script for running blinded limits
#
# 1) Perform the background-only fit using MultiDimFit
#       - NOTE: we do not use FitDiagnostics, as this runs the S+B fit which we do not want right now
# 2) Obtain expected AsymptoticLimits, using the B-only fit result 
#
# USAGE:
#       ./run_blinded.sh [-bl] [--numtoys XYZ] [--seed XYZ] [--tol X.Y] [--strat X] [--verbosity X]
#
###############################################################################

###############################################################################
# Read options from command line 
###############################################################################
bfit=0
limits=0
seed=42
numtoys=100
tol=0.1         # --cminDefaultMinimizerTolerance
strat=0         # --cminDefaultMinimizerStrategy
verbosity=2

options=$(getopt -o "bv:n:lr:" --long "bfit,limits,seed:,numtoys:,fitdir:,strat:,verbosity:,tol:,r_value:,paras:" -- "$@")
eval set -- "$options"

while true; do
    case "$1" in
        --strat)
            shift
            strat=$1
            ;;
        -v|--verbosity)
            shift
            verbosity=$1
            ;;
        -b|--bfit)
            bfit=1
            ;;
        -l|--limits)
            limits=1
            ;;
        --seed)
            shift
            seed=$1
            ;;
        -n|--numtoys)
            shift
            numtoys=$1
            ;;
        --tol)
            shift
            tol=$1
            ;;
        -r|--r_value)
            shift
            echo test $1
            r=$1
            ;;
        --fitdir)
            shift
            fitDir=$1
            ;;
        --paras)
            shift
            paras=$1
            ;;
        --)
            shift
            break;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
    shift
done

echo '--------------------------------------------------------'
echo Using the following options:
echo seed      = $seed
echo strat     = $strat
echo tol       = $tol 
echo numtoys   = $numtoys
echo verbosity = $verbosity
echo paras = $paras
echo '--------------------------------------------------------'
nps=""
parameters="--setParameters "
IFS=';' read -ra _paras <<< "$paras"

for para in "${_paras[@]}"; do
    while IFS= read -r line; do
        read var_name var_value <<< "$line"
        if [[ $var_name != "r" && $var_name != *"QCD_"* && $var_name != *"_In"* && $var_name != *"n_"* && $var_name != *"mcstat"* && $var_name != *"M_"* && $var_name != *"mask_"* ]]; then
            nps=$nps" "$var_name
        fi
        if [[ $line == *"QCD_Rc_SR"* || $line == *"QCD_Rc_CR"* ]]; then
            parameters=$parameters"$var_name=$var_value,"
        fi
    done < $para
done

cwd=`pwd` # current working directory
card="card.txt"
wsm="base.root" # Workspace with channel masks
parameters="$parameters"r=$r
echo $parameters
echo $nps
if [ $limits = 1 ]; then 
    printf "cd $fitDir \n"
    cd $fitDir

    # Check to see if the workspace with channel masks exists
    printf "cd $cwd \n"
fi

echo $fitDir
np_files=$(ls )
_nps=""
for np in $nps; do
    echo $np
    if [[ $np_files == *.r_${r}_impacts_$np.* ]]; then
        _nps=$_nps$np","
    fi
done
_nps=${_nps%?}
echo combineTool.py -M Impacts -d card.root -m 125 --freezeParameters MH -n .impacts --setParameterRanges r=-1,1 -o impacts.json --named "$_nps"
combineTool.py -M Impacts  -d "$wsm" -m 125 --freezeParameters MH -n .r_"$r"_impacts --seed 123456 --setParameterRanges r=-5,5 -o impacts_r_"$r".json --named "$_nps"
plot_name_base="${fitDir//\//_}"
plotImpacts.py -i impacts_r_"$r".json -o "$plot_name_base"_impacts_r_"$r" --per-page 150
cd $cwd


