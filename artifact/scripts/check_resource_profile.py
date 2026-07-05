#!/usr/bin/env python3
"""Validate resource-profile outputs used by the paper."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "resource_profile_check.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    profile = rows(E / "resource_profile.csv")
    scale = rows(E / "resource_profile_scale.csv")
    checks = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "passed": str(passed).lower(), "detail": detail})

    stages = {row["stage"] for row in profile}
    add("required_stages", {"projection audit", "fixed-basis repair", "SQL catalog validation"}.issubset(stages), ",".join(sorted(stages)))
    add("positive_elapsed", all(float(row["elapsed_ms"]) > 0 for row in profile + scale), "all rows")
    add("positive_peak_rss", all(float(row["peak_rss_mb"]) > 0 for row in profile + scale), "all rows")
    add("scale_points", {row["scale"] for row in scale} == {"1x", "2x", "4x", "8x"}, ",".join(row["scale"] for row in scale))
    add("sql_validation_nonzero", any(row["stage"] == "SQL catalog validation" and int(row["output_rows"]) > 0 for row in profile), "sql output rows")
    add("scale_throughput_nonzero", all(float(row["throughput_per_s"]) > 0 for row in scale), "projection replay lift")
    eight = next((row for row in scale if row["scale"] == "8x"), None)
    add("eight_x_lift_rows_current", bool(eight) and int(eight["input_rows"]) >= 2_833_152, eight["input_rows"] if eight else "missing")
    add("eight_x_lift_throughput_floor", bool(eight) and float(eight["throughput_per_s"]) >= 200_000.0, eight["throughput_per_s"] if eight else "missing")
    add("scale_notes_disallow_new_corpus_reading", all("not new corpus" in row["note"].lower() for row in scale), ";".join(row["note"] for row in scale))
    if scale:
        rss_values = [float(row["peak_rss_mb"]) for row in scale]
        rss_bounded = max(rss_values) <= min(rss_values) * 1.10 + 1.0
        add("scale_peak_rss_bounded", rss_bounded, f"min={min(rss_values):.3f};max={max(rss_values):.3f}")
    else:
        add("scale_peak_rss_bounded", False, "missing scale rows")

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "detail"])
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(row["passed"] == "true" for row in checks)
    print(f"Resource profile check: {passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
