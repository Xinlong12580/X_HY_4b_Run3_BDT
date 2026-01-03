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
verbosity=3

options=$(getopt -o "bl" --long "bfit,limits,seed:,numtoys:,fitdir:,fitdir;,strat:,verbosity:" -- "$@")
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
        --fitdir)
            echo test
            shift
            fitDir=$1
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

#################################################################################
# Running the script
#################################################################################

parameters="--setParameters "
while IFS= read -r line; do
    if [[ $line == *"QCD_Rc"* ]]; then
        echo 1
        read var_name var_value <<< "$line"
        parameters=$parameters"$var_name=$var_value,"

    fi
done < control_parameters.txt
parameters=$parameters"r=0,"
echo $parameters
parameters=${parameters%?}
# First, we use MultiDimFit to perform the background-only fit. In this case, the signal strength is explicitly set to zero and we obtain the best-fit parameter values for the background-only hypothesis (assuming zero signal). We can then use these values to generate toys for the blinded limits. 
card=card.txt
wsm=card.root
strat=1
if [ $bfit = 1 ]; then 
    printf "cd $fitDir \n"
    cd $fitDir

    # Check to see if the workspace with channel masks exists
    if [ ! -f "$wsm" ]; then 
        printf "RooWorkspace with channel masks does not exist, creating it now...\n"
        #(set -x; text2workspace.py $card --channel-masks -o $wsm)
        (set -x; text2workspace.py $card -o $wsm)
    fi
    echo "Performing blinded background-only fit"
    (set -x; combine -D data_obs -M GoodnessOfFit --algo saturated --saveWorkspace -m 125 -d $wsm -v $verbosity --cminDefaultMinimizerStrategy $strat --cminDefaultMinimizerTolerance $tol --X-rtd MINIMIZER_MaxCalls=400000 --setParameters "r=0" --freezeParameters "r" -n Snapshot --toysFrequentist -t 2 --saveToys)
    (set -x; combine -D data_obs -M GoodnessOfFit --algo saturated --saveWorkspace -m 125 -d $wsm -v $verbosity --cminDefaultMinimizerStrategy $strat --cminDefaultMinimizerTolerance $tol --X-rtd MINIMIZER_MaxCalls=400000 --setParameters "r=0" --freezeParameters "r" -n Snapshot)
    #(set -x; combine -D data_obs -M GoodnessOfFit --algo saturated --saveWorkspace -m 125 -d $wsm -v $verbosity --cminDefaultMinimizerStrategy $strat --cminDefaultMinimizerTolerance $tol --X-rtd MINIMIZER_MaxCalls=400000 --setParameters "r=0" --freezeParameters "r" -n Snapshot -t 2 --saveToys)
    #(set -x; combine -D data_obs -M GoodnessOfFit --algo saturated --saveWorkspace -m 125 -d $wsm -v $verbosity --cminDefaultMinimizerStrategy $strat --cminDefaultMinimizerTolerance $tol --X-rtd MINIMIZER_MaxCalls=400000 $parameters --freezeParameters "r" -n Snapshot -t 2 --saveToys --toysFrequentist)

    printf "cd $cwd \n"
    cd $cwd
fi
