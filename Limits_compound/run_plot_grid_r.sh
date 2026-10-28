i=1
while (( i < 21 )); do
    ./plot_grid_r.sh \
          --mode fixed \
          --set-parameters r=0 \
          --r-min -2 \
          --r-max 2 \
          --points 81\
          --toy_index $i\
          --toys-file higgsCombiner_0.GenerateOnly.mH125.58.root
    (( i++ ))
done
