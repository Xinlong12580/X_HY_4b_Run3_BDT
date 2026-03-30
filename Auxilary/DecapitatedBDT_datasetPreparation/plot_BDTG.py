#Author: Beikun Fan
import ROOT
import os
from argparse import ArgumentParser

ROOT.gROOT.SetBatch(True)

parser = ArgumentParser()
parser.add_argument('--mode', dest='mode', required=True)
parser.add_argument('--year', dest='year', required=True)
parser.add_argument('--mx', type=str, dest='mx',action='store', required=True)
parser.add_argument('--my', type=str, dest='my',action='store', required=True)
args = parser.parse_args()

root_file = f"TMVAC_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}_discrete.root"
dataset = f"dataset_MX{args.mx}_MY{args.my}_{args.mode}_{args.year}_discrete"
method = f"BDTG_{args.mode}_{args.year}"

if not os.path.exists(root_file):
    print(f"Error: {root_file} not found!")
    exit(1)

f = ROOT.TFile.Open(root_file, "READ")
dir_path = f"{dataset}/Method_BDT/{method}"
d = f.Get(dir_path)

if not d:
    print(f"Error: Could not find directory {dir_path} in {root_file}")
    exit(1)

# 只提取包含了 99% 数据的 Training Sample
h_train_S = d.Get(f"MVA_{method}_Train_S")
h_train_B = d.Get(f"MVA_{method}_Train_B")

c = ROOT.TCanvas("c", "BDT Output", 800, 600)
c.SetBottomMargin(0.12)
c.SetLeftMargin(0.12)

# 把原来的散点换成漂亮的实心填充直方图
h_train_S.SetLineColor(ROOT.kBlue)
h_train_S.SetLineWidth(2)
h_train_S.SetFillColorAlpha(ROOT.kBlue, 0.4)

h_train_B.SetLineColor(ROOT.kRed)
h_train_B.SetLineWidth(2)
h_train_B.SetFillColorAlpha(ROOT.kRed, 0.4)

# 归一化面积
if h_train_S.Integral() > 0: h_train_S.Scale(1.0/h_train_S.Integral())
if h_train_B.Integral() > 0: h_train_B.Scale(1.0/h_train_B.Integral())

# 设置标题和纵轴最大值
max_y = max(h_train_S.GetMaximum(), h_train_B.GetMaximum())
h_train_S.SetMaximum(max_y * 1.3)
h_train_S.SetTitle(f"BDT Classifier Output (MX {args.mx}GeV MY {args.my}GeV {args.mode} {args.year})")
h_train_S.SetStats(0)

# 坐标轴标签
h_train_S.GetXaxis().SetTitle("BDT Response")
h_train_S.GetXaxis().SetTitleSize(0.045)
h_train_S.GetXaxis().SetTitleOffset(1.1)

h_train_S.GetYaxis().SetTitle("Normalized Arbitrary Units")
h_train_S.GetYaxis().SetTitleSize(0.045)
h_train_S.GetYaxis().SetTitleOffset(1.2)

# 画图 (HIST 表示画成直方图形式)
h_train_S.Draw("HIST")
h_train_B.Draw("HIST SAME")

# 图例 (只保留信号和背景)
leg = ROOT.TLegend(0.65, 0.75, 0.88, 0.88)
leg.AddEntry(h_train_S, "Signal", "F")
leg.AddEntry(h_train_B, "Background", "F")
leg.SetBorderSize(0) # 去掉图例边框，显得更干净
leg.Draw()

# 保存
out_name = f"BDT_Output_{args.mode}_{args.year}.png"
c.SaveAs(out_name)
print(f"Saved: {out_name}")
