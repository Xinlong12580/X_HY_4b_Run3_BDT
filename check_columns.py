import ROOT

f_name="Auxilary/makeCustomPUJson/output_ttbar.root"
f_name="root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24NanoAODv15/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/NANOAODSIM/150X_mcRun3_2024_realistic_v2-v2/120000/4b74f791-673b-4b21-be3e-c9287790bc40.root"
f_name="file0.root"
f_namae = "root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv15/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/NANOAODSIM/150X_mcRun3_2022_realistic_v1-v2/2810000/67eb7685-29f5-4475-96a8-f73050db8d05.root" 
f_name="root://cms-xrd-global.cern.ch//store/data/Run2022C/JetMET/NANOAOD/NanoAODv15-v1/140000/95eef86f-e8d8-41d6-b129-dcdb22c92272.root"
rdf= ROOT.RDataFrame("Events", f_name)
for c in rdf.GetColumnNames():
    sc = str(c)
    if "Jet" in sc and "L1" not in sc and "HLT" not in sc:
        print(sc)
f  = ROOT.TFile.Open(f_name, "READ")
events = f.Get("Events")
#events.Scan("Jet_btagUParTAK4B")
events.Scan("nJet")
#events.Scan("FatJet_globalParT3_Xbb")
