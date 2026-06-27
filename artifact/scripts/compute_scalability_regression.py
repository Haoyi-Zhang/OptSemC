#!/usr/bin/env python3
"""Fit simple scaling diagnostics to the measured finite comparison stress."""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "scalability_regression.csv"
SUMMARY = E / "scalability_regression_summary.csv"

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)

def fit(points):
    xs = [float(x) for x, _ in points]
    ys = [float(y) for _, y in points]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    ssxx = sum((x - xbar) ** 2 for x in xs)
    ssxy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    slope = ssxy / ssxx if ssxx else 0.0
    intercept = ybar - slope * xbar
    sst = sum((y - ybar) ** 2 for y in ys)
    sse = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (sse / sst) if sst else 1.0
    return slope, intercept, r2

by_projection = defaultdict(list)
for row in read_csv(E / "scalability_stress.csv"):
    by_projection[row["projection"]].append((row["comparisons"], row["elapsed_ms"]))
rows = []
for projection, points in sorted(by_projection.items()):
    slope, intercept, r2 = fit(points)
    rows.append({
        "projection": projection,
        "points": str(len(points)),
        "slope_ms_per_comparison": f"{slope:.9f}",
        "intercept_ms": f"{intercept:.3f}",
        "r_squared": f"{r2:.6f}",
        "comparisons_per_ms_from_slope": f"{(1.0 / slope) if slope > 0 else 0.0:.3f}",
    })
write_csv(OUT, rows, ["projection", "points", "slope_ms_per_comparison", "intercept_ms", "r_squared", "comparisons_per_ms_from_slope"])
summary = [
    {"metric": "projection_regressions", "value": str(len(rows))},
    {"metric": "min_r_squared", "value": f"{min(float(row['r_squared']) for row in rows):.6f}"},
    {"metric": "max_slope_ms_per_comparison", "value": f"{max(float(row['slope_ms_per_comparison']) for row in rows):.9f}"},
]
write_csv(SUMMARY, summary, ["metric", "value"])
print(f"Scalability regression: min R^2={summary[1]['value']}")
