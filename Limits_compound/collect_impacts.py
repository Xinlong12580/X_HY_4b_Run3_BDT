import ROOT
import os

from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--work_dir', type=str, dest='work_dir',action='store', required=True)
args = parser.parse_args()
nom_file = args.work_dir + "/higgsCombineSnapshot.MultiDimFit.mH125.root"
f_nom = ROOT.TFile.Open(nom_file, "READ")
w_nom = f_nom.Get("w")
w_nom.loadSnapshot("MultiDimFit")
v_nom = w_nom.allVars()
it = v_nom.createIterator()
var = it.Next()
with open(args.work_dir + "/nom_vars.txt", "w") as out_nom_f:
    while var:
        out_nom_f.write(f"{var.GetName()} {var.getVal()}, {var.GetError()}\n")
        print(var.GetName(), var.getVal(), var.GetError())
        var = it.Next()

with open(args.work_dir + "/impact_vars.txt", "w") as out_impact_f:
    for _f in os.listdir(args.work_dir):
        impact_file = os.path.join(args.work_dir, "/" + _f)
        if os.path.isfile(impact_file) and "higgsCombineSnapshot" in impact_file and ".MultiDimFit.mH125.root" in impact_file:
            para = impact_file[impact_file.find("Snapshot") + 8, impact_file.find(".MultiDimFit")] 
            para_name = para[:-2]
            para_vari = para[-1]
            f_impact = ROOT.TFile.Open(impact_file, "READ")
            limits = f_impact.Get("limits")
            for entry in limits:
                r = limits.r
                break
            print(f"{para_name} {para_vari} {r}")
            out_impact_f.write(f"{para_name} {para_vari} {r}\n")
            
            
