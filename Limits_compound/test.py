hname = "Allyears__MC_TTBarJets_VR_SB1_1p1_FULL_MCstat_VR_SR1_1p1_0_2Up"
this_rname = "VR_SB1_1p1"
start_idx = hname.index(this_rname)+len(this_rname)+1 #+1 for the trailing underscore
end_idx = hname.index('_',start_idx)
print("TEST2", start_idx, end_idx)
out = hname[start_idx:end_idx]
print(out)
