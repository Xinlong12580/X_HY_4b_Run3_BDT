import ROOT
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-f', type=str, dest='f',action='store', required=True)
parser.add_argument('-r', type=float, dest='r',action='store', required=True)
parser.add_argument('--title', type=str, dest='title',action='store', required=True)
args = parser.parse_args()
with open("outputList/output_SI_BDT.txt", "r") as _f:
    SIs = _f.readlines()
f_string = args.f.replace("/", "_")

rs = []
deltars = []
sigs = []

nom_r = args.r


for SI in SIs:
    if f_string not in SI or "123456" in SI or f"r_{int(nom_r)}." not in SI:
        continue
    print(SI.strip())
    SI = SI.strip()
    f = ROOT.TFile.Open(SI, "READ")
    limit = f.Get("limit")
    if not limit or limit.GetEntries()<4: continue
        
    limit = np.array(ROOT.RDataFrame("limit", SI).AsNumpy()["limit"])
    limitErr = np.array(ROOT.RDataFrame("limit", SI).AsNumpy()["limitErr"])
    print(limit)
    mask = (limit[::4] < 14 ) * (limit[::4] > -14 ) * (limit[1::4] < 14 ) * (limit[1::4] > -14 ) * (limit[2::4] < 14 ) * (limit[2::4] > -14 )
    mask = (limit[::4] < 14 ) * (limit[::4] > -14 )
    print(mask)
    _rs = limit[::4][mask]
    _deltars = _rs - nom_r
    
    _negErrs = _rs - limit[1::4][mask]
    _posErrs = limit[2::4][mask] - _rs
    
    #_negErrs = limitErr[3::4][mask]
    #_posErrs = limitErr[3::4][mask] 
    
    _sigs = _deltars.copy()
    _sigs[_deltars > 0] = (_deltars / _posErrs ) [_deltars > 0]
    _sigs[_deltars <= 0] = (_deltars / _negErrs ) [_deltars <= 0]
    print("rs", _rs)
    print("deltar", nom_r, _deltars)
    print("negErrs", _negErrs)
    print("posErrs", _posErrs)
    print("sigs",_sigs)
    rs = rs + list(_rs)
    deltars = deltars + list(_deltars)
    sigs = sigs + list(_sigs)

    ''' 
    index = 2
    for entry in limit:
        if entry.iToy != index:
            r = entry.limit
            deltar = entry.limitErr
        else:
            if deltar > 0:
                print(index, r, deltar)
                rs.append(r)
                deltars.append(deltar)
                sigs.append((r - nom_r) / deltar)
                index += 1

    '''



fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1, 1, 1)
counts, bin_edges = np.histogram(sigs, bins=np.linspace(-5, 5, 51))

# Compute bin centers
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# Poisson errors
errors = np.sqrt(counts)

ax.errorbar(bin_centers, counts, yerr=errors, fmt='o', capsize=3)
ax.set_title(f"signal injection, $r_0$={nom_r}, {args.title}")
ax.set_xlabel(r"$(r-r_0)/(\delta r)$")
fig.savefig(f"SIs/signal_injection_r_{int(nom_r)}_{args.title}.png")


fig = plt.figure(figsize = (10, 6))
ax = fig.add_subplot(1, 1, 1)
counts, bin_edges = np.histogram(rs, bins=np.linspace(nom_r - 15, nom_r + 15, 401))

# Compute bin centers
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# Poisson errors
errors = np.sqrt(counts)

ax.errorbar(bin_centers, counts, yerr=errors, fmt='o', capsize=3)
ax.set_title(f"signal injection, $r_0$={nom_r}, {args.title}")
ax.set_xlabel("r")
fig.savefig(f"SIs/r_signal_injection_r_{int(nom_r)}_{args.title}.png")

