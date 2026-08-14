import json
import gzip

years = ["2022_Summer22", "2022_Summer22EE", "2023_Summer23", "2023_Summer23BPix", "2024_Summer24"]
years = ["2022_Summer22"]
for year in years:
    with gzip.open(f"/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/{year}/jetvetomaps.json.gz", "r") as f:
        jvp = json.load(f)
    with gzip.open(f"/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/{year}/jet_jerc.json.gz", "r") as f:
        jerc = json.load(f)

    for _ in jerc["corrections"]:
        print(_["name"])
    #for corr in jerc["corrections"]:
    #    print(year, corr["name"], corr["version"])
    for corr in jvp["corrections"]:
        print(year, corr["name"], corr["version"])
    for corr in jerc["compound_corrections"]:
        print(year, corr["name"], corr["stack"])
