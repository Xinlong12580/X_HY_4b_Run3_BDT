import ROOT
import TIMBER
flavors = [0, 4, 5]
wps = [0, 1, 2, 3, 4, 5]
pts = [0, 200, 500]
absetas = [0, 2, 5]
N_all = {}
N_tagged = {}
for flavor in flavors:
    N_all[flavor] = {}
    N_tagged[flavor] = {}
    for wp in wps:
        N_all[flavor][wp] = {}
        N_tagged[flavor][wp] = {}
        for pt in pts:
            N_all[flavor][wp][pt] = {}
            N_tagged[flavor][wp][pt] = {}
            for abseta in absetas:
                N_all[flavor][wp][pt][abseta] = 0
                N_tagged[flavor][wp][pt][abseta] = 0

f = ROOT.TFile.Open(f_name, "READ")
tree = f.Get("Events")
for entry in trees:
    Jet_etas = entry.Jet_eta
    Jet_pts = entry.Jet_pt
    Jet_flavors = entry.Jet_flavor
    Jet_score_discretes = entry.score_discrete
    for i in range(len(Jet_etas)):
        jet_flavor = Jet_flavors[i]
        jet_score_discrete = Jet_score_discretes[i]
        jet_abseta = abs(Jet_etas[i])
        jet_pt = jet_pts[i]
        for _abseta_l in absetas:
            if jet_abseta > _abseta_l:
                abseta_l = _abseta_l
                break
        for _pt_l in pts:
            if jet_pt > _pt_l:
                pt_l = _pt_l
                break
        for wp in wps:
            if wp <= jet_score_discrete:
                tagged = 1
            else 
                tagged = 0
            N_all[jet_flavor][wp][pt_l][abseta_l] += 1
            N_tagged[jet_flavor][wp][pt_l][abseta_l] += tagged
            
for 
            
eff = {}
for flavor in flavors:
    eff[flavor] = {}
    for wp in wps:
        eff[flavor][wp] = {}
        for pt in pts:
            eff[flavor][wp][pt] = {}
            for abseta in absetas:
                eff[flavor][wp][pt][abseta] = N_tagged[flavor][wp][pt][abseta]/ N_all[flavor][wp][pt][abseta]
print(eff)
