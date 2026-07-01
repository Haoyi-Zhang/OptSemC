#!/usr/bin/env python3
"""Compile the paper with a protected two-pass PDF update.

The checker uses batch-mode LaTeX and keeps a byte-for-byte backup of the last
valid manuscript.  If a compile fails or produces an invalid page count, the
backup is restored before the checker exits.  This avoids truncated PDFs in the
package tree while still exercising the canonical source target.
"""
from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LATEX = ROOT / "Paper" / "latex"
NAME = "paper"
TEX = LATEX / f"{NAME}.tex"
PDF = LATEX / f"{NAME}.pdf"
LOG = LATEX / f"{NAME}.log"
OUT = ROOT / "artifact" / "evaluation" / "latex_compile_check.csv"
BACKUP = LATEX / f"{NAME}.pdf.backup"
TRANSIENT_EXTS = ["aux", "log", "out", "toc", "bbl", "blg", "fls", "fdb_latexmk"]

if PDF.exists():
    shutil.copy2(PDF, BACKUP)

notes: list[str] = []
compile_failed = False
commands = [
    ("pdflatex1", ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", TEX.name]),
    ("bibtex", ["bibtex", NAME]),
    ("pdflatex2", ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", TEX.name]),
    ("pdflatex3", ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", TEX.name]),
]
for label, command in commands:
    if label == "bibtex" and not (LATEX / f"{NAME}.aux").exists():
        compile_failed = True
        notes.append("bibtex:missing_aux")
        break
    try:
        proc = subprocess.run(
            command,
            cwd=LATEX,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=90,
            check=False,
        )
        if proc.returncode != 0:
            notes.append(f"{label}:returncode={proc.returncode}")
    except subprocess.TimeoutExpired:
        compile_failed = True
        notes.append(f"{label}:timeout")
        break

log_text = LOG.read_text(errors="ignore") if LOG.exists() else ""
rows: list[dict[str, str]] = []
failed = compile_failed
rows.append({"check": "compiler_return_codes_nonfatal", "passed": "true", "count": str(len(notes)), "examples": " | ".join(notes[:3])})
patterns_fail = {
    "fatal_error": r"Fatal error|Emergency stop|! LaTeX Error",
    "undefined_refs": r"There were undefined references|Reference `[^']+' .* undefined",
    "undefined_cites": r"undefined citations|Citation `[^']+' .* undefined",
    "overfull_hbox": r"Overfull \\hbox",
    "temporary_extra_page": r"Temporary extra page added",
}
for check, pattern in patterns_fail.items():
    matches = re.findall(pattern, log_text, flags=re.I)
    ok = len(matches) == 0 and not (check == "fatal_error" and compile_failed)
    failed = failed or not ok
    rows.append({"check": check, "passed": str(ok).lower(), "count": str(len(matches)), "examples": " | ".join(str(m) for m in matches[:3])})

vbox_amounts = [float(x) for x in re.findall(r"Overfull \\vbox \(([0-9.]+)pt too high\)", log_text)]
vbox_bad = [x for x in vbox_amounts if x > 5.0]
rows.append({"check": "overfull_vbox_tiny_nonfatal", "passed": str(len(vbox_bad) == 0).lower(), "count": str(len(vbox_amounts)), "examples": ";".join(f"{x:.3f}pt" for x in vbox_amounts[:3])})
failed = failed or bool(vbox_bad)
underfull = len(re.findall(r"Underfull \\[hv]box", log_text))
rows.append({"check": "underfull_boxes_nonfatal", "passed": "true", "count": str(underfull), "examples": ""})

def has_pdf_eof(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 1000:
        return False
    return b"%%EOF" in path.read_bytes()[-2048:]

pdf_ok = has_pdf_eof(PDF)
rows.append({"check": "pdf_eof_marker", "passed": str(pdf_ok).lower(), "count": "1" if pdf_ok else "0", "examples": PDF.name})
failed = failed or not pdf_ok

# Enforce the PVLDB-targeted manuscript shape used throughout the package.
pages = "unknown"
try:
    info = subprocess.check_output(["pdfinfo", str(PDF)], text=True, timeout=20)
    for line in info.splitlines():
        if line.startswith("Pages:"):
            pages = line.split(":", 1)[1].strip()
            break
except Exception as exc:  # pragma: no cover - external tool failure path
    pages = type(exc).__name__
try:
    page_count = int(pages)
except ValueError:
    page_count = 0
rows.append({"check": "expected_total_pages", "passed": str(page_count >= 13).lower(), "count": pages, "examples": "body_12_references_start_page_13_references_unlimited"})
failed = failed or page_count < 13

if failed and BACKUP.exists():
    shutil.copy2(BACKUP, PDF)

# Clean successful build artifacts so package-manifest checks stay deterministic.
for ext in TRANSIENT_EXTS:
    p = LATEX / f"{NAME}.{ext}"
    if p.exists():
        p.unlink()
for pattern in [f"{NAME}.compile_pass*.txt", f"{NAME}_build.*", "stable49.*", "fastbuild.*", "testbuild.*", "halt_*.*"]:
    for p in LATEX.glob(pattern):
        if p.is_file():
            p.unlink()
if BACKUP.exists():
    BACKUP.unlink()

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "count", "examples"])
    writer.writeheader()
    writer.writerows(rows)

passed = sum(row["passed"] == "true" for row in rows)
print(f"LaTeX compile check: {passed}/{len(rows)} checks passed")
if failed:
    for row in rows:
        if row["passed"] != "true":
            print("FAIL", row)
    sys.exit(1)
