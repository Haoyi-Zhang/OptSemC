#!/usr/bin/env python3
"""Guard the manuscript against visual hacks that make the compiled PDF brittle."""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LATEX = ROOT / "Paper" / "latex"
OUT = ROOT / "artifact" / "evaluation" / "visual_latex_style.csv"

rows: list[dict[str, str]] = []


def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": str(details)})


paper = LATEX / "paper.tex"
paper_text = paper.read_text(encoding="utf-8", errors="ignore") if paper.exists() else ""

body_files = [paper]
body_files += sorted((LATEX / "sections").glob("*.tex"))
body_files += sorted((LATEX / "figures").glob("*.tex"))
body_files += sorted((LATEX / "tables").glob("*.tex"))

banned_patterns = {
    r"\\resizebox": "whole-object scaling hides overflow instead of fixing layout",
    r"\\scriptsize": "scriptsize is too small for PVLDB figure/table reading",
    r"\\tiny": "tiny is unreadable in two-column print",
}
violations: list[str] = []
for path in body_files:
    if not path.exists():
        continue
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    for pattern, reason in banned_patterns.items():
        for match in re.finditer(pattern, text):
            line = text.count("\n", 0, match.start()) + 1
            violations.append(f"{rel}:{line}:{pattern}:{reason}")
add("no_banned_visual_scaling_macros", not violations, ";".join(violations[:20]))

required_template = [LATEX / "acmart.cls", LATEX / "ACM-Reference-Format.bst"]
missing_template = [p.name for p in required_template if not p.exists()]
add("official_template_files_present", not missing_template, ";".join(missing_template))

if (LATEX / "acmart.cls").exists():
    data = (LATEX / "acmart.cls").read_bytes()
    text = data.decode("utf-8", errors="ignore")
    officialish = "v1.70" in text and "Association for Computing Machinery" in text
    add("acmart_template_identifiable", officialish, hashlib.sha256(data).hexdigest()[:12])
else:
    add("acmart_template_identifiable", False, "missing")

docclass_ok = bool(re.search(r"\\documentclass\[\s*sigconf\s*,\s*nonacm\s*\]\{acmart\}", paper_text))
add("documentclass_matches_pvldb_template", docclass_ok, "sigconf, nonacm")

pvl_db_block = all(
    token in paper_text
    for token in [
        "PVLDB Reference Format",
        "PVLDB, \\vldbvolume",
        "Proceedings of the VLDB Endowment",
        "\\newcommand\\vldbdoi",
        "\\newcommand\\vldbpages",
        "\\newcommand\\vldbauthors",
        "\\newcommand\\vldbtitle",
    ]
)
add("pvl_db_metadata_block_present", pvl_db_block, "reference/copyright metadata")

author_blocks = re.findall(r"\\author\{[^}]+\}(.*?)(?=\\author\{|\\begin\{document\})", paper_text, re.S)
author_two_text = author_blocks[1] if len(author_blocks) >= 2 else ""
author_two_ok = (
    "Nanyang Technological University" in author_two_text
    and "\\city{Singapore}" in author_two_text
    and "\\country{Singapore}" in author_two_text
    and "Suzhou" not in author_two_text
)
add("author_two_affiliation_is_ntu_singapore", author_two_ok, "Nanyang Technological University, Singapore")

global_hacks = [
    r"\\settopmatter\{printacmref=false\}",
    r"\\renewcommand\\footnotetextcopyrightpermission",
    r"\\setlength\{\\textfloatsep\}",
    r"\\setlength\{\\floatsep\}",
    r"\\setlength\{\\intextsep\}",
    r"\\emergencystretch",
]
hack_hits = [pat for pat in global_hacks if re.search(pat, paper_text)]
add("no_global_template_or_spacing_suppression", not hack_hits, ";".join(hack_hits))

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader()
    writer.writerows(rows)

failed = [row for row in rows if row["passed"] != "true"]
print(f"Visual LaTeX style: {len(rows) - len(failed)}/{len(rows)} passed")
for row in failed:
    print("FAIL", row["check"], row["details"])
sys.exit(1 if failed else 0)
