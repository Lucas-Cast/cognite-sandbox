"""Validate site Rolling Average Output series and export an Excel workbook.

Configure the site external ID below, then run:

    uv run python src/scripts/export_rolling_average_validation.py

For every Line and Zone on the site, the script looks for the canonical
``<asset-external-id>-kpi-RAO-1m`` series, checks its history, and compares at
most 20 raw RAO points with values derived from that asset's Good Quantity
series. The calculation uses the GQ sums at minute t, t-1, and t-2; missing
minutes are excluded from the average and are never treated as zero.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import NodeId, ViewId, filters
from cognite.client.data_classes.datapoints import DatapointsQuery
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client
from core.data.asset_dom import AssetClient
from core.data.cognite_core import CogniteCoreClient

# --- Configuration ---------------------------------------------------------
# Enter the site's Asset DOM external ID. Set SITE_SPACE if it is not unique.
SITE_EXTERNAL_ID = "STE-63b498b98c74c8348c4c6602a6d37e06"
SITE_SPACE: str | None = None

# If omitted, the script discovers the latest accessible view named
# KpiParameterValue. Set the space to disambiguate if more than one is found.
KPI_PARAMETER_VALUE_VIEW_SPACE: str | None = "sp_kpi_glb_ing"
KPI_PARAMETER_VALUE_VIEW_EXTERNAL_ID = "KpiParameterValue"
KPI_PARAMETER_NAME = "GQ"
KPI_PARAMETER_NODE_SPACE = "sp_kpi_glb_dat"
KPI_PARAMETER_NODE_EXTERNAL_ID = "KPR-GQ"
# Used only when an older KpiParameterValue version stores a GQ external ID as
# plain text instead of a direct node reference.
GQ_TIME_SERIES_DEFAULT_SPACE = "sp_otm_fra_dat"

# Coverage is evaluated from the start of February in the current year through
# the execution time. END is exclusive. Set END to an aware datetime to pin it.
START = datetime(datetime.now(UTC).year, 2, 1, tzinfo=UTC)
END: datetime | None = None
OUTPUT_FILENAME: str | None = None

RAO_TIME_SERIES_SUFFIX = "-kpi-RAO-1m"
SAMPLE_POINTS_PER_ASSET = 20
GOOD_QUANTITY_GRANULARITY = "1m"
ROLLING_WINDOW_MINUTES = 3
VALUE_TOLERANCE = 0.01

# Tune these thresholds for the site's operating calendar if needed.
MINIMUM_COVERAGE_PERCENT = 80.0
MAXIMUM_START_DELAY = timedelta(days=1)
MAXIMUM_LAST_POINT_AGE = timedelta(days=1)

# Keep instance-data queries bounded and avoid oversized `in` filters.
INSTANCE_FILTER_BATCH_SIZE = 100
DATAPOINT_QUERY_BATCH_SIZE = 500
DATAPOINT_RETRIEVE_LIMIT = 100_000
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIRECTORY = PROJECT_ROOT / "output"
MILLISECONDS_PER_MINUTE = 60_000


@dataclass
class ValidationAsset:
    """A line or zone and the data collected for its RAO validation."""

    level: str
    external_id: str
    space: str
    name: str
    line_external_id: str
    line_name: str
    rao_series: Any | None = None
    rao_id: NodeId | None = None
    gq_ids: list[NodeId] = field(default_factory=list)
    gq_links: list[tuple[str, str]] = field(default_factory=list)
    sample_points: list[Any] = field(default_factory=list)
    daily_counts: dict[int, int] = field(default_factory=dict)
    first_timestamp: int | None = None
    latest_timestamp: int | None = None
    alerts: list[str] = field(default_factory=list)


def main() -> None:
    """Run the multi-asset validation and save its Excel report."""
    start, end = _resolved_window()
    if not SITE_EXTERNAL_ID or SITE_EXTERNAL_ID == "PUT_SITE_EXTERNAL_ID_HERE":
        raise ValueError("Set SITE_EXTERNAL_ID before running the script.")

    client = create_cognite_client()
    site, lines, zones_by_line = _site_asset_tree(client)
    assets = _validation_assets(lines, zones_by_line)
    _attach_rao_series(client, assets)
    _read_rao_samples(client, assets, start, end)
    _read_daily_coverage(client, assets, start, end)
    _read_latest_timestamps(client, assets, end)

    view_id, kpi_rows = _read_gq_parameter_rows(client)
    _attach_gq_series(assets, view_id, kpi_rows)
    gq_values = _read_gq_values(client, assets)
    sample_rows = _build_sample_rows(assets, gq_values)
    _create_alerts(assets, start, end)

    output_path = _write_workbook(site, lines, assets, sample_rows, start, end)
    _print_result(site, lines, assets, view_id, output_path, start, end)


def _resolved_window() -> tuple[datetime, datetime]:
    end = END or datetime.now(UTC)
    if START.tzinfo is None or end.tzinfo is None:
        raise ValueError("START and END must include a timezone (UTC recommended).")
    start_utc = START.astimezone(UTC)
    end_utc = end.astimezone(UTC)
    if end_utc <= start_utc:
        raise ValueError("END must be later than START.")
    return start_utc, end_utc


def _site_asset_tree(
    client: CogniteClient,
) -> tuple[Any, list[Any], dict[str, list[Any]]]:
    """Resolve a site, its lines, and each line's directly linked zones."""
    asset_client = AssetClient(client)
    site_filter: dict[str, Any] = {"externalId": {"eq": SITE_EXTERNAL_ID}}
    if SITE_SPACE:
        site_filter["space"] = {"eq": SITE_SPACE}
    sites = asset_client.site.query_all_pages(filters=cast(Any, site_filter))
    if not sites:
        raise ValueError(f'Site not found: "{SITE_EXTERNAL_ID}".')
    if len(sites) > 1:
        spaces = ", ".join(sorted(site.space for site in sites))
        raise ValueError(
            f'Site external ID "{SITE_EXTERNAL_ID}" is not unique (spaces: {spaces}). '
            "Set SITE_SPACE."
        )
    site = sites[0]
    site_id = NodeId(space=site.space, external_id=site.external_id)

    # Lines may point to the site via their Plant or LocationHierarchy.
    line_filter = {
        "OR": [
            {"plant": {"site": {"eq": site_id}}},
            {"location": {"site": {"eq": site_id}}},
        ]
    }
    lines = asset_client.line.query_all_pages(filters=cast(Any, line_filter))
    lines = _unique_instances(lines)

    zones_by_line: dict[str, list[Any]] = {}
    for line in lines:
        line_id = NodeId(space=line.space, external_id=line.external_id)
        zones = asset_client.zone.query_all_pages(
            filters=cast(Any, {"line": {"containsAny": [line_id]}})
        )
        zones_by_line[line.external_id] = _unique_instances(zones)
    return site, lines, zones_by_line


def _unique_instances(instances: Iterable[Any]) -> list[Any]:
    by_id: dict[tuple[str, str], Any] = {}
    for item in instances:
        by_id[(item.space, item.external_id)] = item
    return list(by_id.values())


def _validation_assets(
    lines: Sequence[Any], zones_by_line: Mapping[str, Sequence[Any]]
) -> list[ValidationAsset]:
    assets: list[ValidationAsset] = []
    for line in sorted(lines, key=lambda item: (item.name or "", item.external_id)):
        assets.append(
            ValidationAsset(
                level="Line",
                external_id=line.external_id,
                space=line.space,
                name=line.name or "",
                line_external_id=line.external_id,
                line_name=line.name or line.external_id,
            )
        )
        for zone in sorted(
            zones_by_line.get(line.external_id, ()),
            key=lambda item: (item.name or "", item.external_id),
        ):
            assets.append(
                ValidationAsset(
                    level="Zone",
                    external_id=zone.external_id,
                    space=zone.space,
                    name=zone.name or "",
                    line_external_id=line.external_id,
                    line_name=line.name or line.external_id,
                )
            )
    return assets


def _attach_rao_series(
    client: CogniteClient, assets: Sequence[ValidationAsset]
) -> None:
    """Find the canonical RAO series for each line and zone."""
    expected_external_ids = sorted(
        {asset.external_id + RAO_TIME_SERIES_SUFFIX for asset in assets}
    )
    if not expected_external_ids:
        return

    api = CogniteCoreClient(client).cognite_time_series
    series_by_external_id: dict[str, list[Any]] = defaultdict(list)
    for batch in _batches(expected_external_ids, INSTANCE_FILTER_BATCH_SIZE):
        series = api.query_all_pages(
            filters=cast(Any, {"externalId": {"in_": list(batch)}}),
            include=["assets"],
        )
        for item in series:
            series_by_external_id[item.external_id].append(item)

    for asset in assets:
        expected_id = asset.external_id + RAO_TIME_SERIES_SUFFIX
        candidates = series_by_external_id.get(expected_id, [])
        if not candidates:
            asset.alerts.append("RAO series not found")
            continue
        if len(candidates) > 1:
            asset.alerts.append("multiple RAO series with canonical external ID")
        # Prefer an instance whose assets relation points back to this asset.
        asset_ref = (asset.space, asset.external_id)
        matching = [
            item
            for item in candidates
            if any(_reference_key(ref) == asset_ref for ref in item.assets)
        ]
        chosen = matching[0] if matching else candidates[0]
        asset.rao_series = chosen
        asset.rao_id = NodeId(space=chosen.space, external_id=chosen.external_id)
        if chosen.assets and not matching:
            asset.alerts.append("RAO asset relation does not match asset")


def _read_rao_samples(
    client: CogniteClient,
    assets: Sequence[ValidationAsset],
    start: datetime,
    end: datetime,
) -> None:
    """Read up to 20 raw RAO points spread across the requested window."""
    targets = [asset for asset in assets if asset.rao_id is not None]
    if not targets:
        return
    duration_ms = int((end - start).total_seconds() * 1_000)
    query_specs: list[tuple[ValidationAsset, DatapointsQuery]] = []
    for asset in targets:
        for sample_index in range(SAMPLE_POINTS_PER_ASSET):
            window_start = start + timedelta(
                milliseconds=duration_ms * sample_index // SAMPLE_POINTS_PER_ASSET
            )
            window_end = start + timedelta(
                milliseconds=duration_ms * (sample_index + 1) // SAMPLE_POINTS_PER_ASSET
            )
            if window_start >= window_end:
                continue
            query_specs.append(
                (
                    asset,
                    DatapointsQuery(
                        instance_id=cast(NodeId, asset.rao_id),
                        start=window_start,
                        end=window_end,
                        limit=1,
                    ),
                )
            )

    for batch in _batches(query_specs, DATAPOINT_QUERY_BATCH_SIZE):
        response = client.time_series.data.retrieve(
            instance_id=[query for _, query in batch],
            ignore_unknown_ids=True,
            ignore_bad_datapoints=False,
            treat_uncertain_as_bad=False,
        )
        series_ids = list(
            dict.fromkeys(_reference_key(asset.rao_id) for asset, _ in batch)
        )
        for series_key in series_ids:
            matching_specs = [
                (asset, query)
                for asset, query in batch
                if _reference_key(asset.rao_id) == series_key
            ]
            returned = response.get(
                instance_id=cast(NodeId, matching_specs[0][0].rao_id)
            )
            if returned is None:
                continue
            datapoint_groups = returned if isinstance(returned, list) else [returned]
            for (asset, _), datapoints in zip(matching_specs, datapoint_groups):
                asset.sample_points.extend(cast(Iterable[Any], datapoints))

    for asset in targets:
        asset.sample_points.sort(key=lambda point: point.timestamp)
        asset.sample_points = asset.sample_points[:SAMPLE_POINTS_PER_ASSET]
        if asset.sample_points:
            asset.first_timestamp = min(
                int(point.timestamp) for point in asset.sample_points
            )


def _read_daily_coverage(
    client: CogniteClient,
    assets: Sequence[ValidationAsset],
    start: datetime,
    end: datetime,
) -> None:
    """Retrieve compact daily count aggregates for the full coverage window."""
    targets = [asset for asset in assets if asset.rao_id is not None]
    if not targets:
        return
    queries = [
        DatapointsQuery(
            instance_id=cast(NodeId, asset.rao_id),
            aggregates="count",
            granularity="1d",
            start=start,
            end=end,
            limit=DATAPOINT_RETRIEVE_LIMIT,
        )
        for asset in targets
    ]
    response = client.time_series.data.retrieve(
        instance_id=queries,
        ignore_unknown_ids=True,
        ignore_bad_datapoints=False,
        treat_uncertain_as_bad=False,
    )
    by_id = {
        _reference_key(result.instance_id): list(cast(Iterable[Any], result))
        for result in cast(Iterable[Any], response)
        if result.instance_id is not None
    }
    for asset in targets:
        asset.daily_counts = {
            int(point.timestamp): int(point.count or 0)
            for point in by_id.get(_reference_key(asset.rao_id), [])
            if point.count is not None and point.count > 0
        }


def _read_latest_timestamps(
    client: CogniteClient, assets: Sequence[ValidationAsset], end: datetime
) -> None:
    targets = [asset for asset in assets if asset.rao_id is not None]
    if not targets:
        return
    latest = client.time_series.data.retrieve_latest(
        instance_id=[cast(NodeId, asset.rao_id) for asset in targets],
        before=end,
        ignore_unknown_ids=True,
        ignore_bad_datapoints=False,
        treat_uncertain_as_bad=False,
    )
    for result in cast(Iterable[Any], latest):
        if result.instance_id is None or result.timestamp is None:
            continue
        asset = next(
            (
                item
                for item in targets
                if _reference_key(item.rao_id) == _reference_key(result.instance_id)
            ),
            None,
        )
        if asset is not None:
            asset.latest_timestamp = _to_epoch_milliseconds(result.timestamp)


def _read_gq_parameter_rows(
    client: CogniteClient,
) -> tuple[ViewId, list[Any]]:
    views = client.data_modeling.views.list(
        limit=-1,
        space=KPI_PARAMETER_VALUE_VIEW_SPACE,
        include_inherited_properties=True,
        all_versions=False,
    )
    matches = [
        view
        for view in views
        if view.external_id == KPI_PARAMETER_VALUE_VIEW_EXTERNAL_ID
    ]
    if len(matches) != 1:
        locations = ", ".join(sorted(view.space for view in matches)) or "none"
        raise ValueError(
            f"Expected one accessible {KPI_PARAMETER_VALUE_VIEW_EXTERNAL_ID} view; "
            f"found {len(matches)} in spaces: {locations}. Set "
            "KPI_PARAMETER_VALUE_VIEW_SPACE to disambiguate."
        )
    view = matches[0]
    parameter_property = next(
        (name for name in view.properties if _normalize_name(name) == "parameter"),
        None,
    )
    if parameter_property is None:
        raise ValueError(
            f"View {_view_label(view)} has no 'parameter' property. Available: "
            f"{', '.join(sorted(view.properties))}"
        )

    property_ref = [
        view.space,
        f"{view.external_id}/{view.version}",
        parameter_property,
    ]
    rows = list(
        client.data_modeling.instances.list(
            instance_type="node",
            sources=view.as_id(),
            filter=filters.Equals(
                property_ref,
                {
                    "space": KPI_PARAMETER_NODE_SPACE,
                    "externalId": KPI_PARAMETER_NODE_EXTERNAL_ID,
                },
            ),
            limit=-1,
        )
    )
    return view.as_id(), rows


def _attach_gq_series(
    assets: Sequence[ValidationAsset], view_id: ViewId, rows: Sequence[Any]
) -> None:
    """Attach all GQ series referenced for each asset in KpiParameterValue."""
    rows_by_asset: dict[tuple[str, str], list[tuple[NodeId, tuple[str, str]]]] = (
        defaultdict(list)
    )
    for row in rows:
        properties = _view_properties(row, view_id)
        asset_refs: set[tuple[str, str]] = set()
        gq_refs: set[NodeId] = set()
        for name, value in properties.items():
            normalized = _normalize_name(name)
            if normalized == "parameter" and not _parameter_is_gq(value):
                continue
            if (
                ("asset" in normalized or normalized == "entityhierarchy")
                and "timeseries" not in normalized
                and "series" not in normalized
            ):
                asset_refs.update(_references(value, default_space=row.space))
            elif (
                (
                    "timeseries" in normalized
                    or "rawseries" in normalized
                    or normalized.endswith("series")
                )
                and "reducer" not in normalized
            ):
                gq_refs.update(_node_references(value, default_space=row.space))

        # Some view versions expose a generic `value` field as the time-series
        # relation. Consider other non-parameter references only if no obvious
        # time-series property was present.
        if not gq_refs:
            for name, value in properties.items():
                normalized = _normalize_name(name)
                if normalized not in {
                    "value",
                    "parametervalue",
                    "parametervalueid",
                    "rawvalue",
                }:
                    continue
                gq_refs.update(_node_references(value, default_space=row.space))

        if not asset_refs or not gq_refs:
            continue
        for asset_ref in asset_refs:
            for gq_ref in gq_refs:
                matched_assets = [
                    asset
                    for asset in assets
                    if asset.external_id == asset_ref[1]
                    and (not asset_ref[0] or asset.space == asset_ref[0])
                ]
                for asset in matched_assets:
                    rows_by_asset[(asset.space, asset.external_id)].append(
                        (gq_ref, (row.space, row.external_id))
                    )

    for asset in assets:
        rows_for_asset = rows_by_asset.get((asset.space, asset.external_id), [])
        asset.gq_ids = sorted(
            {gq_id for gq_id, _ in rows_for_asset},
            key=lambda item: (item.space, item.external_id),
        )
        asset.gq_links = sorted(
            {link for _, link in rows_for_asset}, key=lambda item: (item[0], item[1])
        )
        if asset.rao_id is not None and not asset.gq_ids:
            asset.alerts.append("no GQ series mapped in KpiParameterValue")


def _read_gq_values(
    client: CogniteClient,
    assets: Sequence[ValidationAsset],
) -> dict[tuple[str, str], dict[int, float]]:
    """Read just the three-minute context for each sampled RAO timestamp."""
    sample_minutes_by_series: dict[tuple[str, str], set[int]] = defaultdict(set)
    series_ids: dict[tuple[str, str], NodeId] = {}
    for asset in assets:
        if not asset.sample_points or not asset.gq_ids:
            continue
        sample_minutes = {
            int(point.timestamp) // MILLISECONDS_PER_MINUTE * MILLISECONDS_PER_MINUTE
            for point in asset.sample_points
        }
        for gq_id in asset.gq_ids:
            key = _reference_key(gq_id)
            series_ids[key] = gq_id
            sample_minutes_by_series[key].update(sample_minutes)

    if not sample_minutes_by_series:
        return {}

    values_by_series: dict[tuple[str, str], dict[int, float]] = {}
    query_specs: list[tuple[tuple[str, str], int, DatapointsQuery]] = []
    for series_key, minutes in sample_minutes_by_series.items():
        for minute in sorted(minutes):
            query_start_ms = (
                minute - (ROLLING_WINDOW_MINUTES - 1) * MILLISECONDS_PER_MINUTE
            )
            query_end_ms = minute + MILLISECONDS_PER_MINUTE
            query_specs.append(
                (
                    series_key,
                    minute,
                    DatapointsQuery(
                        instance_id=series_ids[series_key],
                        aggregates="sum",
                        granularity=GOOD_QUANTITY_GRANULARITY,
                        start=datetime.fromtimestamp(query_start_ms / 1_000, tz=UTC),
                        end=datetime.fromtimestamp(query_end_ms / 1_000, tz=UTC),
                        limit=ROLLING_WINDOW_MINUTES,
                    ),
                )
            )

    # The SDK supports repeated queries for the same series to fetch disjoint
    # periods. Keep each API call bounded and pair each returned result with its
    # corresponding three-minute query in request order.
    for batch in _batches(query_specs, DATAPOINT_QUERY_BATCH_SIZE):
        response = client.time_series.data.retrieve(
            instance_id=[spec[2] for spec in batch],
            ignore_unknown_ids=True,
            ignore_bad_datapoints=False,
            treat_uncertain_as_bad=False,
        )
        for series_key in dict.fromkeys(spec[0] for spec in batch):
            matching_specs = [spec for spec in batch if spec[0] == series_key]
            returned = response.get(instance_id=series_ids[series_key])
            if returned is None:
                continue
            datapoint_groups = returned if isinstance(returned, list) else [returned]
            for (_, target_minute, _), datapoints in zip(
                matching_specs, datapoint_groups
            ):
                bucket_values = values_by_series.setdefault(series_key, {})
                for point in cast(Iterable[Any], datapoints):
                    if point.sum is not None:
                        bucket_values[int(point.timestamp)] = float(point.sum)
    return values_by_series


def _build_sample_rows(
    assets: Sequence[ValidationAsset],
    gq_values: Mapping[tuple[str, str], Mapping[int, float]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for asset in assets:
        gq_by_minute: dict[int, float] = defaultdict(float)
        gq_available_minutes: set[int] = set()
        for gq_id in asset.gq_ids:
            for timestamp, value in gq_values.get(_reference_key(gq_id), {}).items():
                minute = timestamp // MILLISECONDS_PER_MINUTE * MILLISECONDS_PER_MINUTE
                gq_by_minute[minute] += value
                gq_available_minutes.add(minute)

        for point in asset.sample_points:
            timestamp = int(point.timestamp)
            minute = timestamp // MILLISECONDS_PER_MINUTE * MILLISECONDS_PER_MINUTE
            minute_values = [
                gq_by_minute[minute - offset * MILLISECONDS_PER_MINUTE]
                for offset in range(ROLLING_WINDOW_MINUTES)
                if minute - offset * MILLISECONDS_PER_MINUTE in gq_available_minutes
            ]
            calculated = (
                sum(minute_values) / len(minute_values) if minute_values else 0.0
            )
            actual = float(point.value) if point.value is not None else None
            difference = actual - calculated if actual is not None else None
            if not asset.gq_ids:
                status = "GQ MAPPING MISSING"
            elif actual is None:
                status = "RAO VALUE MISSING"
            elif abs(cast(float, difference)) <= VALUE_TOLERANCE:
                status = "OK"
            else:
                status = "MISMATCH"
            rows.append(
                {
                    "line_name": asset.line_name,
                    "line_external_id": asset.line_external_id,
                    "asset_level": asset.level,
                    "asset_name": asset.name,
                    "asset_external_id": asset.external_id,
                    "timestamp_utc": _format_timestamp(timestamp),
                    "rao_external_id": asset.rao_series.external_id
                    if asset.rao_series
                    else "",
                    "gq_time_series_count": len(asset.gq_ids),
                    "gq_sum_t": _sum_or_blank(
                        minute, gq_by_minute, gq_available_minutes
                    ),
                    "gq_sum_t_minus_1": _sum_or_blank(
                        minute - MILLISECONDS_PER_MINUTE,
                        gq_by_minute,
                        gq_available_minutes,
                    ),
                    "gq_sum_t_minus_2": _sum_or_blank(
                        minute - 2 * MILLISECONDS_PER_MINUTE,
                        gq_by_minute,
                        gq_available_minutes,
                    ),
                    "available_gq_minutes_in_window": len(minute_values),
                    "rao_calculated": calculated if asset.gq_ids else None,
                    "rao_actual": actual,
                    "difference": difference,
                    "validation": status,
                }
            )
    return rows


def _sum_or_blank(
    timestamp: int,
    values: Mapping[int, float],
    available: set[int],
) -> float | str:
    minute = timestamp // MILLISECONDS_PER_MINUTE * MILLISECONDS_PER_MINUTE
    return values[minute] if minute in available else ""


def _create_alerts(
    assets: Sequence[ValidationAsset], start: datetime, end: datetime
) -> None:
    expected_minutes = max(1, int((end - start).total_seconds() // 60))
    start_ms = int(start.timestamp() * 1_000)
    end_ms = int(end.timestamp() * 1_000)
    for asset in assets:
        if asset.rao_id is None:
            continue
        total_points = sum(asset.daily_counts.values())
        coverage_percent = min(100.0, total_points / expected_minutes * 100)
        if total_points == 0:
            asset.alerts.append("no RAO datapoints in period")
            continue
        if coverage_percent < MINIMUM_COVERAGE_PERCENT:
            asset.alerts.append(
                f"low point coverage ({coverage_percent:.1f}% < "
                f"{MINIMUM_COVERAGE_PERCENT:.1f}%)"
            )
        if asset.first_timestamp is not None and asset.first_timestamp > (
            start_ms + int(MAXIMUM_START_DELAY.total_seconds() * 1_000)
        ):
            asset.alerts.append("first RAO point starts late")
        if asset.latest_timestamp is not None and asset.latest_timestamp < (
            end_ms - int(MAXIMUM_LAST_POINT_AGE.total_seconds() * 1_000)
        ):
            asset.alerts.append("latest RAO point is stale")


def _write_workbook(
    site: Any,
    lines: Sequence[Any],
    assets: Sequence[ValidationAsset],
    sample_rows: Sequence[Mapping[str, Any]],
    start: datetime,
    end: datetime,
) -> Path:
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)
    filename = OUTPUT_FILENAME or (
        f"rolling_average_validation_{_safe_filename(SITE_EXTERNAL_ID)}.xlsx"
    )
    if Path(filename).name != filename or not filename.lower().endswith(".xlsx"):
        raise ValueError("OUTPUT_FILENAME must be an .xlsx filename without a path.")
    output_path = OUTPUT_DIRECTORY / filename

    workbook = Workbook()
    summary = workbook.active
    summary.title = "Summary"
    _write_summary_sheet(summary, site, lines, assets, start, end)

    coverage = workbook.create_sheet("Asset Coverage")
    _write_asset_coverage_sheet(coverage, assets, start, end)

    samples = workbook.create_sheet("Sample Points")
    _write_table_sheet(
        samples,
        list(sample_rows[0].keys()) if sample_rows else _sample_headers(),
        sample_rows,
    )

    mapping_rows = _gq_mapping_rows(assets)
    mapping = workbook.create_sheet("GQ Mapping")
    _write_table_sheet(mapping, _mapping_headers(), mapping_rows)

    workbook.save(output_path)
    return output_path


def _write_summary_sheet(
    worksheet: Any,
    site: Any,
    lines: Sequence[Any],
    assets: Sequence[ValidationAsset],
    start: datetime,
    end: datetime,
) -> None:
    worksheet.append(["Rolling Average Output validation"])
    worksheet.append(["Site", site.name or site.external_id])
    worksheet.append(["Site external ID", site.external_id])
    worksheet.append(
        ["Window UTC", f"{start.isoformat()} to {end.isoformat()} (end exclusive)"]
    )
    worksheet.append(["Expected minimum coverage", MINIMUM_COVERAGE_PERCENT / 100])
    worksheet[5][1].number_format = "0.0%"
    worksheet.append([])
    worksheet.append(["Metric", "Count", "Details"])

    line_assets = [asset for asset in assets if asset.level == "Line"]
    zone_assets = [asset for asset in assets if asset.level == "Zone"]
    metrics = [
        ("Lines on site", len(lines), "Distinct Asset DOM Lines linked to this site"),
        (
            "Lines with at least one RAO point",
            sum(_has_rao_points(asset) for asset in line_assets),
            "Across the requested window",
        ),
        ("Zones in those lines", len(zone_assets), "Distinct per line association"),
        (
            "Zones with at least one RAO point",
            sum(_has_rao_points(asset) for asset in zone_assets),
            "Across the requested window",
        ),
        ("All line/zone assets", len(line_assets) + len(zone_assets), "Assets checked"),
        (
            "Assets with at least one RAO point",
            sum(_has_rao_points(asset) for asset in assets),
            "Across the requested window",
        ),
        (
            "Assets with alerts",
            sum(bool(asset.alerts) for asset in assets),
            "Includes missing mappings and low coverage",
        ),
    ]
    for metric in metrics:
        worksheet.append(list(metric))

    line_table_row = worksheet.max_row + 2
    worksheet.cell(line_table_row, 1, "Line breakdown")
    headers = [
        "Line name",
        "Line external ID",
        "Zones",
        "Zones with RAO",
        "Line has RAO",
        "Line points",
        "Line coverage",
        "Alert",
    ]
    for column, header in enumerate(headers, start=1):
        worksheet.cell(line_table_row + 1, column, header)
    for row_index, line in enumerate(line_assets, start=line_table_row + 2):
        zones = [
            asset for asset in zone_assets if asset.line_external_id == line.external_id
        ]
        worksheet.cell(row_index, 1, line.line_name)
        worksheet.cell(row_index, 2, line.line_external_id)
        worksheet.cell(row_index, 3, len(zones))
        worksheet.cell(row_index, 4, sum(_has_rao_points(asset) for asset in zones))
        worksheet.cell(row_index, 5, "Yes" if _has_rao_points(line) else "No")
        worksheet.cell(row_index, 6, sum(line.daily_counts.values()))
        worksheet.cell(row_index, 7, _coverage_percent(line, start, end) / 100)
        worksheet.cell(row_index, 7).number_format = "0.0%"
        worksheet.cell(row_index, 8, "; ".join(line.alerts))

    _format_worksheet(worksheet)
    _style_header_row(worksheet, 7)
    _style_header_row(worksheet, line_table_row + 1)
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF", size=15)
        cell.fill = PatternFill("solid", fgColor="17365D")
    worksheet.row_dimensions[1].height = 28
    worksheet.column_dimensions["A"].width = 34
    worksheet.column_dimensions["B"].width = 50
    worksheet.column_dimensions["C"].width = 55
    worksheet.column_dimensions["H"].width = 54


def _write_asset_coverage_sheet(
    worksheet: Any, assets: Sequence[ValidationAsset], start: datetime, end: datetime
) -> None:
    headers = [
        "Line name",
        "Line external ID",
        "Asset level",
        "Asset name",
        "Asset external ID",
        "Instance space",
        "Expected RAO external ID",
        "RAO series space",
        "RAO datapoints in window",
        "Coverage of expected minutes",
        "First RAO point UTC",
        "Latest RAO point UTC",
        "GQ series mapped",
        "KpiParameterValue rows",
        "Alert",
    ]
    worksheet.append(headers)
    for asset in assets:
        worksheet.append(
            [
                asset.line_name,
                asset.line_external_id,
                asset.level,
                asset.name,
                asset.external_id,
                asset.space,
                asset.external_id + RAO_TIME_SERIES_SUFFIX,
                asset.rao_series.space if asset.rao_series else "",
                sum(asset.daily_counts.values()),
                _coverage_percent(asset, start, end) / 100,
                _format_timestamp(asset.first_timestamp)
                if asset.first_timestamp
                else "",
                _format_timestamp(asset.latest_timestamp)
                if asset.latest_timestamp
                else "",
                len(asset.gq_ids),
                len(asset.gq_links),
                "; ".join(dict.fromkeys(asset.alerts)),
            ]
        )
    _format_worksheet(worksheet)
    _highlight_alerts(worksheet, 15)
    worksheet.column_dimensions["A"].width = 30
    worksheet.column_dimensions["B"].width = 46
    worksheet.column_dimensions["D"].width = 28
    worksheet.column_dimensions["E"].width = 46
    worksheet.column_dimensions["G"].width = 55
    worksheet.column_dimensions["K"].width = 29
    worksheet.column_dimensions["L"].width = 29
    worksheet.column_dimensions["O"].width = 54
    for row in range(2, worksheet.max_row + 1):
        worksheet.cell(row, 10).number_format = "0.0%"


def _write_table_sheet(
    worksheet: Any,
    headers: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
) -> None:
    worksheet.append(list(headers))
    for row in rows:
        worksheet.append([row.get(header, "") for header in headers])
    _format_worksheet(worksheet)
    if "validation" in headers:
        validation_column = list(headers).index("validation") + 1
        for row_index in range(2, worksheet.max_row + 1):
            cell = worksheet.cell(row_index, validation_column)
            if cell.value == "OK":
                cell.fill = PatternFill("solid", fgColor="E2F0D9")
            elif cell.value:
                cell.fill = PatternFill("solid", fgColor="FCE4D6")
    for column_index, header in enumerate(headers, start=1):
        width = max(16, min(46, len(header) + 3))
        if "external_id" in header:
            width = 53
        elif header.endswith("_utc"):
            width = 29
        worksheet.column_dimensions[get_column_letter(column_index)].width = width
        if header in {
            "rao_calculated",
            "rao_actual",
            "difference",
            "gq_sum_t",
            "gq_sum_t_minus_1",
            "gq_sum_t_minus_2",
        }:
            for row_index in range(2, worksheet.max_row + 1):
                worksheet.cell(row_index, column_index).number_format = "0.0000"


def _format_worksheet(worksheet: Any) -> None:
    header_fill = PatternFill("solid", fgColor="1F4E78")
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    worksheet.row_dimensions[1].height = 32
    for row in worksheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def _style_header_row(worksheet: Any, row_index: int) -> None:
    fill = PatternFill("solid", fgColor="1F4E78")
    for cell in worksheet[row_index]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = fill
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    worksheet.row_dimensions[row_index].height = 30


def _highlight_alerts(worksheet: Any, column_index: int) -> None:
    alert_fill = PatternFill("solid", fgColor="FCE4D6")
    for row_index in range(2, worksheet.max_row + 1):
        cell = worksheet.cell(row_index, column_index)
        if cell.value:
            cell.fill = alert_fill


def _gq_mapping_rows(assets: Sequence[ValidationAsset]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for asset in assets:
        if asset.gq_ids:
            for gq_id in asset.gq_ids:
                rows.append(
                    {
                        "line_name": asset.line_name,
                        "asset_level": asset.level,
                        "asset_name": asset.name,
                        "asset_external_id": asset.external_id,
                        "kpi_parameter_value_rows": len(asset.gq_links),
                        "gq_time_series_space": gq_id.space,
                        "gq_time_series_external_id": gq_id.external_id,
                    }
                )
        else:
            rows.append(
                {
                    "line_name": asset.line_name,
                    "asset_level": asset.level,
                    "asset_name": asset.name,
                    "asset_external_id": asset.external_id,
                    "kpi_parameter_value_rows": len(asset.gq_links),
                    "gq_time_series_space": "",
                    "gq_time_series_external_id": "NOT FOUND",
                }
            )
    return rows


def _mapping_headers() -> list[str]:
    return [
        "line_name",
        "asset_level",
        "asset_name",
        "asset_external_id",
        "kpi_parameter_value_rows",
        "gq_time_series_space",
        "gq_time_series_external_id",
    ]


def _sample_headers() -> list[str]:
    return [
        "line_name",
        "line_external_id",
        "asset_level",
        "asset_name",
        "asset_external_id",
        "timestamp_utc",
        "rao_external_id",
        "gq_time_series_count",
        "gq_sum_t",
        "gq_sum_t_minus_1",
        "gq_sum_t_minus_2",
        "available_gq_minutes_in_window",
        "rao_calculated",
        "rao_actual",
        "difference",
        "validation",
    ]


def _view_properties(row: Any, view_id: ViewId) -> Mapping[str, Any]:
    properties = row.properties or {}
    # Cognite's Properties mapping accepts ViewId identifiers, not the display
    # string returned by _view_label(). Passing that string to .get() makes the
    # SDK try to parse it as a ViewId and raises TypeError.
    return properties.get(view_id, {})


def _parameter_is_gq(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().upper() == KPI_PARAMETER_NAME.upper()
    refs = _references(value)
    return any(
        external_id.rsplit("-", 1)[-1].upper() == KPI_PARAMETER_NAME.upper()
        for _, external_id in refs
    )


def _references(value: Any, *, default_space: str = "") -> set[tuple[str, str]]:
    refs: set[tuple[str, str]] = set()
    if value is None:
        return refs
    if isinstance(value, (list, tuple, set)):
        for item in value:
            refs.update(_references(item, default_space=default_space))
        return refs
    if isinstance(value, Mapping):
        space = value.get("space", default_space)
        external_id = value.get("externalId", value.get("external_id"))
        if external_id is not None:
            refs.add((str(space), str(external_id)))
        return refs
    if hasattr(value, "external_id"):
        return {(str(getattr(value, "space", default_space)), str(value.external_id))}
    if isinstance(value, str):
        return {("", value)} if value else set()
    return refs


def _node_references(value: Any, *, default_space: str = "") -> set[NodeId]:
    return {
        NodeId(space=space or _fallback_gq_space(), external_id=external_id)
        for space, external_id in _references(value, default_space=default_space)
        if external_id
    }


def _fallback_gq_space() -> str:
    # A reference usually carries its own space. This fallback is only used for
    # a string external ID exposed by an older view version.
    return GQ_TIME_SERIES_DEFAULT_SPACE


def _reference_key(reference: Any) -> tuple[str, str]:
    if reference is None:
        return "", ""
    return str(getattr(reference, "space", "")), str(
        getattr(reference, "external_id", "")
    )


def _coverage_percent(asset: ValidationAsset, start: datetime, end: datetime) -> float:
    expected_minutes = max(1, int((end - start).total_seconds() // 60))
    return min(100.0, sum(asset.daily_counts.values()) / expected_minutes * 100)


def _has_rao_points(asset: ValidationAsset) -> bool:
    return sum(asset.daily_counts.values()) > 0


def _to_epoch_milliseconds(value: datetime | int) -> int:
    if isinstance(value, int):
        return value
    timestamp = value if value.tzinfo is not None else value.replace(tzinfo=UTC)
    return int(timestamp.timestamp() * 1_000)


def _format_timestamp(timestamp: int) -> str:
    return (
        datetime.fromtimestamp(timestamp / 1_000, tz=UTC)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _view_label(view_id: Any) -> str:
    return f"{view_id.space}/{view_id.external_id}/{view_id.version}"


def _safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_.-") or "site"


def _batches(items: Sequence[Any], batch_size: int) -> Iterable[Sequence[Any]]:
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]


def _print_result(
    site: Any,
    lines: Sequence[Any],
    assets: Sequence[ValidationAsset],
    view_id: ViewId,
    output_path: Path,
    start: datetime,
    end: datetime,
) -> None:
    line_assets = [asset for asset in assets if asset.level == "Line"]
    zone_assets = [asset for asset in assets if asset.level == "Zone"]
    print(f"Site: {site.external_id} ({site.space})")
    print(f"Window UTC: {start.isoformat()} to {end.isoformat()} (end exclusive)")
    print(
        f"KpiParameterValue view: {_view_label(view_id)}; parameter={KPI_PARAMETER_NAME}"
    )
    print(
        f"Lines: {len(lines)}; with RAO points: {sum(_has_rao_points(asset) for asset in line_assets)}"
    )
    print(
        f"Zones: {len(zone_assets)}; with RAO points: {sum(_has_rao_points(asset) for asset in zone_assets)}"
    )
    print(f"Assets with alerts: {sum(bool(asset.alerts) for asset in assets)}")
    print(f"Excel saved to: {output_path}")


if __name__ == "__main__":
    main()
