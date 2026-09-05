"""Count OT time series with datapoints for one service/subservice pair.

Edit the constants below, then run this file from the repository root.
"""

from __future__ import annotations

from datetime import UTC, datetime
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Literal, Protocol, cast

from cognite.client import CogniteClient
from cognite.client.data_classes.datapoints import (
    DatapointsQuery,
    LatestDatapointQuery,
)
from cognite.client.data_classes.data_modeling import NodeId
from industrial_model import InstanceId

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client, generate_csv
from core.data.ot_dom import OtClient
from core.data.ot_dom.curated_time_series.filters import CuratedTimeSeriesFilter
from core.data.ot_dom.models import CuratedTimeSeries, RawTimeSeries
from core.data.ot_dom.raw_time_series.filters import RawTimeSeriesFilter

# --- Configuration ---------------------------------------------------------
# Choose which OT view to inspect: "raw" or "curated".
TIME_SERIES_KIND: Literal["raw", "curated"] = "curated"

# These are the external IDs of the OT TimeSeriesService and
# TimeSeriesSubservice instances to inspect.
SERVICE_EXTERNAL_ID = "TSSE-GC"
SUBSERVICE_EXTERNAL_ID = "TSSS-GC-DLT"

# CDF retrieves latest datapoints in batches. Keep this at or below 1,000.
BATCH_SIZE = 1_000

# Print the external IDs of time series that have no datapoints.
PRINT_TIME_SERIES_WITHOUT_DATAPOINTS = False

# When enabled, show the percentage of intervals with at least one datapoint
# for every matching time series in this time window.
PRINT_TIME_SERIES_TIME_COVERAGE = True
WINDOW_START = datetime(2026, 1, 1, tzinfo=UTC)
WINDOW_END = datetime(2026, 9, 1, tzinfo=UTC)
# Use "1d" for daily coverage or "1mo" for monthly coverage.
COVERAGE_GRANULARITY: Literal["1d", "1mo"] = "1mo"
TIME_COVERAGE_CSV_FILENAME = "time_series_coverage.csv"

# Asset external ID prefixes used to resolve the asset marked by LeafAssetType.
LEAF_ASSET_PREFIX_BY_LEVEL = {
    "Machine": "MCH",
    "System": "SYS",
    "Zone": "ZNE",
}
# ---------------------------------------------------------------------------


class LatestDatapointResponse(Protocol):
    """Fields used from one item returned by ``retrieve_latest``."""

    instance_id: NodeId | None
    timestamp: datetime | None


class AggregateDatapointsResponse(Protocol):
    """Fields used from one aggregate datapoints response."""

    instance_id: NodeId | None
    count: list[int] | None


def main() -> None:
    """Query the selected time series view and report datapoint coverage."""
    _validate_configuration()

    cognite_client = create_cognite_client()
    ot_client = OtClient(cognite_client)
    time_series = _query_time_series(ot_client)
    time_series_ids = [NodeId(item.space, item.external_id) for item in time_series]
    asset_metadata_by_time_series = _asset_metadata_by_time_series(time_series)
    ids_with_datapoints = _ids_with_datapoints(cognite_client, time_series_ids)

    missing_ids = [
        time_series_id
        for time_series_id in time_series_ids
        if _id_key(time_series_id) not in ids_with_datapoints
    ]
    total = len(time_series_ids)
    with_datapoints = total - len(missing_ids)
    any_datapoint_coverage = with_datapoints / total * 100 if total else 0.0

    print(f"Time series kind: {TIME_SERIES_KIND}")
    print(f"Service external ID: {SERVICE_EXTERNAL_ID}")
    print(f"Subservice external ID: {SUBSERVICE_EXTERNAL_ID}")
    print(f"Matching time series: {total}")
    print(f"With datapoints: {with_datapoints}")
    print(f"Without datapoints: {len(missing_ids)}")
    print(f"Time series with any datapoint: {any_datapoint_coverage:.2f}%")

    if PRINT_TIME_SERIES_WITHOUT_DATAPOINTS and missing_ids:
        print("\nTime series without datapoints:")
        for time_series_id in missing_ids:
            print(f"- {time_series_id.space}/{time_series_id.external_id}")

    if PRINT_TIME_SERIES_TIME_COVERAGE:
        _write_time_coverage_csv(
            cognite_client,
            time_series_ids,
            asset_metadata_by_time_series,
        )


def _query_time_series(ot_client: OtClient) -> list[RawTimeSeries | CuratedTimeSeries]:
    if TIME_SERIES_KIND == "raw":
        raw_filters: RawTimeSeriesFilter = {
            "timeSeriesService": {"externalId": {"eq": SERVICE_EXTERNAL_ID}},
            "timeSeriesSubservice": {"externalId": {"eq": SUBSERVICE_EXTERNAL_ID}},
        }
        return list(ot_client.raw_time_series.query_all_pages(filters=raw_filters))

    curated_filters: CuratedTimeSeriesFilter = {
        "timeSeriesService": {"externalId": {"eq": SERVICE_EXTERNAL_ID}},
        "timeSeriesSubservice": {"externalId": {"eq": SUBSERVICE_EXTERNAL_ID}},
    }
    return list(ot_client.curated_time_series.query_all_pages(filters=curated_filters))


def _ids_with_datapoints(
    cognite_client: CogniteClient, ids: Sequence[NodeId]
) -> set[tuple[str, str]]:
    ids_with_datapoints: set[tuple[str, str]] = set()
    for start in range(0, len(ids), BATCH_SIZE):
        batch: list[NodeId | LatestDatapointQuery] = []
        batch.extend(ids[start : start + BATCH_SIZE])
        response = cognite_client.time_series.data.retrieve_latest(
            instance_id=batch,
            ignore_bad_datapoints=False,
            treat_uncertain_as_bad=False,
            ignore_unknown_ids=True,
        )
        latest_datapoints = cast(Sequence[LatestDatapointResponse], response)
        for datapoint in latest_datapoints:
            if datapoint.instance_id is not None and datapoint.timestamp is not None:
                ids_with_datapoints.add(_id_key(datapoint.instance_id))
    return ids_with_datapoints


def _write_time_coverage_csv(
    cognite_client: CogniteClient,
    ids: Sequence[NodeId],
    asset_metadata_by_time_series: dict[tuple[str, str], tuple[str | None, str | None]],
) -> None:
    expected_intervals = _expected_intervals()
    intervals_with_data = _intervals_with_data(cognite_client, ids)
    total_intervals = len(ids) * expected_intervals
    covered_intervals = sum(intervals_with_data.values())
    overall_coverage = (
        covered_intervals / total_intervals * 100 if total_intervals else 0.0
    )

    rows: list[dict[str, object]] = []
    for time_series_id in ids:
        covered = intervals_with_data.get(_id_key(time_series_id), 0)
        coverage = covered / expected_intervals * 100
        asset_level, asset_external_id = asset_metadata_by_time_series.get(
            _id_key(time_series_id), (None, None)
        )
        rows.append(
            {
                "space": time_series_id.space,
                "external_id": time_series_id.external_id,
                "asset_level": asset_level,
                "asset_external_id": asset_external_id,
                "time_series_kind": TIME_SERIES_KIND,
                "service_external_id": SERVICE_EXTERNAL_ID,
                "subservice_external_id": SUBSERVICE_EXTERNAL_ID,
                "window_start": WINDOW_START.isoformat(),
                "window_end": WINDOW_END.isoformat(),
                "coverage_granularity": COVERAGE_GRANULARITY,
                "intervals_with_data": covered,
                "expected_intervals": expected_intervals,
                "coverage_percent": _format_percentage(coverage),
            }
        )

    output_path = generate_csv(
        filename=TIME_COVERAGE_CSV_FILENAME,
        fieldnames=(
            "space",
            "external_id",
            "asset_level",
            "asset_external_id",
            "time_series_kind",
            "service_external_id",
            "subservice_external_id",
            "window_start",
            "window_end",
            "coverage_granularity",
            "intervals_with_data",
            "expected_intervals",
            "coverage_percent",
        ),
        rows=rows,
    )
    print(
        "\nTime coverage: "
        f"{covered_intervals}/{total_intervals} intervals ({overall_coverage:.2f}%)."
    )
    print(f"CSV saved to: {output_path}")


def _asset_metadata_by_time_series(
    time_series: Sequence[RawTimeSeries | CuratedTimeSeries],
) -> dict[tuple[str, str], tuple[str | None, str | None]]:
    return {
        (item.space, item.external_id): _leaf_asset_metadata(item.tags, item.assets)
        for item in time_series
    }


def _leaf_asset_metadata(
    tags: Sequence[str], assets: Sequence[InstanceId]
) -> tuple[str | None, str | None]:
    asset_level = next(
        (
            tag.removeprefix("LeafAssetType:")
            for tag in tags
            if tag.startswith("LeafAssetType:")
        ),
        None,
    )
    if asset_level is None:
        return None, None

    prefix = LEAF_ASSET_PREFIX_BY_LEVEL.get(asset_level)
    if prefix is None:
        return asset_level, None

    asset_external_id = next(
        (
            asset.external_id
            for asset in assets
            if asset.external_id.startswith(f"{prefix}-")
        ),
        None,
    )
    return asset_level, asset_external_id


def _intervals_with_data(
    cognite_client: CogniteClient, ids: Sequence[NodeId]
) -> dict[tuple[str, str], int]:
    intervals_with_data: dict[tuple[str, str], int] = {}
    for start in range(0, len(ids), BATCH_SIZE):
        batch: list[NodeId | DatapointsQuery] = []
        batch.extend(ids[start : start + BATCH_SIZE])
        response = cognite_client.time_series.data.retrieve(
            instance_id=batch,
            start=WINDOW_START,
            end=WINDOW_END,
            aggregates="count",
            granularity=COVERAGE_GRANULARITY,
            limit=_expected_intervals(),
            ignore_bad_datapoints=False,
            treat_uncertain_as_bad=False,
            ignore_unknown_ids=True,
        )
        datapoints = cast(Sequence[AggregateDatapointsResponse], response)
        for datapoint in datapoints:
            if datapoint.instance_id is None:
                continue
            intervals_with_data[_id_key(datapoint.instance_id)] = sum(
                count > 0 for count in datapoint.count or []
            )
    return intervals_with_data


def _expected_intervals() -> int:
    if COVERAGE_GRANULARITY == "1d":
        return (WINDOW_END - WINDOW_START).days
    return (WINDOW_END.year - WINDOW_START.year) * 12 + (
        WINDOW_END.month - WINDOW_START.month
    )


def _format_percentage(value: float) -> str:
    formatted = f"{value:.2f}".rstrip("0").rstrip(".").replace(".", ",")
    return f"{formatted}%"


def _id_key(instance_id: NodeId) -> tuple[str, str]:
    return instance_id.space, instance_id.external_id


def _validate_configuration() -> None:
    if TIME_SERIES_KIND not in {"raw", "curated"}:
        raise ValueError('TIME_SERIES_KIND must be "raw" or "curated".')
    if SERVICE_EXTERNAL_ID.startswith("REPLACE_WITH_"):
        raise ValueError("Set SERVICE_EXTERNAL_ID at the top of this script.")
    if SUBSERVICE_EXTERNAL_ID.startswith("REPLACE_WITH_"):
        raise ValueError("Set SUBSERVICE_EXTERNAL_ID at the top of this script.")
    if BATCH_SIZE < 1 or BATCH_SIZE > 1_000:
        raise ValueError("BATCH_SIZE must be between 1 and 1,000.")
    if WINDOW_START.tzinfo is None or WINDOW_END.tzinfo is None:
        raise ValueError("WINDOW_START and WINDOW_END must include a timezone.")
    if WINDOW_END <= WINDOW_START:
        raise ValueError("WINDOW_END must be after WINDOW_START.")
    if COVERAGE_GRANULARITY not in {"1d", "1mo"}:
        raise ValueError('COVERAGE_GRANULARITY must be "1d" or "1mo".')
    if COVERAGE_GRANULARITY == "1mo" and (WINDOW_START.day != 1 or WINDOW_END.day != 1):
        raise ValueError(
            "Monthly coverage requires WINDOW_START and WINDOW_END on the first day of a month."
        )


if __name__ == "__main__":
    main()
