import ROOT

rdf = ROOT.RDataFrame("Events", "root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv12/NMSSM_XtoYHto4B_MX-3000_MY-1600_TuneCP5_13p6TeV_madgraph-pythia8/NANOAODSIM/130X_mcRun3_2022_realistic_v5-v2/2820000/1159ad42-de60-439e-af3b-2d180995a1ec.root")
HLTs = []
Effs = []
Ntot = rdf.Count().GetValue()
for c in rdf.GetColumnNames():
    #if "HLT_AK8" not in str(c):
    if "HLT" not in str(c):
        continue
    else:
        print(c)
        continue
    HLTs.append(c)
    eff = rdf.Sum(c).GetValue() / Ntot
    Effs.append(eff)
    print(c, eff)
sorted_Effs_with_index = sorted(enumerate(Effs), key=lambda x: x[1], reverse=True)
sorted_Effs = [x[1] for x in sorted_Effs_with_index]
sorted_indice = [x[0] for x in sorted_Effs_with_index]

print("SORTED: ")
for ind in sorted_indice:
    print(HLTs[ind], Effs[ind])
