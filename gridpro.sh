work=$1
if [[ $work == skim ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_skim.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_skim/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a skim_args.txt -i "run_skim.py XHY4b_Analyzer.py raw_nano cpp_modules outputList"
fi


if [[ $work == selection_1p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_1p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_1p1_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_selection_1p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == selection_1p1_BDT_debug ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_1p1_BDT_debug.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_1p1_BDT_debug/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_selection_1p1_BDT_debug.py XHY4b_Analyzer.py raw_nano outputList"
fi

if [[ $work == selection_2p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_2p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_2p1_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_selection_2p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == selection_2p1_BDT_Control ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_2p1_BDT_Control.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_2p1_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_selection_2p1_BDT_Control.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == Nminus1_1p1 ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_Nminus1_1p1.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_Nminus1_1p1/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a Nminus1_args.txt -i "cpp_modules run_Nminus1_1p1.py XHY4b_Analyzer.py raw_nano outputList"
fi


if [[ $work == division_1p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_division_1p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_division_1p1_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a division_1p1_BDT_args.txt -i "cpp_modules run_division_1p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi

if [[ $work == division_2p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_division_2p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_division_2p1_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a division_2p1_BDT_args.txt -i "cpp_modules run_division_2p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == selection_2p1 ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_2p1.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_2p1/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_selection_2p1.py XHY4b_Analyzer.py raw_nano outputList"
fi

if [[ $work == Nminus1_2p1 ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_Nminus1_2p1.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_Nminus1_2p1/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a Nminus1_args.txt -i "cpp_modules run_Nminus1_2p1.py XHY4b_Analyzer.py raw_nano outputList"
fi



if [[ $work == selection_combined_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_combined_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_combined_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_selection_combined_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi

if [[ $work == selection_combined_BDT_debug ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_combined_BDT_debug.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_combined_BDT_debug/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_selection_combined_BDT_debug.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == division_combined_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_division_combined_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_division_combined_BDT_experiment4/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a division_combined_BDT_args.txt -i "cpp_modules run_division_combined_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == division_combined_BDT_fast ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_division_combined_BDT_fast.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_division_combined_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a division_combined_BDT_args.txt -i "cpp_modules run_division_combined_BDT_fast.py XHY4b_Analyzer.py raw_nano outputList"
fi

if [[ $work == direct_selection ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_direct_selection.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_direct_selection/#g' -e "s/USER_NAME/$USER/g" gridrun_template_DirectSelection.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a direct_selection_args.txt -i "cpp_modules run_direct_selection.py run_skim.py run_selection_combined_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi


if [[ $work == QCD_selection ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_combined_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_QCD_selection/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a QCD_selection_args.txt -i "cpp_modules run_selection_combined_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi













if [[ $work == skim_a ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_skim.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/tmp/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a amend_skim_args.txt -i "run_skim.py XHY4b_Analyzer.py raw_nano cpp_modules outputList"
fi
if [[ $work == skim_amend ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_skim.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_skim/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a amend_skim_args.txt -i "run_skim.py XHY4b_Analyzer.py raw_nano cpp_modules outputList"
fi
if [[ $work == selection_2p1_debug ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_2p1_debug.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_2p1_debug/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_2p1_debug_args.txt -i "cpp_modules run_selection_2p1_debug.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == mass_debug_2p1 ]] ; then
    
    sed -e 's/PYTHON_SCRIPT/run_mass_debug_2p1.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_mass_debug_2p1/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a mass_debug_2p1_args.txt -i "cpp_modules run_mass_debug_2p1.py XHY4b_Analyzer.py raw_nano outputList"
fi

if [[ $work == selection_1p1_debug ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_1p1_debug.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_1p1_debug/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_1p1_debug_args.txt -i "cpp_modules run_selection_1p1_debug.py XHY4b_Analyzer.py raw_nano outputList"
fi

if [[ $work == trigger_1p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_trigger_1p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_trigger_1p1_BDT_regressedMass/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_trigger_1p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == trigger_2p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_trigger_2p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_trigger_2p1_BDT_regressedMass/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_trigger_2p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == btagging_2p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_btagging_2p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_btagging_2p1_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_btagging_2p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == Xbbtagging_1p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_Xbbtagging_1p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_Xbbtagging_1p1_BDT_regressed/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_Xbbtagging_1p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == Xbbtagging_2p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_Xbbtagging_2p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_Xbbtagging_2p1_BDT_regressed/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_Xbbtagging_2p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi














if [[ $work == skim_a ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_skim.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/tmp/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a amend_skim_args.txt -i "run_skim.py XHY4b_Analyzer.py raw_nano cpp_modules outputList"
fi
if [[ $work == skim_amend ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_skim.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_skim/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a amend_skim_args.txt -i "run_skim.py XHY4b_Analyzer.py raw_nano cpp_modules outputList"
fi
if [[ $work == selection_2p1_debug ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_2p1_debug.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_2p1_debug/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_2p1_debug_args.txt -i "cpp_modules run_selection_2p1_debug.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == mass_debug_2p1 ]] ; then
    
    sed -e 's/PYTHON_SCRIPT/run_mass_debug_2p1.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_mass_debug_2p1/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a mass_debug_2p1_args.txt -i "cpp_modules run_mass_debug_2p1.py XHY4b_Analyzer.py raw_nano outputList"
fi

if [[ $work == selection_1p1_debug ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_selection_1p1_debug.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_selection_1p1_debug/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_1p1_debug_args.txt -i "cpp_modules run_selection_1p1_debug.py XHY4b_Analyzer.py raw_nano outputList"
fi

if [[ $work == btagging_2p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_btagging_2p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_btagging_2p1_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_btagging_2p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == Xbbtagging_1p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_Xbbtagging_1p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_Xbbtagging_1p1_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_Xbbtagging_1p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
if [[ $work == Xbbtagging_2p1_BDT ]] ; then
    sed -e 's/PYTHON_SCRIPT/run_Xbbtagging_2p1_BDT.py/g' -e 's#OUTPUT_DIR#root://cmseos.fnal.gov//store/user/USER_NAME/XHY4bRun3_Xbbtagging_2p1_BDT/#g' -e "s/USER_NAME/$USER/g" gridrun_template.sh > gridrun.sh
    python CondorHelper.py -r gridrun.sh -a selection_args.txt -i "cpp_modules run_Xbbtagging_2p1_BDT.py XHY4b_Analyzer.py raw_nano outputList"
fi
