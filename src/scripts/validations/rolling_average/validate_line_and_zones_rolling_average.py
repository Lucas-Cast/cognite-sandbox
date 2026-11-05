"""Validate Rolling Average Output for one line and its zones.

Configure ``LINE_EXTERNAL_ID`` below, then run:

    uv run python src/scripts/validations/rolling_average/validate_line_and_zones_rolling_average.py

The script checks the line and its directly linked zones, compares up to 20
spread RAO datapoints per asset against the mapped Good Quantity series, and
exports a focused Excel workbook.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import NodeId
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

SCRIPT_DIRECTORY = Path(__file__).resolve().parents[2]
SRC_DIRECTORY = Path(__file__).resolve().parents[3]
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(SRC_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY))

import scripts.validations.rolling_average.export_rolling_average_validation as rao  # noqa: E402
from core import create_cognite_client  # noqa: E402
from core.data.asset_dom.asset_client import AssetClient  # noqa: E402

# --- Configuration: edit these values ------------------------------------
LINE_EXTERNAL_ID = "LNE-d766c97e9ed1c43bd25461748ed1451b"  # PFL04 / Fraga
LINE_SPACE: str | None = "sp_ash_elp_dat"
START = datetime(datetime.now(UTC).year, 2, 1, tzinfo=UTC)
END: datetime | None = None  # Exclusive; None means now.
OUTPUT_FILENAME: str | None = None
# --------------------------------------------------------------------------

OUTPUT_DIRECTORY = PROJECT_ROOT / "output"


def main() -> None:
    """Run the line-and-zones validation and write the Excel report."""
    start, end = _resolved_window()
    if not LINE_EXTERNAL_ID:
        raise ValueError("Set LINE_EXTERNAL_ID before running the script.")

    client = create_cognite_client()
    line, zones = _read_line_and_zones(client)
    assets = rao._validation_assets([line], {line.external_id: zones})

    rao._attach_rao_series(client, assets)
    rao._read_rao_samples(client, assets, start, end)
    rao._read_daily_coverage(client, assets, start, end)
    rao._read_latest_timestamps(client, assets, end)

    view_id, kpi_rows = rao._read_gq_parameter_rows(client)
    rao._attach_gq_series(assets, view_id, kpi_rows)
    gq_values = rao._read_gq_values(client, assets)
    sample_rows = rao._build_sample_rows(assets, gq_values)
    rao._create_alerts(assets, start, end)

    output_path = _write_workbook(line, zones, assets, sample_rows, start, end)
    _print_result(line, zones, assets, view_id, output_path, start, end)


def _resolved_window() -> tuple[datetime, datetime]:
    end = END or datetime.now(UTC)
    if START.tzinfo is None or end.tzinfo is None:
        raise ValueError("START and END must include a timezone (UTC recommended).")
    start_utc = START.astimezone(UTC)
    end_utc = end.astimezone(UTC)
    if end_utc <= start_utc:
        raise ValueError("END must be later than START.")
    return start_utc, end_utc


def _read_line_and_zones(client: CogniteClient) -> tuple[Any, list[Any]]:
    """Resolve one line and the zones directly linked to it."""
    asset_client = AssetClient(client)
    line_filter: dict[str, Any] = {"externalId": {"eq": LINE_EXTERNAL_ID}}
    if LINE_SPACE:
        line_filter["space"] = {"eq": LINE_SPACE}
    lines = asset_client.line.query_all_pages(filters=cast(Any, line_filter))
    lines = rao._unique_instances(lines)
    if not lines:
        raise ValueError(
            f'Line not found: "{LINE_EXTERNAL_ID}"'
            + (f" in space {LINE_SPACE}." if LINE_SPACE else ".")
        )
    if len(lines) > 1:
        spaces = ", ".join(sorted(line.space for line in lines))
        raise ValueError(
            f'Line external ID "{LINE_EXTERNAL_ID}" is not unique '
            f"(spaces: {spaces}). Set LINE_SPACE."
        )

    line = lines[0]
    line_id = NodeId(space=line.space, external_id=line.external_id)
    zones = asset_client.zone.query_all_pages(
        filters=cast(Any, {"line": {"containsAny": [line_id]}})
    )
    return line, rao._unique_instances(zones)


def _write_workbook(
    line: Any,
    zones: Sequence[Any],
    assets: Sequence[rao.ValidationAsset],
    sample_rows: Sequence[dict[str, Any]],
    start: datetime,
    end: datetime,
) -> Path:
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    filename = OUTPUT_FILENAME or (
        f"rolling_average_validation_line_{rao._safe_filename(LINE_EXTERNAL_ID)}.xlsx"
    )
    if Path(filename).name != filename or not filename.lower().endswith(".xlsx"):
        raise ValueError("OUTPUT_FILENAME must be an .xlsx filename without a path.")
    output_path = OUTPUT_DIRECTORY / filename

    workbook = Workbook()
    summary = workbook.active
    summary.title = "Summary"
    _write_summary_sheet(summary, line, zones, assets, start, end)

    coverage = workbook.create_sheet("Asset Coverage")
    rao._write_asset_coverage_sheet(coverage, assets, start, end)

    samples = workbook.create_sheet("Sample Points")
    rao._write_table_sheet(
        samples,
        list(sample_rows[0].keys()) if sample_rows else rao._sample_headers(),
        sample_rows,
    )

    mapping = workbook.create_sheet("GQ Mapping")
    rao._write_table_sheet(
        mapping, rao._mapping_headers(), rao._gq_mapping_rows(assets)
    )

    workbook.save(output_path)
    return output_path


def _write_summary_sheet(
    worksheet: Any,
    line: Any,
    zones: Sequence[Any],
    assets: Sequence[rao.ValidationAsset],
    start: datetime,
    end: datetime,
) -> None:
    worksheet.append(["Rolling Average Output validation: line and zones"])
    worksheet.append(["Line name", line.name or line.external_id])
    worksheet.append(["Line external ID", line.external_id])
    worksheet.append(["Line instance space", line.space])
    worksheet.append(
        ["Window UTC", f"{start.isoformat()} to {end.isoformat()} (end exclusive)"]
    )
    worksheet.append(["Expected minimum coverage", rao.MINIMUM_COVERAGE_PERCENT / 100])
    worksheet[6][1].number_format = "0.0%"
    worksheet.append([])
    worksheet.append(["Metric", "Count", "Details"])

    line_assets = [asset for asset in assets if asset.level == "Line"]
    zone_assets = [asset for asset in assets if asset.level == "Zone"]
    metrics = [
        ("Zones on this line", len(zones), "Directly linked Asset DOM zones"),
        (
            "Line has at least one RAO point",
            int(any(rao._has_rao_points(asset) for asset in line_assets)),
            "Across the requested window",
        ),
        (
            "Zones with at least one RAO point",
            sum(rao._has_rao_points(asset) for asset in zone_assets),
            "Across the requested window",
        ),
        (
            "Line and zone assets checked",
            len(assets),
            "One line plus all directly linked zones",
        ),
        (
            "Assets with GQ mapping",
            sum(bool(asset.gq_ids) for asset in assets),
            "From KpiParameterValue records with parameter GQ",
        ),
        (
            "Assets with validation alerts",
            sum(bool(asset.alerts) for asset in assets),
            "Missing series, missing mapping, low coverage, or stale data",
        ),
    ]
    for metric in metrics:
        worksheet.append(list(metric))

    asset_title_row = worksheet.max_row + 2
    worksheet.cell(asset_title_row, 1, "Line and zone detail")
    headers = [
        "Level",
        "Asset name",
        "Asset external ID",
        "RAO series found",
        "RAO datapoints",
        "Coverage",
        "GQ series mapped",
        "Alert",
    ]
    for column, header in enumerate(headers, start=1):
        worksheet.cell(asset_title_row + 1, column, header)
    for row_index, asset in enumerate(assets, start=asset_title_row + 2):
        worksheet.cell(row_index, 1, asset.level)
        worksheet.cell(row_index, 2, asset.name)
        worksheet.cell(row_index, 3, asset.external_id)
        worksheet.cell(row_index, 4, "Yes" if asset.rao_series else "No")
        worksheet.cell(row_index, 5, sum(asset.daily_counts.values()))
        worksheet.cell(
            row_index,
            6,
            rao._coverage_percent(asset, start, end) / 100,
        )
        worksheet.cell(row_index, 6).number_format = "0.0%"
        worksheet.cell(row_index, 7, len(asset.gq_ids))
        worksheet.cell(row_index, 8, "; ".join(dict.fromkeys(asset.alerts)))

    rao._format_worksheet(worksheet)
    rao._style_header_row(worksheet, 8)
    rao._style_header_row(worksheet, asset_title_row + 1)
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF", size=15)
        cell.fill = PatternFill("solid", fgColor="17365D")
    worksheet.row_dimensions[1].height = 28
    worksheet.column_dimensions["A"].width = 38
    worksheet.column_dimensions["B"].width = 36
    worksheet.column_dimensions["C"].width = 48
    worksheet.column_dimensions["H"].width = 54


def _print_result(
    line: Any,
    zones: Sequence[Any],
    assets: Sequence[rao.ValidationAsset],
    view_id: Any,
    output_path: Path,
    start: datetime,
    end: datetime,
) -> None:
    zone_assets = [asset for asset in assets if asset.level == "Zone"]
    zones_with_rao = sum(rao._has_rao_points(asset) for asset in zone_assets)
    print(f"Line: {line.name or line.external_id} ({line.space}/{line.external_id})")
    print(f"Window UTC: {start.isoformat()} to {end.isoformat()} (end exclusive)")
    print(f"Zones: {len(zones)}; with RAO points: {zones_with_rao}")
    print(f"KpiParameterValue view: {rao._view_label(view_id)}; parameter=GQ")
    print(f"Assets with alerts: {sum(bool(asset.alerts) for asset in assets)}")
    print(f"Excel saved to: {output_path}")


if __name__ == "__main__":
    main()
