"""Small report builders for CSV-backed artifact diagnostics."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class MarkdownTable:
    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]

    def render(self) -> str:
        lines = ["| " + " | ".join(self.headers) + " |", "| " + " | ".join("---" for _ in self.headers) + " |"]
        for row in self.rows:
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)


@dataclass(frozen=True)
class ReportSection:
    title: str
    paragraphs: tuple[str, ...] = ()
    table: MarkdownTable | None = None

    def render(self) -> str:
        parts = [f"## {self.title}"]
        parts.extend(self.paragraphs)
        if self.table:
            parts.append(self.table.render())
        return "\n\n".join(parts)


def rows_to_table(rows: Sequence[Mapping[str, object]], columns: Sequence[str] | None = None, limit: int | None = None) -> MarkdownTable:
    if columns is None:
        columns = tuple(rows[0].keys()) if rows else ("empty",)
    clipped = rows if limit is None else rows[:limit]
    return MarkdownTable(tuple(columns), tuple(tuple(str(row.get(col, "")) for col in columns) for row in clipped))


def csv_summary(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {"path": path.as_posix(), "rows": str(len(rows)), "columns": str(len(rows[0]) if rows else 0)}


def render_report(title: str, sections: Sequence[ReportSection]) -> str:
    return "\n\n".join([f"# {title}", *[section.render() for section in sections]]) + "\n"


def pass_fail_section(title: str, rows: Sequence[Mapping[str, str]]) -> ReportSection:
    passed = sum(1 for row in rows if row.get("passed") == "true")
    paragraph = f"Passed {passed}/{len(rows)} checks."
    return ReportSection(title, (paragraph,), rows_to_table(rows, limit=20))


def write_markdown_report(path: Path, title: str, sections: Sequence[ReportSection]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_report(title, sections), encoding="utf-8")

