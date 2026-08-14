mx=$1
my=$2
templates=$(ls Templates/*)
for template in $templates; do
    if [[ $template == *"MCstat"* || $template == *"rebinned"* ]]; then
        continue
    fi
    echo $template
    python hist_preprosessing.py -f $template --mx $mx --my $my
done
