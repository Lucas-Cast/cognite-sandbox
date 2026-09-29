"""Delete datapoints from CogniteTimeSeries selected by any exact tag.

This script deletes datapoints only. It does not delete the CogniteTimeSeries
nodes themselves. Review the matched time series with ``DRY_RUN = True``
before setting it to ``False``.

Run from the repository root:

    uv run python src/scripts/delete_cognite_timeseries_datapoints_by_tag.py
"""

from __future__ import annotations

import sys
from collections.abc import Iterator, Sequence
from datetime import UTC, datetime
from pathlib import Path

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import NodeId

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client
from core.data.cognite_core import CogniteCoreClient
from core.data.cognite_core.cognite_time_series.filters import CogniteTimeSeriesFilter
from core.data.cognite_core.models import CogniteTimeSeries

# --- Configuration ---------------------------------------------------------
# A time series is selected when it contains at least one exact tag below.
TIME_SERIES_TAGS: list[str] = ["Kpi:RUP:1m", "KpiParameter:RUP"]

# Optional instance-space restriction. Leave None to search every accessible
# instance space that contains the configured tag.
TIME_SERIES_SPACE: str | None = "sp_evt_glb_dat"

# Set to True to list the selected time series without deleting datapoints.
DRY_RUN = True

# The CDF datapoints API supports the range from 1900 through 2050. The end is
# exclusive, so this covers every supported timestamp before 2050-01-01 UTC.
DELETE_START = datetime(1900, 1, 1, tzinfo=UTC)
DELETE_END = datetime(2050, 1, 1, tzinfo=UTC)

# The deletion API accepts up to 10,000 ranges in one request. Smaller batches
# make progress reporting and recovery from an API error clearer.
DELETE_BATCH_SIZE = 1_000
# ---------------------------------------------------------------------------


def main() -> None:
    """Find tagged time series and delete their datapoints when enabled."""
    time_series_tags = _validate_configuration()
    cognite_client = create_cognite_client()
    time_series = _find_time_series(cognite_client, time_series_tags)

    _print_matches(time_series, time_series_tags)
    if DRY_RUN:
        print("\nDry run enabled: no datapoints were deleted.")
        print("Set DRY_RUN = False to allow deletion.")
        return
    if not time_series:
        print("\nNothing to delete.")
        return

    _delete_datapoints(cognite_client, time_series)
    print(f"\nDeleted datapoints from {len(time_series)} CogniteTimeSeries node(s).")


def _find_time_series(
    cognite_client: CogniteClient,
    time_series_tags: Sequence[str],
) -> list[CogniteTimeSeries]:
    """Return CDF time series that contain any configured exact tag."""
    filters: CogniteTimeSeriesFilter = {
        "tags": {"containsAny": list(time_series_tags)},
    }
    if TIME_SERIES_SPACE is not None:
        filters["space"] = {"eq": TIME_SERIES_SPACE}
    return CogniteCoreClient(cognite_client).cognite_time_series.query_all_pages(
        filters=filters
    )


def _print_matches(
    time_series: Sequence[CogniteTimeSeries],
    time_series_tags: Sequence[str],
) -> None:
    print(f"Tags exatas (qualquer uma): {', '.join(time_series_tags)}")
    print(f'Instance space: "{TIME_SERIES_SPACE or "all"}"')
    print(f"CogniteTimeSeries encontradas: {len(time_series)}")
    for item in time_series:
        name = item.name or "(sem nome)"
        print(f"- {item.space}/{item.external_id} | {name}")


def _delete_datapoints(
    cognite_client: CogniteClient,
    time_series: Sequence[CogniteTimeSeries],
) -> None:
    """Delete datapoints over the full supported timestamp range in batches."""
    deleted = 0
    for batch in _batches(time_series, DELETE_BATCH_SIZE):
        cognite_client.time_series.data.delete_ranges(
            [
                {
                    "instance_id": NodeId(item.space, item.external_id),
                    "start": DELETE_START,
                    "end": DELETE_END,
                }
                for item in batch
            ]
        )
        deleted += len(batch)
        print(f"Deleted datapoints from {deleted}/{len(time_series)} time series.")


def _validate_configuration() -> list[str]:
    time_series_tags = [tag.strip() for tag in TIME_SERIES_TAGS]
    if not time_series_tags or any(not tag for tag in time_series_tags):
        raise ValueError("Set TIME_SERIES_TAGS with at least one non-empty exact tag.")
    if len(set(time_series_tags)) != len(time_series_tags):
        raise ValueError("TIME_SERIES_TAGS must not contain duplicate tags.")
    if TIME_SERIES_SPACE is not None and not TIME_SERIES_SPACE.strip():
        raise ValueError("Set TIME_SERIES_SPACE to a non-empty value or None.")
    if DELETE_END <= DELETE_START:
        raise ValueError("DELETE_END must be after DELETE_START.")
    if DELETE_BATCH_SIZE < 1 or DELETE_BATCH_SIZE > 10_000:
        raise ValueError("DELETE_BATCH_SIZE must be between 1 and 10,000.")
    return time_series_tags


def _batches(
    items: Sequence[CogniteTimeSeries], batch_size: int
) -> Iterator[list[CogniteTimeSeries]]:
    for start in range(0, len(items), batch_size):
        yield list(items[start : start + batch_size])


if __name__ == "__main__":
    main()
