#!/bin/bash 

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
r=0
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
echo '--------------------------------------------------------'

#################################################################################
# Setting some variables
#################################################################################
#fitDir='test_workspace/SignalMC_XHY4b_1x1_area'
cwd=`pwd` # current working directory
card="card.txt"
wsm="workspace_masked.root" # Workspace with channel masks
echo $para1 $para2
parameters="--setParameters "
IFS=';' read -ra _paras <<< "$paras"

for para in "${_paras[@]}"; do
    echo $para
    while IFS= read -r line; do
        if [[ $line == *"QCD_Rc_SR"* || $line == *"QCD_Rc_CR"* ]]; then
            echo 1
            read var_name var_value <<< "$line"
            parameters=$parameters"$var_name=$var_value,"
            #if [[ $line == *"QCD_Rc_SR"* ]]; then
            #    parameters=$parameters"$var_name=$var_value,"
            #else
            #    parameters=$parameters"$var_name=1,"
            #fi
        fi
    done < $para
done

parameters="$parameters"r"="$r
parameters="${parameters//VR/SR}"

echo $parameters
card=card.txt
wsm=card.root
if [ $limits = 1 ]; then 
    printf "cd $fitDir \n"
    cd $fitDir
    rm $wsm
    (set -x; text2workspace.py $card --channel-masks -o $wsm)
    #(set -x; combine -M FitDiagnostics -d $wsm -D higgsCombiner_"$r".GenerateOnly.mH125.$seed.root:toys/toy_1 -m 125 -n "r_$r" -v $verbosity $parameters --saveWorkspace --rMin "-20" --rMax 20 --bypassFrequentistFit -s $seed  --floatParameters r   --justFit --toysFrequentist --cminDefaultMinimizerTolerance $tol --trackErrors r --trackParameters r --skipBOnly -t 20 )
    (set -x; combine -M FitDiagnostics -d $wsm -D higgsCombiner_"$r".GenerateOnly.mH125.1.root:toys/toy_$seed -m 125 -n "r_$r" -v 3 $parameters --saveWorkspace --rMin "-20" --rMax 20 -s $seed  --floatParameters r   --justFit  --cminDefaultMinimizerTolerance $tol --trackErrors r --trackParameters r --X-rtd MINIMIZER_MaxCalls=40000000000 --skipBOnly --cminPreScan --cminPoiOnlyFit --cminPreFit 1  --robustFit 1 )
    #echo combine -M MultiDimFit -d $wsm -t 2 -n "r_$r" --toysFile higgsCombine"r_$r".GenerateOnly.mH125.$seed.root --algo singles --toysFrequentist --rMin -20 --rMax 20 -s $seed -m 125 -v 3
    #combine -M MultiDimFit -d $wsm -t 20 -n "r_$r" --toysFile higgsCombine"r_$r".GenerateOnly.mH125.$seed.root --algo singles --toysFrequentist --rMin -20 --rMax 20 -s $seed -m 125 -v 3 --X-rtd MINIMIZER_MaxCalls=40000000000 $parameters 
    printf "cd $cwd \n"
    cd $cwd
fi
