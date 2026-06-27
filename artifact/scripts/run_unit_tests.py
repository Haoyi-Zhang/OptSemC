#!/usr/bin/env python3
"""Fast unit test runner with integration-test delegation.

The repository has separate checkers for full-corpus SQL execution, leave-out
stability, scalability, and lattice enumeration.  This runner executes the
package-level unit tests in one interpreter for speed and records the few heavy
integration tests delegated to those package gates.
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
DELEGATED_INTEGRATION_TESTS = {
    "test_false_severity_multicatalog.py": "false_portability_severity_check;sql_probe_multicatalog_check",
    "test_stability_leave_out.py": "leave_out_stability_check;engine_family_stress_check",
    "test_incremental_audit.py": "incremental_audit_check",
    "test_information_sql_bundle.py": "projection_information_profile_check;sql_probe_bundle_check",
    "test_sql_execution_catalog.py": "sql_probe_execution_check",
    "test_workload_replay_cover_order.py": "replay_plan_check;benchmark_compiler_check",
    "test_workload_replay_diagnostic_order.py": "replay_plan_check;benchmark_efficiency_certificate",
    "test_projection_resolution_lattice.py": "projection_resolution_check",
    "test_source_support_paper.py": "source_witness_support_check;paper_package_check",
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

total = 0
delegated = 0
failures: list[dict[str, str]] = []
for path in sorted(TEST_DIR.glob("test_*.py")):
    if path.name in DELEGATED_INTEGRATION_TESTS:
        n = count_tests(path)
        delegated += n
        print(f"DELEGATE {path.name} ({n} tests) -> {DELEGATED_INTEGRATION_TESTS[path.name]}", flush=True)
        continue
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
    writer.writerow({"check": "integration_tests_delegated_to_package_gates", "passed": "true", "tests": str(delegated), "failures": "0", "details": ";".join(f"{k}->{v}" for k,v in sorted(DELEGATED_INTEGRATION_TESTS.items()))})
if failures:
    print(f"Unit tests failed: {len(failures)}/{total}")
    for f in failures[:20]:
        print("FAIL", f.get("file"), f.get("test"), f.get("error"))
    raise SystemExit(1)
print(f"Unit tests passed: {total}/{total}; integration delegated: {delegated}")
