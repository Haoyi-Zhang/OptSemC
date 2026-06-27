"""Streaming scanners used by package-facing hygiene gates."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Iterator, Pattern

TEXT_SUFFIXES = frozenset({
    ".bib", ".cff", ".csv", ".json", ".jsonl", ".md", ".py", ".sh", ".tex", ".toml", ".txt", ".yaml", ".yml",
})
BINARY_SUFFIXES = frozenset({".pdf", ".png", ".jpg", ".jpeg", ".gz", ".zip", ".duckdb", ".sqlite"})


def iter_text_files(base: Path) -> Iterator[Path]:
    """Yield files likely to be UTF-8 text without reading their contents."""
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in BINARY_SUFFIXES:
            continue
        if suffix and suffix not in TEXT_SUFFIXES and path.name not in {"Makefile", "LICENSE", "VERSION"}:
            continue
        yield path


def contains_pattern(path: Path, pattern: Pattern[str], *, chunk_size: int = 1024 * 1024) -> bool:
    """Return true iff a text file contains a regex pattern using bounded memory."""
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            carry = ""
            for chunk in iter(lambda: handle.read(chunk_size), ""):
                text = carry + chunk
                if pattern.search(text):
                    return True
                carry = text[-512:]
    except OSError:
        return False
    return False


def transient_paths(base: Path, *, suffixes: tuple[str, ...], names: set[str]) -> list[str]:
    """Return transient paths relative to a base tree."""
    offenders: list[str] = []
    for path in base.rglob("*"):
        name = path.name
        if name in names or name.endswith(suffixes) or name.startswith("paper_build"):
            offenders.append(path.relative_to(base).as_posix())
    return sorted(offenders)
