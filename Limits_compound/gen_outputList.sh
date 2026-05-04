division_1p1_dir=/store/user/$USER/XHY4bRun3_division_1p1/
eosls $division_1p1_dir  > outputList/output_division_1p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$division_1p1_dir@" outputList/output_division_1p1_tmp.txt > outputList/output_division_1p1.txt


division_2p1_dir=/store/user/$USER/XHY4bRun3_division_2p1/
eosls $division_2p1_dir > outputList/output_division_2p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$division_2p1_dir@" outputList/output_division_2p1_tmp.txt > outputList/output_division_2p1.txt


dir=/store/user/$USER/XHY4bRun3_limits_1p1/
eosls $dir > outputList/output_limits_1p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$dir@" outputList/output_limits_1p1_tmp.txt > outputList/output_limits_1p1.txt

dir=/store/user/$USER/XHY4bRun3_limits_2p1/
eosls $dir > outputList/output_limits_2p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$dir@" outputList/output_limits_2p1_tmp.txt > outputList/output_limits_2p1.txt

rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_division_1p1_BDT/
eosls $file_dir > outputList/output_selection_1p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_1p1_tmp.txt > outputList/output_division_1p1_BDT.txt

rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_division_combined_BDT/
eosls $file_dir > outputList/output_selection_1p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_1p1_tmp.txt > outputList/output_division_combined_BDT.txt

rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_division_2p1_BDT_hv0/
eosls $file_dir > outputList/output_selection_1p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_1p1_tmp.txt > outputList/output_division_2p1_BDT_hv0.txt
file_dir=/store/user/$USER/XHY4bRun3_division_2p1_BDT_v1/
eosls $file_dir > outputList/output_selection_2p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_2p1_tmp.txt > outputList/output_division_2p1_BDT_v1.txt
rm outputList/*tmp*

rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_division_2p1_BDT_noDDT/
eosls $file_dir > outputList/output_selection_1p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_1p1_tmp.txt > outputList/output_division_2p1_BDT_noDDT.txt
rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_division_2p1_BDT/
eosls $file_dir > outputList/output_selection_1p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_1p1_tmp.txt > outputList/output_division_2p1_BDT.txt

file_dir=/store/user/$USER/XHY4bRun3_limits_1p1_BDT/
eosls $file_dir > outputList/output_selection_1p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_1p1_tmp.txt > outputList/output_limits_1p1_BDT.txt

rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_limits_2p1_BDT/
eosls $file_dir > outputList/output_selection_2p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_2p1_tmp.txt > outputList/output_limits_2p1_BDT.txt
rm outputList/*tmp*

file_dir=/store/user/$USER/XHY4bRun3_limits_2p1_BDT_noDDT/
eosls $file_dir > outputList/output_selection_2p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_2p1_tmp.txt > outputList/output_limits_2p1_BDT_noDDT.txt
rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_limits_2p1_BDT_v0/
eosls $file_dir > outputList/output_selection_2p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_2p1_tmp.txt > outputList/output_limits_2p1_BDT_v0.txt
rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_limits_2p1_BDT_v1/
eosls $file_dir > outputList/output_selection_2p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_2p1_tmp.txt > outputList/output_limits_2p1_BDT_v1.txt
rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_limits_All1p1AndOnly2p1_BDT/
eosls $file_dir > outputList/output_selection_2p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_2p1_tmp.txt > outputList/output_limits_All1p1AndOnly2p1_BDT.txt
rm outputList/*tmp*
file_dir=/store/user/$USER/XHY4bRun3_limits_All2p1AndOnly1p1_BDT/
eosls $file_dir > outputList/output_selection_2p1_tmp.txt
sed "s@^@root://cmseos.fnal.gov/$file_dir@" outputList/output_selection_2p1_tmp.txt > outputList/output_limits_All2p1AndOnly1p1_BDT.txt
rm outputList/*tmp*
