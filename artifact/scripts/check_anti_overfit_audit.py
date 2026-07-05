#!/usr/bin/env python3
"""Check that the anti-overfitting audit records both pass and boundary cases."""
from __future__ import annotations

import csv
from pathlib import Path

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
    add("audit_rows", len(rows) >= 8, str(len(rows)))
    add("has_source_sensitive_yesno", any(row["scope"] == "yes/no" and row["verdict"] == "source-sensitive" for row in rows), "yes/no boundary recorded")
    add("has_stress_fail_boundary", "stress-fails" in verdicts, ",".join(sorted(verdicts)))
    add("has_within_denominator_boundary", "within-denominator" in verdicts, ",".join(sorted(verdicts)))
    add("reported_basis_keywords_present", {"keyword", "operator-only", "yes/no"}.issubset(scopes) or any("reported layer+placement" in s for s in scopes), ",".join(sorted(scopes)))
    add("claim_boundaries_nonempty", all(row["claim_boundary"].strip() for row in rows), "all rows")

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "detail"])
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(row["passed"] == "true" for row in checks)
    print(f"Anti-overfit audit check: {passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
