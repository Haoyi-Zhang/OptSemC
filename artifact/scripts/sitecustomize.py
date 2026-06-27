"""Normalize CSV line endings for direct script entrypoints."""
from __future__ import annotations

import csv as _csv
from typing import Any

_writer = _csv.writer
_DictWriter = _csv.DictWriter


def writer(csvfile: Any, dialect: str = "excel", *args: Any, **kwargs: Any) -> Any:
    kwargs.setdefault("lineterminator", "\n")
    return _writer(csvfile, dialect, *args, **kwargs)


class DictWriter(_DictWriter):
    def __init__(self, f: Any, fieldnames: Any, restval: str = "", extrasaction: str = "raise", dialect: str = "excel", *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("lineterminator", "\n")
        super().__init__(f, fieldnames, restval=restval, extrasaction=extrasaction, dialect=dialect, *args, **kwargs)


_csv.writer = writer
_csv.DictWriter = DictWriter
