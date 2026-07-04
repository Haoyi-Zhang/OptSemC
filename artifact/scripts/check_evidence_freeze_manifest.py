#!/usr/bin/env python3
"""Validate frozen evidence hashes against the current replay package."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
MANIFEST = E / "evidence_freeze_manifest.csv"
OUT = E / "evidence_freeze_manifest_check.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    rows = list(csv.DictReader(MANIFEST.open(newline="", encoding="utf-8")))
    checks = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "passed": str(passed).lower(), "detail": detail})

    add("manifest_has_core_inputs", len(rows) >= 10, str(len(rows)))
    roles = {row["role"] for row in rows}
    add(
        "core_roles_present",
        {"schema", "feature_space", "source_manifest", "evidence_spans", "admitted_rules", "projection_portfolio"}.issubset(roles),
        ",".join(sorted(roles)),
    )
    for row in rows:
        rel = row["path"]
        path = ROOT / rel
        exists = path.exists()
        add(f"exists:{rel}", exists, rel)
        if exists:
            add(f"sha:{rel}", sha256(path) == row["sha256"], row["sha256"][:12])
        add(
            f"freeze_policy:{rel}",
            row["freeze_point"] == "before_projection_witness_counting" and bool(row["forbidden_after_freeze"].strip()),
            row["freeze_point"],
        )

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "detail"])
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(row["passed"] == "true" for row in checks)
    print(f"Evidence freeze manifest check: {passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
