#!/usr/bin/env python3
"""Record the replay environment used for artifact validation."""
from __future__ import annotations

import csv
import hashlib
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation" / "environment.csv"


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def module_version(name: str) -> str:
    try:
        module = __import__(name)
    except Exception as exc:
        return f"unavailable:{type(exc).__name__}"
    return str(getattr(module, "__version__", "installed"))


def command_output(args: list[str], timeout: int = 8) -> str:
    try:
        proc = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    except Exception as exc:
        return f"unavailable:{type(exc).__name__}"
    text = " ".join(proc.stdout.split())
    return text[:240] if proc.returncode == 0 else f"unavailable:exit{proc.returncode}:{text[:160]}"


def redacted_executable_name() -> str:
    name = Path(sys.executable).name
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name) or "python"


def postgres_version() -> str:
    dsn = os.environ.get("OPTSEMC_POSTGRES_DSN")
    if not dsn:
        return "not-requested"
    try:
        import psycopg
        with psycopg.connect(dsn, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SHOW server_version")
                row = cur.fetchone()
                return str(row[0]) if row else "unknown"
    except Exception as exc:
        return f"unavailable:{type(exc).__name__}"


rows = [
    {"key": "scope", "value": "artifact-only" if not (ROOT.parent / "Paper").exists() else "full-repository"},
    {"key": "python", "value": sys.version.replace("\n", " ")},
    {"key": "platform", "value": platform.platform()},
    {"key": "machine", "value": platform.machine()},
    {"key": "python_executable_name", "value": redacted_executable_name()},
    {"key": "pyyaml", "value": module_version("yaml")},
    {"key": "pypdf", "value": module_version("pypdf")},
    {"key": "duckdb", "value": module_version("duckdb")},
    {"key": "psycopg", "value": module_version("psycopg")},
    {"key": "postgres", "value": postgres_version()},
    {"key": "git_head", "value": command_output(["git", "-C", str(ROOT.parent), "rev-parse", "--short=12", "HEAD"])},
    {"key": "artifact_readme_sha256", "value": file_digest(ROOT / "README.md")},
]

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["key", "value"])
    writer.writeheader()
    writer.writerows(rows)
print(f"Environment report: {len(rows)} rows")
