"""Preview or delete Cognite Core time series selected by space and exact tag.

The script targets ``CogniteTimeSeries`` nodes in the Cognite Core data model,
not legacy Time Series API resources. Set ``DRY_RUN = True`` to preview the
selection or ``DRY_RUN = False`` to perform the irreversible deletion.

Examples:
    uv run python src/scripts/delete_cognite_timeseries_by_space_and_tag.py
"""

from __future__ import annotations

import sys
from collections.abc import Iterator, Sequence
from pathlib import Path

from cognite.client import CogniteClient

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client
from core.data.cognite_core import CogniteCoreClient
from core.data.cognite_core.cognite_time_series.filters import CogniteTimeSeriesFilter
from core.data.cognite_core.models import CogniteTimeSeries

# Keep node deletion requests small to avoid API timeouts on large graph changes.
NODE_DELETE_BATCH_SIZE = 100

# CDF instance space containing the CogniteTimeSeries nodes.
TIME_SERIES_SPACE = "sp_evt_san_dat"

# Exact tag that every matched CogniteTimeSeries must contain.
TIME_SERIES_TAG = "KpiCode:RUP"

# Set to True to preview the selection without deleting it.
DRY_RUN = False


def main() -> None:
    """Find matching nodes and act according to the configured dry-run mode."""
    _validate_configuration()
    cognite_client = create_cognite_client()
    time_series = _find_time_series(cognite_client, TIME_SERIES_SPACE, TIME_SERIES_TAG)

    _print_matches(time_series, TIME_SERIES_SPACE, TIME_SERIES_TAG)
    if DRY_RUN:
        print("\nDry run enabled: no time series were deleted.")
        print("Set DRY_RUN = False to allow deletion.")
        return

    if not time_series:
        print("\nNothing to delete.")
        return

    _delete_time_series(cognite_client, time_series)
    print(f"\nDeleted {len(time_series)} CogniteTimeSeries node(s).")


def _validate_configuration() -> None:
    if not TIME_SERIES_SPACE:
        raise ValueError("Set TIME_SERIES_SPACE before running the script.")
    if not TIME_SERIES_TAG:
        raise ValueError("Set TIME_SERIES_TAG before running the script.")


def _find_time_series(
    cognite_client: CogniteClient, space: str, tag: str
) -> list[CogniteTimeSeries]:
    """Return time series in ``space`` that contain exactly ``tag``."""
    filters: CogniteTimeSeriesFilter = {
        "space": {"eq": space},
        "tags": {"containsAll": [tag]},
    }
    return CogniteCoreClient(cognite_client).cognite_time_series.query_all_pages(
        filters=filters
    )


def _print_matches(
    time_series: Sequence[CogniteTimeSeries], space: str, tag: str
) -> None:
    print(f'Space: "{space}"')
    print(f'Tag exata: "{tag}"')
    print(f"CogniteTimeSeries encontradas: {len(time_series)}")
    for item in time_series:
        name = item.name or "(sem nome)"
        print(f"- {item.space}/{item.external_id} | {name}")


def _delete_time_series(
    cognite_client: CogniteClient, time_series: Sequence[CogniteTimeSeries]
) -> None:
    """Delete time-series nodes in small batches to avoid API timeouts."""
    instances = cognite_client.data_modeling.instances
    deleted = 0
    for batch in _batches(time_series, NODE_DELETE_BATCH_SIZE):
        node_ids = [(item.space, item.external_id) for item in batch]
        instances.delete(nodes=node_ids)
        deleted += len(batch)
        print(f"Deleted {deleted}/{len(time_series)} node(s).")


def _batches(
    items: Sequence[CogniteTimeSeries], batch_size: int
) -> Iterator[list[CogniteTimeSeries]]:
    for start in range(0, len(items), batch_size):
        yield list(items[start : start + batch_size])


if __name__ == "__main__":
    main()
