#!/usr/bin/env python3
"""Audit paper-table rendering ownership for the current OptSem-C snapshot.

Earlier drafts used this entry point to synthesize tables from now-retired CSV
names. Keeping a stale renderer in the artifact is a reproducibility hazard:
reviewers can invoke it, get silently skipped tables, and reasonably conclude
that the paper and artifact disagree. The current artifact keeps table
generation close to the evidence-producing scripts, so this compatibility
entry point now performs a strict manifest audit instead of regenerating
heavyweight evidence.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"
MANIFEST = ART / "evaluation" / "paper_table_manifest.csv"
OUT = ART / "evaluation" / "paper_table_renderers.csv"
SCRIPT_DIR = ART / "scripts"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def discover_owner_scripts(latex_rel: str) -> list[str]:
    """Return scripts that mention the table file by basename or relative path."""
    basename = Path(latex_rel).name
    hits: list[str] = []
    for script in sorted(SCRIPT_DIR.glob("*.py")):
        if script.name == Path(__file__).name:
            continue
        text = script.read_text(encoding="utf-8", errors="ignore")
        if basename in text or latex_rel in text:
            hits.append(script.relative_to(ART).as_posix())
    return hits


def main() -> int:
    if not MANIFEST.exists():
        raise SystemExit(f"missing paper-table manifest: {MANIFEST.relative_to(ROOT)}")

    rows: list[dict[str, str]] = []
    all_ok = True
    for item in read_csv(MANIFEST):
        table = item["paper_table"]
        latex_rel = item["latex_file"]
        source_rels = [s.strip() for s in item.get("source_files", "").split(";") if s.strip()]
        latex_missing = not (ROOT / latex_rel).exists()
        missing_sources = [src for src in source_rels if not (ROOT / src).exists()]
        owner_scripts = discover_owner_scripts(latex_rel)
        # Static tables are allowed, but only when they have declared evidence
        # sources. The manifest is the contract; the owner list is an audit aid.
        ok = (not latex_missing) and (not missing_sources) and bool(source_rels)
        all_ok &= ok
        rows.append(
            {
                "paper_table": table,
                "latex_file": latex_rel,
                "source_count": str(len(source_rels)),
                "missing_source_count": str(len(missing_sources)),
                "missing_sources": "|".join(missing_sources),
                "owner_script_count": str(len(owner_scripts)),
                "owner_scripts": "|".join(owner_scripts) if owner_scripts else "manifest-sourced-static",
                "passed": str(ok).lower(),
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "paper_table",
        "latex_file",
        "source_count",
        "missing_source_count",
        "missing_sources",
        "owner_script_count",
        "owner_scripts",
        "passed",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    passed = sum(1 for row in rows if row["passed"] == "true")
    print(f"Paper-table renderer audit: {passed}/{len(rows)} passed")
    if not all_ok:
        for row in rows:
            if row["passed"] != "true":
                print("FAIL", row["paper_table"], row["missing_sources"])
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
