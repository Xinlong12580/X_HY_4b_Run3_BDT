#!/usr/bin/env python3
"""Plot saved MultiDimFit grid points without requiring a best-fit entry."""

import argparse
import math
from array import array

import ROOT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--poi", default="r")
    parser.add_argument("--output", required=True)
    parser.add_argument("--y-max", type=float, default=100.0)
    parser.add_argument("--y-cut", type=float, default=100.0)
    args = parser.parse_args()

    ROOT.gROOT.SetBatch(True)
    source = ROOT.TFile.Open(args.input)
    if not source or source.IsZombie():
        raise RuntimeError(f"Cannot open scan file: {args.input}")
    tree = source.Get("limit")
    if not tree:
        raise RuntimeError(f"No 'limit' tree in: {args.input}")

    # Multiple entries at the same r can occur. Keep the smallest saved NLL at
    # each point, but do not require a deltaNLL=0 unconditional-fit entry.
    points = {}
    for entry in tree:
        x = float(getattr(entry, args.poi))
        y = 2.0 * float(entry.deltaNLL)
        if not (math.isfinite(x) and math.isfinite(y)):
            continue
        if y > args.y_cut:
            continue
        points[x] = min(y, points.get(x, math.inf))

    if not points:
        raise RuntimeError("The limit tree contains no finite scan points")

    ordered = sorted(points.items())
    xs = array("d", (point[0] for point in ordered))
    ys = array("d", (point[1] for point in ordered))
    graph = ROOT.TGraph(len(ordered), xs, ys)
    graph.SetTitle(f";{args.poi};2#Delta NLL")
    graph.SetLineWidth(2)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.7)

    canvas = ROOT.TCanvas("scan", "scan", 800, 700)
    canvas.SetGridy()
    graph.Draw("ALP")
    graph.GetYaxis().SetRangeUser(0.0, args.y_max)

    # Reference levels only; no best-fit line or marker is drawn.
    for level, style in ((1.0, 2), (4.0, 3)):
        line = ROOT.TLine(xs[0], level, xs[-1], level)
        line.SetLineStyle(style)
        line.SetLineColor(ROOT.kGray + 2)
        line.Draw()
        # Keep ownership on the canvas until it is saved.
        canvas.GetListOfPrimitives().Add(line)

    canvas.SaveAs(args.output + ".pdf")
    canvas.SaveAs(args.output + ".png")
    source.Close()


if __name__ == "__main__":
    main()
