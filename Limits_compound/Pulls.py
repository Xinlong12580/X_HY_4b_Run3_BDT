from TwoDAlphabet.helpers import execute_cmd
import os, ROOT

vtol=0.3
stol=0.1
vtol2=2.0
stol2=0.5
regex='^(?!.*(_bin_|_par)|.*mcstat|.*MCstat)'

diffnuis_cmd = f"python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py fitDiagnosticsTest.root --abs -g nuisance_pulls.root --vtol={vtol} --stol={stol} --vtol2={vtol2} --stol2={stol2} --all --regex='{regex}'"

execute_cmd(diffnuis_cmd)

# Make a PDF of the nuisance_pulls.root
if os.path.exists('nuisance_pulls.root'):
    nuis_file = ROOT.TFile.Open('nuisance_pulls.root')
    nuis_can = nuis_file.Get('nuisances')
    nuis_can.SetCanvasSize(nuis_can.GetWw(), int(4 * nuis_can.GetWh()))
    nuis_can.SetBottomMargin(0.3)
    nuis_can.Modified()
    nuis_can.Update()
    nuis_can.Print('nuisance_pulls.png','png')
    nuis_file.Close()
