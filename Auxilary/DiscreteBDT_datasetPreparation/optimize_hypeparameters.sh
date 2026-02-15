NTreeses=(300 3000)
MinNodeSizes=(1% 10%)
Shrinkages=(0.01 0.2) 
BaggedSampleFractions=(0.4 0.8) 
nCutses=(20 200) 
MaxDepthes=(2 5) 

NTreeses=(500 1500)
MinNodeSizes=(2% 5%)
Shrinkages=(0.03 0.1)
BaggedSampleFractions=(0.5 0.7)
nCutses=(50 100)
MaxDepthes=(3 4)

NTreeses=(500 1500)
MinNodeSizes=(2 5)
Shrinkages=(0.03 0.1)
BaggedSampleFractions=(0.5 0.7)
nCutses=(50 100)
MaxDepthes=(3 4)

S_NTreeses='{'
S_MinNodeSizes='{'
S_Shrinkages='{'
S_BaggedSampleFractions='{'
S_nCutses='{'
S_MaxDepthes='{'

RANDOM=1234

N=2
for ((i=0; i<N; i++)); do
    echo "Iteration $i"
    I=$((RANDOM % ${#NTreeses[@]} ))
    NTrees=${NTreeses[$I]}

    I=$((RANDOM % ${#MinNodeSizes[@]} ))
    MinNodeSize=${MinNodeSizes[$I]}

    I=$((RANDOM % ${#Shrinkages[@]} ))
    Shrinkage=${Shrinkages[$I]}

    I=$((RANDOM % ${#BaggedSampleFractions[@]} ))
    BaggedSampleFraction=${BaggedSampleFractions[$I]}

    I=$((RANDOM % ${#nCutses[@]} ))
    nCuts=${nCutses[$I]}

    I=$((RANDOM % ${#MaxDepthes[@]} ))
    MaxDepth=${MaxDepthes[$I]}
    S_NTreeses=$S_NTreeses$NTrees,
    S_MinNodeSizes=$S_MinNodeSizes$MinNodeSize,
    S_Shrinkages=$S_Shrinkages$Shrinkage,
    S_BaggedSampleFractions=$S_BaggedSampleFractions$BaggedSampleFraction,
    S_nCutses=$S_nCutses$nCuts,
    S_MaxDepthes=$S_MaxDepthes$MaxDepth,

    #config="!H:!V:NTrees=$NTrees:MinNodeSize=$MinNodeSize:BoostType=Grad:Shrinkage=$Shrinkage:UseBaggedBoost:BaggedSampleFraction=$BaggedSampleFraction:nCuts=$nCuts:MaxDepth=$MaxDepth"
    #echo $config
    #root -b -q 'BDT_Trainer_discrete_paraTuning.C("2p1", "1600", "500", "'$config'")'
done
S_NTreeses=${S_NTreeses%?}'}'
S_MinNodeSizes=${S_MinNodeSizes%?}'}'
S_Shrinkages=${S_Shrinkages%?}'}'
S_BaggedSampleFractions=${S_BaggedSampleFractions%?}'}'
S_nCutses=${S_nCutses%?}'}'
S_MaxDepthes=${S_MaxDepthes%?}'}'

root -b -q 'BDT_Trainer_discrete_paraTuning.C("2p1", "1600", "500", '$S_NTreeses,$S_MinNodeSizes,$S_Shrinkages,$S_BaggedSampleFractions,$S_nCutses,$S_MaxDepthes')'

