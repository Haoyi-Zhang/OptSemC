#!/usr/bin/env python3
"""Validate that the artifact is a clean installable Python package."""
from __future__ import annotations
import csv, importlib, sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 compatibility
    import tomli as tomllib  # type: ignore[no-redef]
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation" / "packaging_installability.csv"
rows=[]
def add(check, passed, details=""):
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": str(details)})
try:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = data.get("project", {})
    dynamic_fields = set(project.get("dynamic", []))
    add("project_version_not_hardcoded", "version" not in project and "version" in dynamic_fields, f"dynamic={sorted(dynamic_fields)}")
    build_requires = set(data.get("build-system", {}).get("requires", []))
    add("dynamic_version_backend_declared", any(req.startswith("setuptools-scm") for req in build_requires), str(sorted(build_requires)))
    scm = data.get("tool", {}).get("setuptools_scm", {})
    add(
        "dynamic_version_git_root_declared",
        scm.get("root") == ".." and scm.get("relative_to") == "pyproject.toml",
        str(scm),
    )
    tool = data.get("tool", {}).get("setuptools", {})
    pkg_dir = tool.get("package-dir", {}).get("optsemc", "")
    add("package_dir_exists", bool(pkg_dir) and (ROOT / pkg_dir).is_dir(), pkg_dir)
    packages = set(tool.get("packages", []))
    add("optsemc_declared_package", "optsemc" in packages, str(packages))
    add("readme_exists", (ROOT / str(project.get("readme", "README.md"))).exists(), str(project.get("readme", "README.md")))
    add("license_is_spdx_string", isinstance(project.get("license"), str) and project.get("license") == "MIT", str(project.get("license")))
    scripts = project.get("scripts", {})
    target = scripts.get("optsemc", "")
    add("console_script_declared", target == "optsemc.cli:main", target)
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    module = importlib.import_module("optsemc.cli")
    add("console_script_target_imports", hasattr(module, "main"), "optsemc.cli:main")
except Exception as exc:
    add("packaging_exception", False, type(exc).__name__ + ":" + str(exc))
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed=sum(r["passed"]=="true" for r in rows)
print(f"Packaging installability: {passed}/{len(rows)} passed")
for r in rows:
    if r["passed"] != "true": print("FAIL", r["check"], r["details"])
if passed != len(rows): sys.exit(1)
