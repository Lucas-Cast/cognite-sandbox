"""Insert zero-valued datapoints from each asset's earliest BaseEvent onward.

The script finds numeric CogniteTimeSeries by space and tag, retrieves only
the BaseEvent with the smallest ``startTime`` for each related asset, and
inserts ``0.0`` once per minute from that date onward. Existing datapoints are
not read or preserved.

``START_TIME`` and ``END_TIME`` optionally restrict the write range. When they
are both ``None``, the range is from the earliest event in the full history to
the current UTC time. Keep ``DRY_RUN = True`` for the first run.
"""

from __future__ import annotations

import sys
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import NoneType

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import InstanceSort, NodeId, ViewId

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client
from core.data.cognite_core import CogniteCoreClient
from core.data.cognite_core.cognite_time_series.filters import CogniteTimeSeriesFilter
from core.data.cognite_core.models import CogniteTimeSeries

# --- Configuration ---------------------------------------------------------
# A time series matches when it contains at least one exact tag below.
TIME_SERIES_TAGS: list[str] = ["KpiParameter:RUP"]

# Instance spaces containing the CogniteTimeSeries nodes.
TIME_SERIES_SPACES: list[str] = ["sp_evt_fra_dat", "sp_evt_elp_dat", "sp_evt_san_dat"]

# BaseEvents are searched only in this space. Set None to search all spaces
BASE_EVENT_INSTANCE_SPACE: str | None = None
BASE_EVENT_VIEW = ViewId("sp_evt_glb_dmd", "BaseEvent", "v1.0.0")
BASE_EVENT_ASSETS_PROPERTY = "assets"
BASE_EVENT_START_TIME_PROPERTY = "startTime"
# Window is half-open: START_TIME <= timestamp < END_TIME. Set both to None
# to write from the first BaseEvent in history until the current UTC time.
START_TIME: datetime | None = None
END_TIME: datetime | None = None
INTERVAL = timedelta(minutes=1)

# Always review the planned inserts first. Set False to write zeros to CDF.
DRY_RUN = False

# CDF accepts up to 10,000 datapoints per insert request.
INSERT_BATCH_SIZE = 10_000
# Number of BaseEvents read per chronological page while locating first events.
BASE_EVENT_SCAN_PAGE_SIZE = 1_000
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NodeReference:
    space: str
    external_id: str


@dataclass(frozen=True)
class TimeInterval:
    start_ms: int
    end_ms: int


@dataclass
class FillStats:
    event_intervals: int = 0
    expected_timestamps: int = 0
    inserted_datapoints: int = 0


def main() -> None:
    """Insert zeros in BaseEvent intervals for each time series asset."""
    tags, time_series_spaces = _validate_configuration()
    cognite_client = create_cognite_client()
    _validate_base_event_properties(cognite_client)
    time_series = _find_time_series(cognite_client, tags, time_series_spaces)
    numeric_series, skipped_series = _split_numeric_time_series(time_series)
    assets = _assets_from_time_series(numeric_series)
    print(
        "Searching BaseEvents chronologically for the first event of "
        f"{len(assets)} assets..."
    )
    event_intervals_by_asset = _intervals_from_first_events_by_asset(
        cognite_client, assets
    )

    print(f"Tags exatas (qualquer uma): {', '.join(tags)}")
    print(f"Instance spaces das time series: {', '.join(time_series_spaces)}")
    print(f"Instance space dos BaseEvents: {BASE_EVENT_INSTANCE_SPACE or 'all'}")
    print(
        f"Window UTC: {_format_utc(START_TIME) if START_TIME else 'first event'} to {_format_utc(END_TIME) if END_TIME else 'now'}"
    )
    print(f"Interval: {_format_interval(INTERVAL)}")
    print(f"CogniteTimeSeries encontradas: {len(time_series)}")
    print(f"Séries numéricas: {len(numeric_series)}")
    if skipped_series:
        print(f"Séries ignoradas por não serem numéricas: {len(skipped_series)}")

    total = FillStats()
    for item in numeric_series:
        asset_references = _references(item.assets)
        intervals = _merge_intervals(
            interval
            for asset in asset_references
            for interval in event_intervals_by_asset.get(asset, [])
        )
        stats = _fill_datapoints(cognite_client, item, intervals)
        _add_stats(total, stats)
        print(
            f"{item.space}/{item.external_id}: assets={len(asset_references)}, "
            f"event_intervals={stats.event_intervals}, "
            f"planned={stats.expected_timestamps}, inserted={stats.inserted_datapoints}"
        )

    print(f"Total event intervals: {total.event_intervals}")
    print(f"Total expected timestamps inside events: {total.expected_timestamps}")
    if DRY_RUN:
        print("Dry run enabled: no datapoints were inserted.")
        print("Set DRY_RUN = False to insert zero-valued datapoints.")
    else:
        print(f"Total zero-valued datapoints inserted: {total.inserted_datapoints}")


def _validate_base_event_properties(cognite_client: CogniteClient) -> None:
    views = cognite_client.data_modeling.views.retrieve(
        BASE_EVENT_VIEW,
        include_inherited_properties=True,
        all_versions=False,
    )
    if not views:
        raise ValueError(f"BaseEvent view not found: {_view_label(BASE_EVENT_VIEW)}")
    required = (
        BASE_EVENT_ASSETS_PROPERTY,
        BASE_EVENT_START_TIME_PROPERTY,
    )
    missing = [
        property_name
        for property_name in required
        if property_name not in views[0].properties
    ]
    if missing:
        available = ", ".join(sorted(views[0].properties))
        raise ValueError(
            f"BaseEvent properties not found: {', '.join(missing)}. "
            f"Available properties: {available}"
        )


def _find_time_series(
    cognite_client: CogniteClient,
    tags: Sequence[str],
    time_series_spaces: Sequence[str],
) -> list[CogniteTimeSeries]:
    filters_to_apply: CogniteTimeSeriesFilter = {
        "space": {"in": list(time_series_spaces)},
        "tags": {"containsAny": list(tags)},
    }
    return CogniteCoreClient(cognite_client).cognite_time_series.query_all_pages(
        filters=filters_to_apply
    )


def _split_numeric_time_series(
    time_series: Sequence[CogniteTimeSeries],
) -> tuple[list[CogniteTimeSeries], list[CogniteTimeSeries]]:
    numeric: list[CogniteTimeSeries] = []
    skipped: list[CogniteTimeSeries] = []
    for item in time_series:
        if item.type.lower() == "numeric":
            numeric.append(item)
        else:
            skipped.append(item)
    return numeric, skipped


def _assets_from_time_series(
    time_series: Sequence[CogniteTimeSeries],
) -> list[NodeReference]:
    return sorted(
        {asset for item in time_series for asset in _references(item.assets)},
        key=lambda asset: (asset.space, asset.external_id),
    )


def _intervals_from_first_events_by_asset(
    cognite_client: CogniteClient, assets: Sequence[NodeReference]
) -> dict[NodeReference, list[TimeInterval]]:
    intervals_by_asset: dict[NodeReference, list[TimeInterval]] = {
        asset: [] for asset in assets
    }
    remaining_assets = set(assets)
    first_event_start_by_asset: dict[NodeReference, int] = {}
    for event_page in cognite_client.data_modeling.instances(
        chunk_size=BASE_EVENT_SCAN_PAGE_SIZE,
        instance_type="node",
        sources=BASE_EVENT_VIEW,
        space=BASE_EVENT_INSTANCE_SPACE,
        sort=InstanceSort(
            _base_event_property_reference(BASE_EVENT_START_TIME_PROPERTY),
            nulls_first=False,
        ),
        limit=-1,
    ):
        for event in event_page:
            properties = (
                event.properties.get(BASE_EVENT_VIEW, {}) if event.properties else {}
            )
            event_start_ms = _as_milliseconds(
                properties.get(BASE_EVENT_START_TIME_PROPERTY)
            )
            if event_start_ms is None:
                continue
            for asset in _references(properties.get(BASE_EVENT_ASSETS_PROPERTY)):
                if asset in remaining_assets:
                    first_event_start_by_asset[asset] = event_start_ms
                    remaining_assets.remove(asset)
        if not remaining_assets:
            break

    window_end_ms = _window_end_milliseconds()
    for asset in assets:
        event_start_ms = first_event_start_by_asset.get(asset)
        if event_start_ms is None:
            continue
        window_start_ms = _window_start_milliseconds()
        start_ms = (
            max(event_start_ms, window_start_ms)
            if window_start_ms is not None
            else event_start_ms
        )
        if start_ms < window_end_ms:
            intervals_by_asset[asset].append(TimeInterval(start_ms, window_end_ms))
    return intervals_by_asset


def _fill_datapoints(
    cognite_client: CogniteClient,
    time_series: CogniteTimeSeries,
    intervals: Sequence[TimeInterval],
) -> FillStats:
    stats = FillStats(event_intervals=len(intervals))
    if not intervals:
        return stats

    instance_id = NodeId(time_series.space, time_series.external_id)
    batch: list[tuple[int, float]] = []
    for interval in intervals:
        for timestamp in _timestamps_in_interval(interval):
            stats.expected_timestamps += 1
            batch.append((timestamp, 0.0))
            if len(batch) == INSERT_BATCH_SIZE:
                stats.inserted_datapoints += _insert_batch(
                    cognite_client, instance_id, batch
                )
                batch = []

    if batch:
        stats.inserted_datapoints += _insert_batch(cognite_client, instance_id, batch)
    return stats


def _timestamps_in_interval(interval: TimeInterval) -> Iterator[int]:
    interval_ms = int(INTERVAL.total_seconds() * 1_000)
    offset = interval.start_ms % interval_ms
    timestamp = (
        interval.start_ms if offset == 0 else interval.start_ms + interval_ms - offset
    )
    while timestamp < interval.end_ms:
        yield timestamp
        timestamp += interval_ms


def _merge_intervals(
    intervals: Iterator[TimeInterval] | Sequence[TimeInterval],
) -> list[TimeInterval]:
    ordered = sorted(
        intervals, key=lambda interval: (interval.start_ms, interval.end_ms)
    )
    merged: list[TimeInterval] = []
    for interval in ordered:
        if not merged or interval.start_ms > merged[-1].end_ms:
            merged.append(interval)
            continue
        previous = merged[-1]
        merged[-1] = TimeInterval(
            previous.start_ms, max(previous.end_ms, interval.end_ms)
        )
    return merged


def _insert_batch(
    cognite_client: CogniteClient,
    instance_id: NodeId,
    datapoints: Sequence[tuple[int, float]],
) -> int:
    if DRY_RUN:
        return 0
    cognite_client.time_series.data.insert(datapoints, instance_id=instance_id)
    return len(datapoints)


def _references(value: object) -> list[NodeReference]:
    values = value if isinstance(value, list) else [value]
    return [reference for item in values if (reference := _reference(item))]


def _reference(value: object) -> NodeReference | None:
    if isinstance(value, Mapping):
        space = value.get("space")
        external_id = value.get("externalId", value.get("external_id"))
    else:
        space = getattr(value, "space", None)
        external_id = getattr(value, "external_id", None)
    if isinstance(space, str) and isinstance(external_id, str):
        return NodeReference(space, external_id)
    return None


def _as_milliseconds(value: object) -> int | None:
    if isinstance(value, datetime):
        timestamp = value if value.tzinfo else value.replace(tzinfo=UTC)
        return _datetime_to_milliseconds(timestamp)
    if isinstance(value, str):
        try:
            return _datetime_to_milliseconds(
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            )
        except ValueError:
            return None
    return None


def _base_event_property_reference(property_name: str) -> list[str]:
    return [
        BASE_EVENT_VIEW.space,
        f"{BASE_EVENT_VIEW.external_id}/{BASE_EVENT_VIEW.version}",
        property_name,
    ]


def _batches(
    items: Sequence[NodeReference], batch_size: int
) -> Iterator[Sequence[NodeReference]]:
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]


def _add_stats(total: FillStats, stats: FillStats) -> None:
    total.event_intervals += stats.event_intervals
    total.expected_timestamps += stats.expected_timestamps
    total.inserted_datapoints += stats.inserted_datapoints


def _datetime_to_milliseconds(value: datetime) -> int:
    return int(value.timestamp() * 1_000)


def _window_start_milliseconds() -> int | None:
    return _datetime_to_milliseconds(START_TIME) if START_TIME else None


def _window_end_milliseconds() -> int:
    return _datetime_to_milliseconds(END_TIME or datetime.now(UTC))


def _format_utc(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def _format_interval(value: timedelta) -> str:
    total_seconds = int(value.total_seconds())
    if total_seconds % 60 == 0:
        return f"{total_seconds // 60}m"
    return f"{total_seconds}s"


def _view_label(view: ViewId) -> str:
    return f"{view.space}/{view.external_id}/{view.version}"


def _validate_configuration() -> tuple[list[str], list[str]]:
    tags = [tag.strip() for tag in TIME_SERIES_TAGS]
    if not tags or any(not tag for tag in tags):
        raise ValueError("Set TIME_SERIES_TAGS with one or more non-empty exact tags.")
    if len(set(tags)) != len(tags):
        raise ValueError("TIME_SERIES_TAGS must not contain duplicate tags.")
    spaces = [space.strip() for space in TIME_SERIES_SPACES]
    if not spaces or any(not space for space in spaces):
        raise ValueError("Set TIME_SERIES_SPACES with one or more non-empty spaces.")
    if len(set(spaces)) != len(spaces):
        raise ValueError("TIME_SERIES_SPACES must not contain duplicate spaces.")
    if BASE_EVENT_INSTANCE_SPACE is not None and not BASE_EVENT_INSTANCE_SPACE.strip():
        raise ValueError("Set BASE_EVENT_INSTANCE_SPACE to a non-empty value or None.")
    for name, value in (("START_TIME", START_TIME), ("END_TIME", END_TIME)):
        if value is not None and value.tzinfo is None:
            raise ValueError(f"{name} must include a timezone or be None.")
    if START_TIME is not None and END_TIME is not None and END_TIME <= START_TIME:
        raise ValueError("END_TIME must be after START_TIME.")
    interval_ms = INTERVAL.total_seconds() * 1_000
    if interval_ms <= 0 or not interval_ms.is_integer():
        raise ValueError("INTERVAL must be a positive whole number of milliseconds.")
    if INSERT_BATCH_SIZE < 1 or INSERT_BATCH_SIZE > 10_000:
        raise ValueError("INSERT_BATCH_SIZE must be between 1 and 10,000.")
    if BASE_EVENT_SCAN_PAGE_SIZE < 1:
        raise ValueError("BASE_EVENT_SCAN_PAGE_SIZE must be at least 1.")
    return tags, spaces


if __name__ == "__main__":
    main()
