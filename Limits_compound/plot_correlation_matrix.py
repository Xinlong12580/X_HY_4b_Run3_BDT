import ROOT
import numpy as np
from argparse import ArgumentParser
import matplotlib.pyplot as plt
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
parser.add_argument('--title', type=str, dest='title',action='store', required=True)
args = parser.parse_args()

f = ROOT.TFile.Open(args.f, "READ")

results = f.Get("fit_mdf")
results.Print()
matrix = results.correlationMatrix()
pars = results.floatParsFinal()
print(matrix.GetNrows(), matrix[1][1])
goodParList = []
goodParIndex = []
for i in range(pars.getSize()):
    p = pars.at(i)
    if "QCD_" in p.GetName() or "TTBAR" in p.GetName():
        continue
    goodParList.append(p.GetName())
    goodParIndex.append(i)
print(goodParList, len(goodParList))
    
mat=np.zeros((len(goodParList), len(goodParList)))
for i in range(len(goodParList)):
    for j in range(len(goodParList)):
        mat[i][j]=matrix[goodParIndex[i]][goodParIndex[j]]
print(mat)
fig, ax = plt.subplots(figsize=(20,20))

im = ax.imshow(mat, cmap='viridis')

ax.set_xticks(np.arange(len(goodParList)))
ax.set_yticks(np.arange(len(goodParList)))

ax.set_xticklabels(goodParList, fontsize=12)
ax.set_yticklabels(goodParList, fontsize=12)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

plt.colorbar(im)

plt.title(args.title, fontsize = 36)
plt.tight_layout()
plt.savefig(f"CMs/{args.title}.png")

