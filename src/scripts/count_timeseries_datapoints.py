"""Count OT time series with datapoints matching the configured filters.

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
from core.line_asset_tree_service import (
    AssetExternalIdsByLevel,
    LineAssetTreeService,
)

# --- Configuration ---------------------------------------------------------
# Choose which OT view to inspect: "raw" or "curated".
TIME_SERIES_KIND: Literal["raw", "curated"] = "curated"

# These are optional external IDs of the OT TimeSeriesService and
# TimeSeriesSubservice instances to inspect. They are not applied when
# NAME_CONTAINS is set, because CDF search does not support these nested filters.
SERVICE_EXTERNAL_ID = "TSSE-SC"
SUBSERVICE_EXTERNAL_ID = "TSSS-SC-DLT"

# Optional text that must occur anywhere in the time series external ID.
EXTERNAL_ID_CONTAINS = None

# Optional text sent to CDF's full-text search, restricted to the name field.
# CDF matches complete tokens and a prefix for the final token, not arbitrary
# character substrings. Set this when SERVICE_EXTERNAL_ID and
# SUBSERVICE_EXTERNAL_ID are empty.
NAME_CONTAINS: str | None = None

# The CDF search endpoint returns at most 1,000 results.
NAME_SEARCH_LIMIT = 1_000

# Optional Asset DOM Line external ID. When set, the script filters matching
# time series in memory using their asset_external_id, then reports matching
# time series per asset for its Zone, Machine, and System descendants.
LINE_EXTERNAL_ID = "LNE-a33832a03a11376bd957d576abed79de"

# CDF retrieves latest datapoints in batches. Keep this at or below 1,000.
BATCH_SIZE = 1_000

# Print the external IDs of time series that have no datapoints.
PRINT_TIME_SERIES_WITHOUT_DATAPOINTS = False

# When enabled, show the percentage of intervals with at least one datapoint
# for every matching time series in this time window.
PRINT_TIME_SERIES_TIME_COVERAGE = True
WINDOW_START = datetime(2026, 1, 1, tzinfo=UTC)
WINDOW_END = datetime(2026, 10, 1, tzinfo=UTC)
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
    line_asset_external_ids_by_level = (
        LineAssetTreeService(cognite_client).descendant_asset_external_ids(
            LINE_EXTERNAL_ID
        )
        if LINE_EXTERNAL_ID
        else None
    )
    time_series = _query_time_series(ot_client)
    asset_metadata_by_time_series = _asset_metadata_by_time_series(time_series)
    if line_asset_external_ids_by_level is not None:
        time_series = _filter_time_series_by_line_assets(
            time_series,
            asset_metadata_by_time_series,
            line_asset_external_ids_by_level,
        )
        asset_metadata_by_time_series = _asset_metadata_by_time_series(time_series)
    time_series_ids = [
        NodeId(space=item.space, external_id=item.external_id) for item in time_series
    ]
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
    print(f"External ID contains: {EXTERNAL_ID_CONTAINS}")
    print(f"Name search: {NAME_CONTAINS}")
    print(f"Line external ID: {LINE_EXTERNAL_ID}")
    if NAME_CONTAINS:
        print("Service/subservice filters: not applied to CDF name search")
    print(f"Matching time series: {total}")
    print(f"With datapoints: {with_datapoints}")
    print(f"Without datapoints: {len(missing_ids)}")
    print(f"Time series with any datapoint: {any_datapoint_coverage:.2f}%")

    if line_asset_external_ids_by_level is not None:
        _print_line_asset_time_series_summary(
            time_series,
            line_asset_external_ids_by_level,
        )

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
        raw_filters = _raw_time_series_filters()
        time_series = _raw_time_series_query(ot_client, raw_filters)
    else:
        curated_filters = _curated_time_series_filters()
        time_series = _curated_time_series_query(ot_client, curated_filters)

    if NAME_CONTAINS and len(time_series) == NAME_SEARCH_LIMIT:
        raise RuntimeError(
            "The CDF name search reached its 1,000-result limit. Refine the "
            "filters to ensure the count is complete."
        )
    return [item for item in time_series if _matches_external_id_contains(item)]


def _raw_time_series_query(
    ot_client: OtClient,
    filters: RawTimeSeriesFilter,
) -> list[RawTimeSeries]:
    if not NAME_CONTAINS:
        return list(ot_client.raw_time_series.query_all_pages(filters=filters))
    return list(
        ot_client.raw_time_series.search(
            query=NAME_CONTAINS,
            query_properties=["name"],
            query_operator="AND",
            limit=NAME_SEARCH_LIMIT,
        )
    )


def _curated_time_series_query(
    ot_client: OtClient,
    filters: CuratedTimeSeriesFilter,
) -> list[CuratedTimeSeries]:
    if not NAME_CONTAINS:
        return list(ot_client.curated_time_series.query_all_pages(filters=filters))
    return list(
        ot_client.curated_time_series.search(
            query=NAME_CONTAINS,
            query_properties=["name"],
            query_operator="AND",
            limit=NAME_SEARCH_LIMIT,
        )
    )


def _raw_time_series_filters() -> RawTimeSeriesFilter:
    filters: RawTimeSeriesFilter = {}
    if SERVICE_EXTERNAL_ID:
        filters["timeSeriesService"] = {"externalId": {"eq": SERVICE_EXTERNAL_ID}}
    if SUBSERVICE_EXTERNAL_ID:
        filters["timeSeriesSubservice"] = {"externalId": {"eq": SUBSERVICE_EXTERNAL_ID}}
    return filters


def _curated_time_series_filters() -> CuratedTimeSeriesFilter:
    filters: CuratedTimeSeriesFilter = {}
    if SERVICE_EXTERNAL_ID:
        filters["timeSeriesService"] = {"externalId": {"eq": SERVICE_EXTERNAL_ID}}
    if SUBSERVICE_EXTERNAL_ID:
        filters["timeSeriesSubservice"] = {"externalId": {"eq": SUBSERVICE_EXTERNAL_ID}}
    return filters


def _matches_external_id_contains(item: RawTimeSeries | CuratedTimeSeries) -> bool:
    return not EXTERNAL_ID_CONTAINS or EXTERNAL_ID_CONTAINS in item.external_id


def _filter_time_series_by_line_assets(
    time_series: Sequence[RawTimeSeries | CuratedTimeSeries],
    asset_metadata_by_time_series: dict[tuple[str, str], tuple[str | None, str | None]],
    asset_external_ids_by_level: AssetExternalIdsByLevel,
) -> list[RawTimeSeries | CuratedTimeSeries]:
    return [
        item
        for item in time_series
        if _matches_line_asset_metadata(
            asset_metadata_by_time_series[(item.space, item.external_id)],
            asset_external_ids_by_level,
        )
    ]


def _matches_line_asset_metadata(
    asset_metadata: tuple[str | None, str | None],
    asset_external_ids_by_level: AssetExternalIdsByLevel,
) -> bool:
    asset_level, asset_external_id = asset_metadata
    return (
        asset_level is not None
        and asset_external_id in asset_external_ids_by_level.get(asset_level, set())
    )


def _print_line_asset_time_series_summary(
    time_series: Sequence[RawTimeSeries | CuratedTimeSeries],
    asset_external_ids_by_level: AssetExternalIdsByLevel,
) -> None:
    print(f"\nTime series for line {LINE_EXTERNAL_ID} (time series/assets):")
    for asset_level in ("Zone", "Machine", "System"):
        matching_time_series = sum(
            _leaf_asset_level(item.tags) == asset_level for item in time_series
        )
        print(
            f"{asset_level}: "
            f"{matching_time_series}/{len(asset_external_ids_by_level[asset_level])}"
        )


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
                "external_id_contains": EXTERNAL_ID_CONTAINS,
                "name_contains": NAME_CONTAINS,
                "line_external_id": LINE_EXTERNAL_ID,
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
            "external_id_contains",
            "name_contains",
            "line_external_id",
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
    asset_level = _leaf_asset_level(tags)
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


def _leaf_asset_level(tags: Sequence[str]) -> str | None:
    return next(
        (
            tag.removeprefix("LeafAssetType:")
            for tag in tags
            if tag.startswith("LeafAssetType:")
        ),
        None,
    )


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
    return _instance_key(instance_id)


def _instance_key(instance_id: NodeId | InstanceId) -> tuple[str, str]:
    return instance_id.space, instance_id.external_id


def _validate_configuration() -> None:
    if TIME_SERIES_KIND not in {"raw", "curated"}:
        raise ValueError('TIME_SERIES_KIND must be "raw" or "curated".')
    if not any(
        (
            SERVICE_EXTERNAL_ID,
            SUBSERVICE_EXTERNAL_ID,
            EXTERNAL_ID_CONTAINS,
            NAME_CONTAINS,
            LINE_EXTERNAL_ID,
        )
    ):
        raise ValueError(
            "Set SERVICE_EXTERNAL_ID, SUBSERVICE_EXTERNAL_ID, EXTERNAL_ID_CONTAINS, "
            "NAME_CONTAINS, or LINE_EXTERNAL_ID."
        )
    if BATCH_SIZE < 1 or BATCH_SIZE > 1_000:
        raise ValueError("BATCH_SIZE must be between 1 and 1,000.")
    if NAME_SEARCH_LIMIT != 1_000:
        raise ValueError("NAME_SEARCH_LIMIT must be 1,000.")
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
