"""Reusable CSV generation utilities for local scripts."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIRECTORY = PROJECT_ROOT / "output"


def generate_csv(
    filename: str,
    fieldnames: Sequence[str],
    rows: Iterable[Mapping[str, object]],
) -> Path:
    """Write rows to ``output/<filename>`` and return the resulting path."""
    output_path = _output_path(filename)
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)

    # UTF-8 with BOM and semicolon delimiters open correctly in Excel with pt-BR settings.
    with output_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="raise",
            delimiter=";",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return output_path


def _output_path(filename: str) -> Path:
    path = Path(filename)
    if path.name != filename or path.suffix.lower() != ".csv":
        raise ValueError("filename must be a CSV filename without directory components.")
    return OUTPUT_DIRECTORY / path
