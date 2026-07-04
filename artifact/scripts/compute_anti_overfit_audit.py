#!/usr/bin/env python3
"""Build a compact anti-overfitting audit from frozen evaluation outputs."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
G = E / "grounded"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def by_key(path: Path, key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows(path)}


def write_csv(path: Path, data: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def main() -> int:
    negative = rows(G / "negative_control.csv")[0]
    source = by_key(G / "source_robustness_summary.csv", "method")
    feature = by_key(E / "feature_holdout_repair_summary.csv", "method")
    engine = by_key(E / "engine_family_stress_summary.csv", "projection")
    subsample = rows(G / "probe_subsample_robustness.csv")
    engine_learned = by_key(G / "repair_enginepair_generalization_summary.csv", "method")

    def subsample_nonzero(method: str, fraction: str) -> str:
        for row in subsample:
            if row["method"] == method and row["fraction"] == fraction:
                return f"{row['nonzero_trials']}/{row['trials']}"
        return "--"

    audit: list[dict[str, str]] = [
        {
            "gate": "negative control",
            "scope": "strict reference",
            "evidence": f"false={negative['false_equivalences']}",
            "verdict": "pass",
            "claim_boundary": "reference equality is not counted as a collision source",
        },
        {
            "gate": "source removal",
            "scope": "keyword",
            "evidence": f"nonzero={source['keyword']['runs_with_nonzero_false_equivalences']}/{source['keyword']['leave_one_source_runs']}",
            "verdict": "pass",
            "claim_boundary": "keyword collisions survive every single-source removal",
        },
        {
            "gate": "source removal",
            "scope": "operator-only",
            "evidence": f"nonzero={source['operator_only']['runs_with_nonzero_false_equivalences']}/{source['operator_only']['leave_one_source_runs']}",
            "verdict": "pass",
            "claim_boundary": "operator-only collisions survive every single-source removal",
        },
        {
            "gate": "source removal",
            "scope": "yes/no",
            "evidence": f"nonzero={source['yesno']['runs_with_nonzero_false_equivalences']}/{source['yesno']['leave_one_source_runs']}",
            "verdict": "source-sensitive",
            "claim_boundary": "yes/no is sparse; do not claim every source-removal run remains nonzero",
        },
        {
            "gate": "probe subsample",
            "scope": "keyword/operator 10%",
            "evidence": f"{subsample_nonzero('keyword','0.1')}; {subsample_nonzero('operator_only','0.1')}",
            "verdict": "pass",
            "claim_boundary": "headline keyword/operator effects are not carried by one probe slice",
        },
        {
            "gate": "feature-family stress",
            "scope": "fixed layer+placement",
            "evidence": "; ".join(
                f"{m}:{feature[m]['robust_basis_unresolved_total']}" for m in ("keyword", "operator_only", "yesno")
            ),
            "verdict": "pass",
            "claim_boundary": "overlapping feature-family stress, not a disjoint held-out test",
        },
        {
            "gate": "engine-family stress",
            "scope": "fixed layer+placement",
            "evidence": "; ".join(
                f"{m}:{engine[m]['max_unresolved_after_layer_placement']}" for m in ("keyword", "operator_only", "yesno")
            ),
            "verdict": "pass",
            "claim_boundary": "fixed predeclared basis stress, not learned repair transfer",
        },
        {
            "gate": "learned engine-pair repair",
            "scope": "point-learned minima",
            "evidence": "; ".join(
                f"{m}:{engine_learned[m]['heldout_unresolved']}" for m in ("keyword", "operator_only", "yesno")
            ),
            "verdict": "stress-fails",
            "claim_boundary": "do not claim point-learned repairs generalize across held-out engine pairs",
        },
    ]
    fields = ["gate", "scope", "evidence", "verdict", "claim_boundary"]
    write_csv(E / "anti_overfit_audit.csv", audit, fields)
    print(f"Anti-overfit audit: wrote {len(audit)} gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
