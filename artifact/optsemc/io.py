"""Deterministic file helpers for OptSem-C CSV/JSONL/YAML artifacts."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, MutableMapping, Sequence, TypeVar

try:
    import yaml
except Exception:  # pragma: no cover - caught at call site for clearer messages
    yaml = None

T = TypeVar("T", bound=Mapping[str, object])


def read_jsonl(path: Path) -> Iterator[dict]:
    """Yield JSON objects from a JSONL file with line-aware errors."""
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:  # pragma: no cover - exceptional path
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: expected object, got {type(value).__name__}")
            yield value


def write_jsonl(path: Path, rows: Iterable[Mapping[str, object]], *, sort_keys: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(dict(row), ensure_ascii=False, sort_keys=sort_keys, separators=(",", ":")))
            handle.write("\n")


def read_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        if not rows:
            fieldnames = ["empty"]
            rows = [{"empty": "true"}]
        else:
            fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        writer.writerows([dict(row) for row in rows])


def read_yaml(path: Path) -> object:
    if yaml is None:
        raise RuntimeError("PyYAML is required to read YAML artifacts")
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def metric(rows: Iterable[Mapping[str, str]], key: str, *, key_fields: Sequence[str] = ("metric", "check"), value_fields: Sequence[str] = ("value", "passed")) -> str | None:
    for row in rows:
        if any(row.get(field) == key for field in key_fields):
            for value_field in value_fields:
                if row.get(value_field) is not None:
                    return str(row.get(value_field))
    return None
