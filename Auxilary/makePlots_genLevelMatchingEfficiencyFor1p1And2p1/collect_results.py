import glob

files = glob.glob("*.log")

print(files)
massXs = []
massYs = []
effs = {"1p0": [], "2p0": [], "0p2": [], "0p1": [] , "1p1": [], "2p1": [], "1p2": [], "2p2": []}
for _file in files:
    if "condor" in _file or "FAILED" in _file:
        continue
    print(_file)
    mass = _file.partition("__")[0]
    mx = mass.partition("_")[0]
    my = mass.partition("_")[2]
    massXs.append(mx)
    massYs.append(my)
    with open(_file, "r") as f:
        lines = f.readlines()
        shift = 0
        if "in" in lines[-1]:
            shift = 1
        effs["1p0"].append(lines[-8- shift].strip().split()[1])
        effs["2p0"].append(lines[-7- shift].strip().split()[1])
        effs["0p2"].append(lines[-6- shift].strip().split()[1])
        effs["0p1"].append(lines[-5 - shift].strip().split()[1])
        effs["1p1"].append(lines[-4 - shift].strip().split()[1])
        effs["2p1"].append(lines[-3- shift].strip().split()[1])
        effs["1p2"].append(lines[-2 - shift].strip().split()[1])
        effs["2p2"].append(lines[-1 - shift].strip().split()[1])
with open ("matching_eff_withPNet.txt", "w") as f:
    for i in range(len(massXs)):
        f.write(f"{massXs[i]} {massYs[i]} {effs['1p0'][i]} {effs['2p0'][i]} {effs['0p2'][i]} {effs['0p1'][i]} {effs['1p1'][i]} {effs['2p1'][i]} {effs['1p2'][i]} {effs['2p2'][i]}\n") 
