#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  plot_postfit_MXslice.sh FIT_DIR TF PASS_NAME FAIL_NAME MODE DO_LOADING MX_BOUNDARY1 MX_BOUNDARY2 [PLOT_OPTIONS...]

Create three post-fit mY projections in mX slices:
  mX < MX_BOUNDARY1
  MX_BOUNDARY1 <= mX < MX_BOUNDARY2
  mX >= MX_BOUNDARY2

The two boundaries must coincide with mX bin edges in the post-fit TH2s.
Additional options are forwarded to plot_1d_perbin_MXslice.py, for example
--sig or --do_sig.
EOF
}

if (( $# < 8 )); then
    usage >&2
    exit 2
fi

fit_dir_arg=$1
tf=$2
pass_name=$3
fail_name=$4
mode=$5
do_loading=$6
mx_boundary1=$7
mx_boundary2=$8
shift 8
plot_options=("$@")

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

if [[ ! -d $fit_dir_arg ]]; then
    echo "ERROR: fit directory does not exist: $fit_dir_arg" >&2
    exit 2
fi

fit_dir=$(cd -- "$fit_dir_arg" && pwd)
output_dir="$script_dir/plotting/postfit_plots"
mkdir -p -- "$output_dir"

# plot_1d_perbin_MXslice.py imports shared helpers from plot_1d_perbin.py.
# Keep the copies in the fit directory synchronized with plotting/.
cp -- "$script_dir"/plotting/*.py "$fit_dir"/

original_dir=$PWD
trap 'cd -- "$original_dir"' EXIT
cd -- "$fit_dir"

if [[ $do_loading == 1 ]]; then
    PostFit2DShapesFromWorkspace \
        -w higgsCombineSnapshot.MultiDimFit.mH125.root \
        --output postfitshapes_b.root \
        -f multidimfitSnapshot.root:fit_mdf \
        --postfit --samples 100 --print
fi

python plot_1d_perbin_MXslice.py \
    --tf "$tf" \
    --pass_name "${pass_name}_Region0" \
    --fail_name "${fail_name}_Region0" \
    --title_extra "$mode" \
    --mx-boundaries "$mx_boundary1" "$mx_boundary2" \
    "${plot_options[@]}"

shopt -s nullglob
plots=(
    perbin_*_mY_MXslice-*.png
    log_perbin_*_mY_MXslice-*.png
)
if (( ${#plots[@]} == 0 )); then
    echo "ERROR: no MX-sliced post-fit plots were produced" >&2
    exit 1
fi
cp -- "${plots[@]}" "$output_dir"/

echo "Wrote ${#plots[@]} plots in $fit_dir"
echo "Copied plots to $output_dir"
