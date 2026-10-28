#root -l -b -q   'save_clean_workspace.C("SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/higgsCombine.AsymptoticLimits.mH125.123456.root","workspace_clean.root")'
#root -l -b -q   'save_clean_workspace.C("SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/higgsCombiner_0.MultiDimFit.mH125.58.root","workspace_clean.root")'
#root -l -b -q   'save_clean_workspace.C("SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/higgsCombine100xr_1.GenerateOnly.mH125.58.root","workspace_clean.root")'
#PostFit2DShapesFromWorkspace  -w workspace_clean.root --output shapes_clean.root
#python plot_workspace.py --prefit --tf 0x1 --pass_name _CR_SR1_1p1_Region0 --fail_name _CR_SB1_1p1_Region0 --title_extra test --method 1 --do_sig
python plot_workspace.py --prefit --tf 0x2 --pass_name _SR_SR1_1p1_Region0 --fail_name _SR_SB1_1p1_Region0 --title_extra test --method 1 --do_sig
#python plot_workspace.py --prefit --tf 0x1 --pass_name _SR_SR1_2p1_Region0 --fail_name _SR_SB1_2p1_Region0 --title_extra test --method 1 --do_sig
