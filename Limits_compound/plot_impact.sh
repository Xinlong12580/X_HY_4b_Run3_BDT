combineTool.py -M Impacts -d card.root -m 125 --freezeParameters MH -n .impacts --setParameterRanges r=-1,1 -o impacts.json
plotImpacts.py -i impacts.json -o impacts
