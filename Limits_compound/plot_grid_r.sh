#!/usr/bin/env bash

# Run and plot a one-dimensional profile-likelihood scan of the signal
# strength r for toys produced by Combine GenerateOnly.

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
#default_fit_dir="$script_dir/SignalInjection/CS_All1p1AndOnly2p1_MX-1800_MY-200_workspace/SignalMC_XHY4b_area"
default_fit_dir="$script_dir/SignalInjection/CS_All1p1AndOnly2p1_MX-3500_MY-200_workspace/SignalMC_XHY4b_area/"

fit_dir="$default_fit_dir"
workspace="card.root"
#toys_file="higgsCombiner_0.GenerateOnly.mH125.51.root"
toys_file="higgsCombiner_0.GenerateOnly.mH125.58.root"
mode="profile"
points=101
r_min=-10
r_max=10
seed=58
mass=125
num_toys=1
name_suffix=""
verbosity=1
set_parameters=""
freeze_parameters=""
parameter_file="$script_dir/para_SI.txt"
name=""
output_dir="grid_r_scan"
plot_script=""
dry_run=0

usage() {
    cat <<'EOF'
Usage: ./plot_grid_r.sh [options]

Modes:
  --mode profile            Profile all nuisance parameters at every r point
                            (default).
  --mode fixed              Freeze all workspace parameters except r. The
                            script excludes observables, global observables,
                            derived expected yields, and channel masks.

Inputs and scan options:
  --fit-dir DIR             Directory containing workspace and toys.
  --workspace FILE          Workspace path, relative to fit-dir unless absolute.
  --toys-file FILE          GenerateOnly ROOT file, likewise relative to fit-dir.
  --points N                Number of grid points (default: 101).
  --r-min X                 Lower scan boundary (default: -10).
  --r-max X                 Upper scan boundary (default: 10).
  --num-toys N              Number of toys read from the file (default: 1).
  --seed N                  Combine seed/output suffix (default: 51).
  --mass X                  Higgs mass argument (default: 125).
  -v, --verbosity N         Combine verbosity (default: 1).

Parameter controls:
  --set-parameters LIST     Comma-separated name=value assignments. Use this to
                            reproduce the parameters used to generate the toys.
  --parameter-file FILE     Two-column "name value" file (default:
                            parameters_SI.txt). As in run_signal_injection.sh,
                            only QCD_Rc_SR* and QCD_Rc_CR* values are passed to
                            --setParameters. Later --set-parameters values win.
  --freeze-parameters LIST  Extra comma-separated parameters to freeze in either
                            mode. In fixed mode these are added to the automatic
                            list.

Output controls:
  --output-dir DIR          Output directory (default: grid_r_scan).
  --name NAME               Combine name suffix (automatic by default).
  --plot-script FILE        Explicit CombinedLimit plot1DScan.py path.
  --dry-run                 Print commands without executing them.
  -h, --help                Show this help.

Examples:
  ./plot_grid_r.sh --mode profile --set-parameters r=0

  ./plot_grid_r.sh --mode fixed \
      --parameter-file parameters/my_postfit_parameters.txt \
      --set-parameters r=0

Notes:
  * The generated curve is 2*deltaNLL versus r.
  * Scanning multiple toys produces multiple curves in one ROOT tree; the
    standard plot1DScan.py is most useful with the default --num-toys 1.
EOF
}

options=$(getopt -o hv: --long help,fit-dir:,workspace:,name_suffix:,toy_index:,toys-file:,mode:,points:,r-min:,r-max:,seed:,mass:,num-toys:,verbosity:,set-parameters:,parameter-file:,freeze-parameters:,output-dir:,name:,plot-script:,dry-run -- "$@") || {
    usage >&2
    exit 2
}
eval set -- "$options"
while true; do
    case "$1" in
        --fit-dir) shift; fit_dir=$1 ;;
        --workspace) shift; workspace=$1 ;;
        --toys-file) shift; toys_file=$1 ;;
        --mode) shift; mode=$1 ;;
        --points) shift; points=$1 ;;
        --r-min) shift; r_min=$1 ;;
        --r-max) shift; r_max=$1 ;;
        --seed) shift; seed=$1 ;;
        --mass) shift; mass=$1 ;;
        --name_suffix) shift; name_suffix=$1 ;;
        --toy_index) shift; toy_index=$1 ;;
        --num-toys) shift; num_toys=$1 ;;
        -v|--verbosity) shift; verbosity=$1 ;;
        --set-parameters) shift; set_parameters=$1 ;;
        --parameter-file) shift; parameter_file=$1 ;;
        --freeze-parameters) shift; freeze_parameters=$1 ;;
        --output-dir) shift; output_dir=$1 ;;
        --name) shift; name=$1 ;;
        --plot-script) shift; plot_script=$1 ;;
        --dry-run) dry_run=1 ;;
        -h|--help) usage; exit 0 ;;
        --) shift; break ;;
        *) echo "Internal option parsing error: $1" >&2; exit 2 ;;
    esac
    shift
done

if [[ $mode != profile && $mode != fixed ]]; then
    echo "ERROR: --mode must be 'profile' or 'fixed'." >&2
    exit 2
fi
if ! [[ $points =~ ^[1-9][0-9]*$ && $num_toys =~ ^[1-9][0-9]*$ ]]; then
    echo "ERROR: --points and --num-toys must be positive integers." >&2
    exit 2
fi

[[ $fit_dir = /* ]] || fit_dir="$script_dir/$fit_dir"
[[ $workspace = /* ]] || workspace="$fit_dir/$workspace"
[[ $toys_file = /* ]] || toys_file="$fit_dir/$toys_file"
[[ $output_dir = /* ]] || output_dir="$script_dir/$output_dir"
if [[ -n $parameter_file && $parameter_file != /* ]]; then
    parameter_file="$script_dir/$parameter_file"
fi

for input in "$workspace" "$toys_file"; do
    [[ -f $input ]] || { echo "ERROR: input not found: $input" >&2; exit 1; }
done
if [[ -n $parameter_file && ! -f $parameter_file ]]; then
    echo "ERROR: parameter file not found: $parameter_file" >&2
    exit 1
fi
command -v combine >/dev/null 2>&1 || {
    echo "ERROR: combine is not available. Enter the CMSSW environment first." >&2
    exit 1
}

mkdir -p "$output_dir"
tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/grid-r-scan.XXXXXX")
trap 'rm -rf -- "$tmp_dir"' EXIT

# Match run_signal_injection.sh: read the parameter file but set only the QCD Rc
# function parameters. Other parameter values in the file must not be passed to
# --setParameters.
file_set=""
if [[ -n $parameter_file ]]; then
    while read -r par val _; do
        [[ -z ${par:-} || $par == \#* || -z ${val:-} ]] && continue
        [[ $val =~ ^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)([eE][-+]?[0-9]+)?$ ]] || continue
        case "$par" in
            QCD_Rc_SR*|QCD_Rc_CR*) file_set+="${file_set:+,}${par}=${val}" ;;
        esac
    done < "$parameter_file"
fi

# In fixed mode, construct the same type of freeze list as
# run_signal_injection.sh from all workspace variables. Parameter values still
# come only from the QCD Rc entries above; the other variables are frozen at
# their values in card.root.
file_freeze=""
if [[ $mode == fixed ]]; then
    command -v root >/dev/null 2>&1 || {
        echo "ERROR: ROOT is required to construct the fixed-parameter list." >&2
        exit 1
    }
    auto_parameters="$tmp_dir/workspace_parameters.txt"
    root -l -b -q "$script_dir/load_parameters.C(\"$workspace\",\"$auto_parameters\",\"__use_current_workspace_values__\")" \
        >"$tmp_dir/load_parameters.log" 2>&1
    while read -r par val _; do
        [[ -z ${par:-} || -z ${val:-} ]] && continue
        case "$par" in
            #r|M_JY_*|M_JJ_*|*_In|n_exp_bin_*|mask_*|lumi) continue ;;
            r|M_JY_*|M_JJ_*|*_In|n_exp_bin_*|mask_*) continue ;;
            *) file_freeze+="${file_freeze:+,}${par}" ;;
        esac
    done < "$auto_parameters"
fi

combined_set="$file_set"
[[ -n $set_parameters ]] && combined_set+="${combined_set:+,}${set_parameters}"
combined_freeze=""
[[ $mode == fixed ]] && combined_freeze=$file_freeze
[[ -n $freeze_parameters ]] && combined_freeze+="${combined_freeze:+,}${freeze_parameters}"

if [[ -z $name ]]; then
    name="GridR_${mode}_seed${seed}_toy${toy_index}_${name_suffix}"
fi
[[ $name == _* ]] || name="_$name"
 masked_channels=(
    CR_SR1_1p1_Region0
    CR_SB1_1p1_Region0
    SR_SB1_1p1_Region0
    SR_SR1_2p1_Region0
    SR_SB1_2p1_Region0
  )

 #masked_channels=(
 #   SR_SR1_1p1_Region0
#)
mask_values=""
mask_names=""
for channel in "${masked_channels[@]}"; do
    mask_values+="mask__${channel}=1,"
    mask_names+="mask__${channel},"
done

mask_values="${mask_values%,}"
mask_names="${mask_names%,}"

combine_cmd=(
  combine -M MultiDimFit -d "$workspace"
   -D "${toys_file}:toys/toy_${toy_index}"
  --algo grid --points "$points"
  -P r --redefineSignalPOIs r
  --setParameterRanges "r=${r_min},${r_max}"
  -m "$mass" -s "$seed" -n "$name" -v "$verbosity"
  --saveNLL
)

#combine_cmd=(
#    combine -M MultiDimFit -d "$workspace"
#    -t "$num_toys" --toysFile "$toys_file"
#    --algo grid --points "$points"
#    -P r --redefineSignalPOIs r
#    --setParameterRanges "r=${r_min},${r_max}"
#    -m "$mass" -s "$seed" -n "$name" -v "$verbosity"
#    --saveNLL
#)
frozen_parameters="$mask_names"
set_parameters="$mask_values"

[[ -n $combined_set ]] &&
    set_parameters+="${set_parameters:+,}${combined_set}"

[[ -n $combined_freeze ]] &&
    frozen_parameters+="${frozen_parameters:+,}${combined_freeze}"

combine_cmd+=(--setParameters "$set_parameters")
combine_cmd+=(--freezeParameters "$frozen_parameters")

printf 'Mode: %s\nWorkspace: %s\nToys: %s\nOutput: %s\n' \
    "$mode" "$workspace" "$toys_file" "$output_dir"
printf 'Command:'
printf ' %q' "${combine_cmd[@]}"
printf '\n'

if (( dry_run )); then
    exit 0
fi
(
    cd "$output_dir"
    "${combine_cmd[@]}" 2>&1 | tee "combine${name}.log"
)

scan_root="$output_dir/higgsCombine${name}.MultiDimFit.mH${mass}.${seed}.root"
[[ -f $scan_root ]] || {
    echo "ERROR: expected scan output was not produced: $scan_root" >&2
    exit 1
}

if [[ -z $plot_script ]]; then
    plot_script="$script_dir/plot_scan_only.py"
fi
[[ -f $plot_script ]] || {
    echo "ERROR: scan plotting script was not found: $plot_script" >&2
    exit 1
}

plot_base="r_scan_${mode}_seed${seed}_toy${toy_index}_${name_suffix}"
(
    cd "$output_dir"
    python "$plot_script" "$(basename -- "$scan_root")" \
        --poi r --output "$plot_base" --y-max 100 --y-cut 100
)

echo "Scan ROOT file: $scan_root"
echo "Plot: $output_dir/${plot_base}.pdf"
echo "Plot: $output_dir/${plot_base}.png"
