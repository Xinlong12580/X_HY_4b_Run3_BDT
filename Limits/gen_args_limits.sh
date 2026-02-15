> limits_args.txt
while IFS= read -r line; do
    #echo $line SB1 SR1 SB1 SR1 1p1 >> limits_args.txt
    echo $line SB1 SR1 SB1 SR1 2p1 >> limits_args.txt
done < ../raw_nano/GoodMassPoints.txt
