"""Run the query configured in ``calculator.py`` and save its result as CSV.

Example:
    uv run python src/scripts/export_calculator_csv.py
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import generate_csv

if TYPE_CHECKING:
    from industrial_model.calculator import (
        CalculationResult,
        Calculator,
        CalculatorQuery,
    )


DEFAULT_OUTPUT_FILENAME = "calculator_result.csv"

# --- Configuration ---------------------------------------------------------
# Edit this calculation window before running the script.
START = datetime(2026, 8, 23, tzinfo=UTC)
END = datetime(2026, 8, 24, tzinfo=UTC)
# ---------------------------------------------------------------------------


def main() -> None:
    """Calculate the current query and write a spreadsheet-friendly CSV."""
    args = _parse_arguments()
    if END <= START:
        raise ValueError("END must be after START.")

    calculator, query = _load_current_calculator()
    result = calculator.calculate(query, start=START, end=END)
    input_aliases = [parameter.alias for parameter in query.parameters]
    fieldnames, rows = _csv_rows(result, input_aliases)
    output_path = generate_csv(args.output, fieldnames, rows)

    print(f"Formula: {query.formula}")
    print(f"Period: {_format_timestamp(START)} to {_format_timestamp(END)}")
    print(f"Calculated datapoints: {len(result.datapoints)}")
    print(f"CSV saved to: {output_path}")


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run src/scripts/calculator.py and export its results to CSV."
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILENAME,
        help=(
            "CSV filename to create inside output/ "
            f"(default: {DEFAULT_OUTPUT_FILENAME})."
        ),
    )
    return parser.parse_args()


def _load_current_calculator() -> tuple[Calculator, CalculatorQuery]:
    """Load the calculator and query exactly as currently configured."""
    from scripts.calculator import calculator, query

    return calculator, query


def _csv_rows(
    result: CalculationResult,
    input_aliases: Sequence[str],
) -> tuple[list[str], list[dict[str, object]]]:
    """Flatten calculated and input values into one row per timestamp."""
    input_columns = _input_columns(input_aliases, result)
    input_values_by_timestamp = {
        alias: {
            datapoint.timestamp: datapoint.value for datapoint in result.inputs[alias]
        }
        for alias in input_columns
    }

    rows: list[dict[str, object]] = []
    for datapoint in result.datapoints:
        row: dict[str, object] = {
            "timestamp_utc": _format_timestamp(datapoint.timestamp),
            "calculated_value": _format_excel_number(datapoint.value),
        }
        for alias, column_name in input_columns.items():
            row[column_name] = _format_excel_number(
                input_values_by_timestamp[alias].get(datapoint.timestamp)
            )
        rows.append(row)

    return ["timestamp_utc", "calculated_value", *input_columns.values()], rows


def _input_columns(
    input_aliases: Sequence[str], result: CalculationResult
) -> dict[str, str]:
    """Return stable, human-readable and unique column names for calculator inputs."""
    columns: dict[str, str] = {}
    used_names = {"timestamp_utc", "calculated_value"}
    for alias in input_aliases:
        if alias not in result.inputs or alias in columns:
            continue

        base_name = f"input_{_csv_safe_name(alias)}"
        column_name = base_name
        suffix = 2
        while column_name in used_names:
            column_name = f"{base_name}_{suffix}"
            suffix += 1
        columns[alias] = column_name
        used_names.add(column_name)
    return columns


def _csv_safe_name(value: str) -> str:
    cleaned = "".join(
        character.lower() if character.isalnum() else "_" for character in value.strip()
    ).strip("_")
    return cleaned or "value"


def _format_timestamp(timestamp: datetime) -> str:
    return timestamp.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _format_excel_number(value: float | None) -> str:
    """Render a numeric value as plain text when the CSV opens in Excel.

    Excel's General format turns large values into scientific notation and can
    discard digits. A text-returning formula keeps every digit visible while
    leaving empty datapoints as empty cells.
    """
    if value is None:
        return ""

    plain_value = format(value, ".15f").rstrip("0").rstrip(".")
    return f'="{plain_value}"'


if __name__ == "__main__":
    main()
