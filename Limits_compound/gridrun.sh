#!/bin/bash
export USER=xinlong
root_dir=$(pwd)
OUTTXT="$1"_"$2"_"$3"_"$4"_"${5}"_"${6}"_"$7"_"$8"_"$9"_output.log
OUTTXT="${OUTTXT//\//_}"
echo "OUTTXT" $OUTTXT
echo "Run script starting" | tee $root_dir/$OUTTXT
echo "Running on: `uname -a`" | tee -a $root_dir/$OUTTXT
echo "System software: `cat /etc/redhat-release`" | tee -a $root_dir/$OUTTXT

# Set up pre-compiled CMSSW env
ls | tee -a $root_dir/$OUTTXT
source /cvmfs/cms.cern.ch/cmsset_default.sh
xrdcp root://cmseos.fnal.gov//store/user/$USER/tar_2dalphabet.tgz ./
echo TEST-3 | tee -a $root_dir/$OUTTXT
echo xrdcp root://cmseos.fnal.gov//store/user/$USER/tar_2dalphabet.tgz ./ | tee -a $root_dir/$OUTTXT
pwd | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT
echo TEST-2 | tee -a $root_dir/$OUTTXT

export SCRAM_ARCH=el9_amd64_gcc12
scramv1 project CMSSW CMSSW_14_1_0_pre4
echo "Unpacking compiled CMSSW environment tarball..." | tee -a $root_dir/$OUTTXT
tar -xzvf tar_2dalphabet.tgz | tee -a $root_dir/$OUTTXT
echo TEST-1 | tee -a $root_dir/$OUTTXT
rm tar_2dalphabet.tgz
mkdir tardir 
mv tarball.tgz tardir/ 
cd tardir/
tar -xzvf tarball.tgz | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT
rm tarball.tgz
mkdir ../CMSSW_14_1_0_pre4/src/testdir
cp -r * ../CMSSW_14_1_0_pre4/src/testdir
cd ../CMSSW_14_1_0_pre4/src/
echo TEST0 | tee -a $root_dir/$OUTTXT
pwd | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT
echo TEST1 | tee -a $root_dir/$OUTTXT
 
# CMSREL and virtual env setup
echo 'IN RELEASE' | tee -a $root_dir/$OUTTXT
echo 'scramv1 runtime -sh' | tee -a $root_dir/$OUTTXT
eval `scramv1 runtime -sh` 
echo $CMSSW_BASE "is the CMSSW we have on the local worker node" | tee -a $root_dir/$OUTTXT
pwd | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT
echo 'python3 -m venv twoD-env' | tee -a $root_dir/$OUTTXT
python3 -m venv twoD-env
echo 'source twoD-env/bin/activate' | tee -a $root_dir/$OUTTXT
source twoD-env/bin/activate
ls twoD-env | tee -a $root_dir/$OUTTXT
echo "$(which python3)" | tee -a $root_dir/$OUTTXT
echo $VIRTUAL_ENV is the virtual env | tee -a $root_dir/$OUTTXT
pwd | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT
echo $PYTHONPATH is the python path | tee -a $root_dir/$OUTTXT
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cvmfs/cms.cern.ch/el8_amd64_gcc10/external/boost/1.78.0-0d68c45b1e2660f9d21f29f6d0dbe0a0/lib
#export ROOT_INCLUDE_PATH=$ROOT_INCLUDE_PATH:$(correction config --incdir)
pwd | tee -a $root_dir/$OUTTXT
twod=$(cat twoD-env/lib/python3.9/site-packages/TwoDAlphabet.egg-link)
twod=$(echo $twod)
echo TESTd $twod | tee -a $root_dir/$OUTTXT
ls ${twod[0]} | tee -a $root_dir/$OUTTXT
# xrootd debug & certs
#export XRD_LOGLEVEL=Debug
export X509_CERT_DIR=/cvmfs/grid.cern.ch/etc/grid-security/certificates/

# MAIN FUNCTION
cd testdir
MX=$1
MY=$2
SR_FAIL=$3
SR_PASS=$4
CR_FAIL=$5
CR_PASS=$6
mode=$7
tf="0x0"
mkdir Templates
base_All_mode=${mode#*All}     
base_All_mode=${base_All_mode%%AndOnly*}
base_Only_mode=${mode#*Only}
All_mode=All$base_All_mode
Only_mode=Only$base_Only_mode

while IFS= read -r line; do
    read _Reg _mode _tf <<< "$line"
    if [[ $_Reg == "CR" && $_mode == $All_mode ]]; then
        tf_CR_Allmode=$_tf
    fi
    if [[ $_Reg == "CR" && $_mode == $Only_mode ]]; then
        tf_CR_Onlymode=$_tf
    fi
    if [[ $_Reg == "VR" && $_mode == $All_mode ]]; then
        tf_SR_Allmode=$_tf
    fi
    if [[ $_Reg == "VR" && $_mode == $Only_mode ]]; then
        tf_SR_Onlymode=$_tf
    fi
done < BEST_TF.txt

#################################################################################################
################################PREPARE ALL MDOE#################################################
##################################################################################################

xrdcp -f $root_dir/$OUTTXT root://cmseos.fnal.gov//store/user/$USER/XHY4bRun3_limits_"$mode"_BDT/
 echo ./load_fit_grid.sh $MX $MY $All_mode Signal | tee -a $root_dir/$OUTTXT
./load_fit_grid.sh $MX $MY $All_mode Signal
ls Templates | tee -a $root_dir/$OUTTXT
 echo ./load_fit_grid.sh $MX $MY $All_mode Signal | tee -a $root_dir/$OUTTXT
xrdcp -f $root_dir/$OUTTXT root://cmseos.fnal.gov//store/user/$USER/XHY4bRun3_limits_"$mode"_BDT/
./load_fit_grid.sh $MX $MY $All_mode Control
pwd | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT


ls Templates | tee -a $root_dir/$OUTTXT

tf=$tf_SR_Allmode
xrdcp -f $root_dir/$OUTTXT root://cmseos.fnal.gov//store/user/$USER/XHY4bRun3_limits_"$mode"_BDT/
echo python XYH.py --mode "$base_All_mode" --tf $tf --sig $MX-$MY --r_fail SR_SB1_$base_All_mode --r_pass SR_SR1_$base_All_mode --make --makeCard --wsp Signal_"$All_mode"_MX-"$MX"_MY-"$MY" | tee -a $root_dir/$OUTTXT

./make_json.sh "$All_mode" Signal
python XYH.py --mode "$base_All_mode" --tf $tf --sig $MX-$MY --r_fail SR_SB1_$base_All_mode --r_pass SR_SR1_$base_All_mode --make --makeCard --wsp Signal_"$All_mode"_MX-"$MX"_MY-"$MY" 2>&1 | tee -a $root_dir/$OUTTXT
python modify_card.py --eff_file Templates/Templates_"$All_mode"_Signal_all.root --card_file Signal_"$All_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$All_mode" --fail_name SR_"$All_mode" 2>&1 | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT


tf=$tf_CR_Allmode
echo python XYH.py --mode "$base_All_mode" --tf $tf --sig $MX-$MY --r_fail CR_SB1_$base_All_mode --r_pass CR_SR1_$base_All_mode --make --makeCard --wsp Control_"$All_mode"_MX-"$MX"_MY-"$MY" | tee -a $root_dir/$OUTTXT 
./make_json.sh "$All_mode" Control
python XYH.py --mode "$base_All_mode" --tf $tf --sig $MX-$MY --r_fail CR_SB1_$base_All_mode --r_pass CR_SR1_$base_All_mode --make --makeCard --wsp Control_"$All_mode"_MX-"$MX"_MY-"$MY" 2>&1 | tee -a $root_dir/$OUTTXT
python modify_card.py --eff_file Templates/Templates_"$All_mode"_Control_all.root --card_file Control_"$All_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$All_mode" --fail_name CR_"$All_mode" 2>&1 | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT



#################################################################################################
################################PREPARE ONLY MDOE#################################################
##################################################################################################





xrdcp -f $root_dir/$OUTTXT root://cmseos.fnal.gov//store/user/$USER/XHY4bRun3_limits_"$mode"_BDT/
 echo ./load_fit_grid.sh $MX $MY $Only_mode Signal | tee -a $root_dir/$OUTTXT
./load_fit_grid.sh $MX $MY $Only_mode Signal
ls Templates | tee -a $root_dir/$OUTTXT
 echo ./load_fit_grid.sh $MX $MY $Only_mode Signal | tee -a $root_dir/$OUTTXT
xrdcp -f $root_dir/$OUTTXT root://cmseos.fnal.gov//store/user/$USER/XHY4bRun3_limits_"$mode"_BDT/
./load_fit_grid.sh $MX $MY $Only_mode Control
pwd | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT


ls Templates | tee -a $root_dir/$OUTTXT

tf=$tf_SR_Onlymode
xrdcp -f $root_dir/$OUTTXT root://cmseos.fnal.gov//store/user/$USER/XHY4bRun3_limits_"$mode"_BDT/
echo python XYH.py --mode "$base_Only_mode" --tf $tf --sig $MX-$MY --r_fail SR_SB1_$base_Only_mode --r_pass SR_SR1_$base_Only_mode --make --makeCard --wsp Signal_"$Only_mode"_MX-"$MX"_MY-"$MY" | tee -a $root_dir/$OUTTXT

./make_json.sh "$Only_mode" Signal
python XYH.py --mode "$base_Only_mode" --tf $tf --sig $MX-$MY --r_fail SR_SB1_$base_Only_mode --r_pass SR_SR1_$base_Only_mode --make --makeCard --wsp Signal_"$Only_mode"_MX-"$MX"_MY-"$MY" 2>&1 | tee -a $root_dir/$OUTTXT
python modify_card.py --eff_file Templates/Templates_"$Only_mode"_Signal_all.root --card_file Signal_"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$Only_mode" --fail_name SR_"$Only_mode" 2>&1 | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT


tf=$tf_CR_Onlymode
echo python XYH.py --mode "$base_Only_mode" --tf $tf --sig $MX-$MY --r_fail CR_SB1_$base_Only_mode --r_pass CR_SR1_$base_Only_mode --make --makeCard --wsp Control_"$Only_mode"_MX-"$MX"_MY-"$MY" | tee -a $root_dir/$OUTTXT 
./make_json.sh "$Only_mode" Control
python XYH.py --mode "$base_Only_mode" --tf $tf --sig $MX-$MY --r_fail CR_SB1_$base_Only_mode --r_pass CR_SR1_$base_Only_mode --make --makeCard --wsp Control_"$Only_mode"_MX-"$MX"_MY-"$MY" 2>&1 | tee -a $root_dir/$OUTTXT
python modify_card.py --eff_file Templates/Templates_"$Only_mode"_Control_all.root --card_file Control_"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/card.txt --pass_name "$Only_mode" --fail_name CR_"$Only_mode" 2>&1 | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT











#########################################################################################################
#######################COMBINE AND RUN LIMITS##########################################################
##########################################################################################################



#./combine_channels.sh CS_"$mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_area Signal_"$All_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area SR_"$base_All_mode" Control_"$All_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area CR_"$base_All_mode" Signal_"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area SR_"$base_Only_mode" Control_"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area CR_"$base_Only_mode" 2>&1 | tee -a $root_dir/$OUTTXT
if [[ $All_mode == *"2p1"* ]]; then 
./combine_channels.sh CS_"$mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_area Signal_"$All_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area SR_"$base_All_mode" Signal_"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area SR_"$base_Only_mode" Control_"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area CR_"$base_Only_mode" 2>&1 | tee -a $root_dir/$OUTTXT

paras="parameters/Validation_"$All_mode"_"$tf_SR_Allmode"_control_parameters.txt;parameters/Validation_"$Only_mode"_"$tf_SR_Onlymode"_control_parameters.txt;parameters/Control_"$Only_mode"_"$tf_CR_Onlymode"_control_parameters.txt"        

elif [[ $Only_mode == *"2p1"* ]]; then
./combine_channels.sh CS_"$mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_area Signal_"$All_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area SR_"$base_All_mode" Control_"$All_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area CR_"$base_All_mode" Signal_"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_*_area SR_"$base_Only_mode" 2>&1 | tee -a $root_dir/$OUTTXT
paras="parameters/Validation_"$All_mode"_"$tf_SR_Allmode"_control_parameters.txt;parameters/Validation_"$Only_mode"_"$tf_SR_Onlymode"_control_parameters.txt;parameters/Control_"$All_mode"_"$tf_CR_Allmode"_control_parameters.txt"        
fi


echo "CALCULATING LIMITS ......." | tee -a $root_dir/$OUTTXT
ls | tee -a $root_dir/$OUTTXT
#./run_limits.sh --fitdir CS_"$All_mode"And"$Only_mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_"$tf"_area/ -l -v 2 --mode "$All_mode"And"$Only_mode" 2>&1 | tee -a $root_dir/$OUTTXT
echo $paras | tee -a $root_dir/$OUTTXT
./run_limits.sh --fitdir CS_"$mode"_MX-"$MX"_MY-"$MY"_workspace/SignalMC_XHY4b_area/ -l --paras $paras 2>&1 | tee -a $root_dir/$OUTTXT




status=${PIPESTATUS[0]}
if [ $status -eq 0 ]; then
    rm *root
    rm *txt
    # move all snapshots to the EOS (there will only be one)
    #cp CS*workspace/base.root base_"$MX"_"$MY"_region_"$CR_FAIL"_"$CR_PASS"_"$SR_FAIL"_"$SR_PASS".root
    cp CS*workspace/SignalMC_XHY4b_area/card.txt card_"$MX"_"$MY"_region_"$mode".txt
    cp CS*workspace/SignalMC_XHY4b_area/higgsCombine.AsymptoticLimits.mH125.123456.root higgsCombine.AsymptoticLimits.mH125.123456_"$MX"_"$MY"_region_"$mode".root 
    #cp CS*workspace/SignalMC_XHY4b_"$tf"_area/higgsCombineSnapshot.MultiDimFit.mH125.root higgsCombineSnapshot.MultiDimFit.mH125_"$MX"_"$MY"_region_"$CR_FAIL"_"$CR_PASS"_"$SR_FAIL"_"$SR_PASS".root 
    xrdcp -f *txt *root root://cmseos.fnal.gov//store/user/$USER/XHY4bRun3_limits_"$mode"_BDT/
    tar -cvzf workspace_"$MX"_"$MY"_region_"$CR_FAIL"_"$CR_PASS"_"$SR_FAIL"_"$SR_PASS".tgz CS*workspace
    xrdcp -f *gz root://cmseos.fnal.gov//store/user/$USER/XHY4bRun3_limits_"$mode"_BDT/
    
else
    mv $root_dir/$OUTTXT $root_dir/FAILED_$OUTTXT
    OUTTXT=FAILED_$OUTTXT
fi
ls | tee -a $root_dir/$OUTTXT
#xrdcp -f $root_dir/$OUTTXT root://cmseos.fnal.gov//store/user/$USER/XHY4bRun3_limits_$mode/
