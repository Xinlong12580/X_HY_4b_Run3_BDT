mx=$1
my=$2
templates=$(ls Templates/*)
for template in $templates; do
    if [[ $template == *"MCstat"* || $template == *"rebinned"* ]]; then
        continue
    fi
    echo $template
    python hist_preprosessing_withfloor.py -f $template --mx $mx --my $my
    python hist_rebinning_withfloor.py -f $template --mx $mx --my $my --year Allyears --recreate
    python hist_rebinning_withfloor.py -f $template --mx $mx --my $my --year 2022
    python hist_rebinning_withfloor.py -f $template --mx $mx --my $my --year 2022EE
    python hist_rebinning_withfloor.py -f $template --mx $mx --my $my --year 2023
    python hist_rebinning_withfloor.py -f $template --mx $mx --my $my --year 2023BPix
    python hist_rebinning_withfloor.py -f $template --mx $mx --my $my --year 2024
done
