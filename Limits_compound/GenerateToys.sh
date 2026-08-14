#fitdir=Validation_Only2p1_workspace/SignalMC_XHY4b_0x0_area/
#root 'load_parameters.C("'$fitdir'/higgsCombineSnapshot.MultiDimFit.mH125.root","para_SI.txt")' -b -q
#./run_generateOnly.sh --fitdir $fitdir -b  --paras para_SI.txt -l --numtoys 1000 -r 0
#exit
#fitdir=CV_All1p1AndOnly2p1_workspace/SignalMC_XHY4b_area/
#root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI.txt")' -b -q
#./run_generateOnly.sh --fitdir $fitdir -b  --paras para_SI.txt -l --numtoys 1000 -r 0
#./run_generateOnly.sh --fitdir $fitdir -b  --paras para_SI.txt -l --numtoys 1000 -r 3
fitdir=$1
seed=$2
numtoys=20
echo ./run_generateOnly.sh --fitdir $fitdir -b  --paras para_SI.txt -l --numtoys $numtoys -r 0 --seed $seed     
root 'load_parameters.C("'$fitdir'/higgsCombine.AsymptoticLimits.mH125.123456.root","para_SI.txt")' -b -q
./run_generateOnly.sh --fitdir $fitdir -b  --paras para_SI.txt -l --numtoys $numtoys -r 0 --seed $seed
./run_generateOnly.sh --fitdir $fitdir -b  --paras para_SI.txt -l --numtoys $numtoys -r 1 --seed $seed
