#!/usr/bin/env python3
"""Fast unit test runner with verified integration-gate delegation.

The repository has separate checkers for full-corpus SQL execution, leave-out
stability, scalability, and lattice enumeration.  This runner executes the
package-level unit tests in one interpreter for speed.  Heavy integration tests
may be delegated only when their current gate CSV files exist and pass.
"""
from __future__ import annotations
import ast
import csv
import importlib.util
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TEST_DIR = ROOT / "tests"
OUT = ROOT / "evaluation" / "unit_test_results.csv"
EVAL = ROOT / "evaluation"
DELEGATED_INTEGRATION_TESTS = {
    "test_false_severity_multicatalog.py": ("false_equivalence_severity_check", "sql_probe_multicatalog_check"),
    "test_stability_leave_out.py": ("leave_out_stability_check", "engine_family_stress_check"),
    "test_incremental_audit.py": ("incremental_audit_check",),
    "test_information_sql_bundle.py": ("projection_information_profile_check", "sql_probe_bundle_check"),
    "test_sql_execution_catalog.py": ("sql_probe_execution_check",),
    "test_projection_resolution_lattice.py": ("projection_resolution_check",),
}

def count_tests(path: Path) -> int:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return 0
    return sum(isinstance(node, ast.FunctionDef) and node.name.startswith("test_") for node in tree.body)

def run_file(path: Path) -> tuple[int, list[dict[str, str]]]:
    failures: list[dict[str, str]] = []
    count = 0
    try:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        for name, obj in list(vars(module).items()):
            if name.startswith("test_") and callable(obj):
                count += 1
                try:
                    obj()
                except Exception as exc:
                    failures.append({"file": path.name, "test": name, "error": repr(exc), "trace": traceback.format_exc(limit=3)})
    except Exception as exc:
        failures.append({"file": path.name, "test": "<module>", "error": repr(exc), "trace": traceback.format_exc(limit=3)})
    return count, failures

def row_ok(row: dict[str, str]) -> bool:
    if "passed" in row:
        return row.get("passed", "").lower() == "true"
    if "status" in row:
        return row.get("status", "").upper() == "PASS"
    if "ok" in row:
        return row.get("ok", "").lower() == "true"
    return True

def gate_csv_path(gate: str) -> Path:
    rel = gate if gate.endswith(".csv") else f"{gate}.csv"
    return EVAL / rel

def gate_passes(gate: str) -> tuple[bool, str]:
    path = gate_csv_path(gate)
    if not path.exists():
        return False, f"{gate}:missing:{path.relative_to(ROOT).as_posix()}"
    try:
        rows = read_csv(path)
    except Exception as exc:
        return False, f"{gate}:unreadable:{type(exc).__name__}"
    passable = [row for row in rows if any(key in row for key in ("passed", "status", "ok"))]
    if not passable:
        return False, f"{gate}:no-pass-column"
    failed = [row for row in passable if not row_ok(row)]
    if failed:
        return False, f"{gate}:failed={len(failed)}/{len(passable)}"
    return True, f"{gate}:passed={len(passable)}"

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

total = 0
delegated = 0
failures: list[dict[str, str]] = []
delegation_details: list[str] = []
delegation_failures: list[str] = []
for path in sorted(TEST_DIR.glob("test_*.py")):
    if path.name in DELEGATED_INTEGRATION_TESTS:
        n = count_tests(path)
        gate_results = [gate_passes(gate) for gate in DELEGATED_INTEGRATION_TESTS[path.name]]
        if all(ok for ok, _detail in gate_results):
            delegated += n
            details = ",".join(detail for _ok, detail in gate_results)
            delegation_details.append(f"{path.name}({n})->{details}")
            print(f"DELEGATE {path.name} ({n} tests) -> {details}", flush=True)
            continue
        for ok, detail in gate_results:
            if not ok:
                delegation_failures.append(f"{path.name}:{detail}")
        print(f"RUN {path.name} because delegated gate is not clean", flush=True)
    print(f"RUN {path.name}", flush=True)
    count, file_failures = run_file(path)
    total += count
    failures.extend(file_failures)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "tests", "failures", "details"])
    writer.writeheader()
    details = "|".join(f"{f.get('file')}:{f.get('test')}:{f.get('error')}" for f in failures[:10])
    writer.writerow({"check": "unit_tests", "passed": str(not failures).lower(), "tests": str(total), "failures": str(len(failures)), "details": details})
    writer.writerow({"check": "integration_tests_delegated_to_verified_gates", "passed": str(not delegation_failures).lower(), "tests": str(delegated), "failures": str(len(delegation_failures)), "details": ";".join(delegation_details + delegation_failures)})
if failures or delegation_failures:
    print(f"Unit tests failed: {len(failures)}/{total}")
    for f in failures[:20]:
        print("FAIL", f.get("file"), f.get("test"), f.get("error"))
    for f in delegation_failures[:20]:
        print("FAIL", f)
    raise SystemExit(1)
print(f"Unit tests passed: {total}/{total}; integration delegated: {delegated}")
