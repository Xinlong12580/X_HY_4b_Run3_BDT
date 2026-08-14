mx=$1
my=$2
templates=$(ls Templates/*)
for template in $templates; do
    if [[  $template != *"rebinned"* ]]; then 
    continue 
    fi
    echo $template
    python make_MCstats_templates.py -f $template 
done
