#!/usr/bin/env python3
"""Check repository architecture boundaries and import graph acyclicity."""
from __future__ import annotations
import csv, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.architecture import import_edges, internal_adjacency, module_name, strongly_connected_components, has_module_docstring
from optsemc.io import write_csv

PKG = ROOT / "optsemc"
E = ROOT / "evaluation"
modules = sorted(module_name(p, PKG.parent) for p in PKG.glob("*.py"))
edges = import_edges(PKG)
adj = internal_adjacency(edges, modules)
sccs = strongly_connected_components(adj)
write_csv(E / "architecture_import_graph.csv", [e.as_row() for e in edges], ["source", "target", "kind"])
write_csv(E / "architecture_import_cycles.csv", [{"cycle": " -> ".join(c)} for c in sccs], ["cycle"])
rows=[]
def add(check, passed, details=""):
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": str(details)})
add("package_modules_present", len(modules) >= 40, f"modules={len(modules)}")
add("package_import_graph_acyclic", len(sccs) == 0, ";".join("|".join(c) for c in sccs[:5]))
package_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in PKG.glob("*.py"))
script_import_edges = [e for e in edges if e.target.startswith("artifact.scripts") or e.target.startswith("scripts")]
add("package_never_imports_scripts", not script_import_edges, ";".join(e.source+"->"+e.target for e in script_import_edges[:5]))
add("package_no_sys_path_mutation", "sys.path" not in package_text, "")
add("all_package_modules_documented", all(has_module_docstring(p) for p in PKG.glob("*.py")), "")
todo_hits=[]
for p in list(PKG.glob("*.py")) + list((ROOT/"scripts").glob("*.py")):
    t = p.read_text(encoding="utf-8", errors="ignore")
    markers = ("TO"+"DO", "FIX"+"ME", "XX"+"X", "HA"+"CK")
    if any(marker in t for marker in markers):
        todo_hits.append(str(p.relative_to(ROOT)))
add("no_todo_fixme_markers", not todo_hits, "|".join(todo_hits[:10]))
# Scripts may add ROOT to sys.path for standalone execution, but package modules should remain library-clean.
script_imports_package = 0
for p in (ROOT/"scripts").glob("*.py"):
    if "optsemc" in p.read_text(encoding="utf-8", errors="ignore"):
        script_imports_package += 1
add("scripts_reuse_package_library", script_imports_package >= 40, f"scripts={script_imports_package}")
write_csv(E / "architecture_contract.csv", rows, ["check", "passed", "details"])
passed=sum(r["passed"]=="true" for r in rows)
print(f"Architecture contract: {passed}/{len(rows)} passed")
for r in rows:
    if r["passed"] != "true": print("FAIL", r["check"], r["details"])
if passed != len(rows): sys.exit(1)
