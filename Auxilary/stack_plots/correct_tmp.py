import pickle
save_name = "pkls/nPV_2p1_TH.pkl" 

with open(save_name, "rb") as f:
    hist_old = pickle.load( f)
hist = hist_old.copy()
hist["PU"] = hist_old["noPU"].copy()
hist["noPU"] = hist_old["PU"].copy()
with open(save_name, "wb") as f:
    pickle.dump(hist, f)

