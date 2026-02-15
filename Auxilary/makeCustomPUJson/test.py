import ROOT
from TIMBER.Analyzer import Correction, CutGroup, ModuleWorker, analyzer, Node
import TIMBER.Tools.AutoPU_correctionlib as AutoPU

ana = analyzer("ttbar.root")
for name in ana.DataFrame.GetColumnNames():
    print(str(name))
AutoPU.AutoPU(ana, "2024_Summer24")
ana.MakeWeightCols(name = "All")
ana.Snapshot([], "output_ttbar.root", "Events")
