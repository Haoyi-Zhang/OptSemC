#!/usr/bin/env python3
"""Check that the anti-overfitting audit records both pass and boundary cases."""
from __future__ import annotations

import csv
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "evaluation" / "anti_overfit_audit.csv"
OUT = ROOT / "evaluation" / "anti_overfit_audit_check.csv"


def main() -> int:
    rows = list(csv.DictReader(PATH.open(newline="", encoding="utf-8")))
    checks = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "passed": str(passed).lower(), "detail": detail})

    verdicts = {row["verdict"] for row in rows}
    scopes = {row["scope"] for row in rows}
    by_gate_scope = {(row["gate"], row["scope"]): row for row in rows}

    def has_row(gate: str, scope: str, evidence: str | None = None, verdict: str | None = None) -> bool:
        row = by_gate_scope.get((gate, scope))
        if row is None:
            return False
        if evidence is not None and row["evidence"] != evidence:
            return False
        if verdict is not None and row["verdict"] != verdict:
            return False
        return True

    def unresolved_counts(row: dict[str, str] | None) -> list[int]:
        if not row:
            return []
        return [int(value) for value in re.findall(r":(\d+)", row["evidence"])]

    add("audit_rows", len(rows) >= 8, str(len(rows)))
    add("has_source_sensitive_yesno", any(row["scope"] == "yes/no" and row["verdict"] == "source-sensitive" for row in rows), "yes/no boundary recorded")
    add("has_stress_fail_boundary", "stress-fails" in verdicts, ",".join(sorted(verdicts)))
    add("has_within_denominator_boundary", "within-denominator" in verdicts, ",".join(sorted(verdicts)))
    add("reported_basis_keywords_present", {"keyword", "operator-only", "yes/no"}.issubset(scopes) or any("reported layer+placement" in s for s in scopes), ",".join(sorted(scopes)))
    add("claim_boundaries_nonempty", all(row["claim_boundary"].strip() for row in rows), "all rows")
    add("keyword_source_loo_exact", has_row("source removal", "keyword", "nonzero=26/26", "pass"), "keyword source removal")
    add("operator_source_loo_exact", has_row("source removal", "operator-only", "nonzero=26/26", "pass"), "operator source removal")
    add("probe_subsample_exact", has_row("probe subsample", "keyword/operator 10%", "30/30; 30/30", "within-denominator"), "probe subsample")
    add("yesno_source_sensitive_exact", has_row("source removal", "yes/no", "nonzero=25/26", "source-sensitive"), "yes/no source boundary")
    feature = by_gate_scope.get(("feature-family stress", "fixed layer+placement"))
    engine = by_gate_scope.get(("engine-family stress", "fixed layer+placement"))
    learned = by_gate_scope.get(("learned engine-pair repair", "point-learned pair minima"))
    add("fixed_basis_feature_stress_zero", unresolved_counts(feature) == [0, 0, 0], feature["evidence"] if feature else "missing")
    add("fixed_basis_engine_stress_zero", unresolved_counts(engine) == [0, 0, 0], engine["evidence"] if engine else "missing")
    learned_counts = unresolved_counts(learned)
    add("learned_pair_transfer_fails_nonzero", bool(learned_counts) and all(value > 0 for value in learned_counts), learned["evidence"] if learned else "missing")

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "detail"])
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(row["passed"] == "true" for row in checks)
    print(f"Anti-overfit audit check: {passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
