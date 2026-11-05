"""Print aggregate values by bucket for a configured time series and window.

Edit the constants below, then run:
    uv run python src/scripts/get_timeseries_aggregated_values.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Protocol, cast
from zoneinfo import ZoneInfo

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import NodeId
from cognite.client.data_classes.datapoints import DatapointsQuery

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client
from core.data.cognite_core import CogniteCoreClient

# --- Configuration: edit these values ------------------------------------
TIME_SERIES_EXTERNAL_ID = "ZNE-538382edc95683c1a2cddcaeb442db82-parameter-RUNT"
# Set the instance space if the external ID may exist in multiple spaces.
TIME_SERIES_SPACE: str | None = "sp_evt_san_dat"
AGGREGATION = "sum"
GRANULARITY = "1d"
# Sandy, Utah uses Mountain Time (MST/MDT); ZoneInfo applies DST automatically.
TIME_ZONE = ZoneInfo("America/Denver")
START = datetime(2026, 9, 23, tzinfo=TIME_ZONE)
END = datetime(2026, 9, 24, tzinfo=TIME_ZONE)  # Exclusive.
# --------------------------------------------------------------------------

SUPPORTED_AGGREGATIONS = {
    "average",
    "count",
    "continuousVariance",
    "discreteVariance",
    "interpolation",
    "max",
    "min",
    "stepInterpolation",
    "sum",
    "totalVariation",
}


class AggregateDatapoint(Protocol):
    timestamp: int
    value: float | None


class AggregateResult(Protocol):
    instance_id: NodeId | None

    def __iter__(self) -> object: ...


def main() -> None:
    if not TIME_SERIES_EXTERNAL_ID:
        raise SystemExit("Configure TIME_SERIES_EXTERNAL_ID no início do script.")
    if AGGREGATION not in SUPPORTED_AGGREGATIONS:
        raise SystemExit(f"AGGREGATION inválida: {AGGREGATION!r}.")
    if END <= START:
        raise SystemExit("END precisa ser posterior a START.")

    client = create_cognite_client()
    series_id = _resolve_series(client, TIME_SERIES_EXTERNAL_ID, TIME_SERIES_SPACE)
    query = DatapointsQuery(
        instance_id=series_id,
        start=START,
        end=END,
        aggregates=AGGREGATION,
        granularity=GRANULARITY,
        ignore_unknown_ids=False,
        ignore_bad_datapoints=False,
        treat_uncertain_as_bad=False,
    )
    results = client.time_series.data.retrieve(instance_id=[query], limit=100_000)
    rows = [
        (point.timestamp, getattr(point, AGGREGATION, None))
        for result in cast(list[AggregateResult], results)
        for point in cast(list[AggregateDatapoint], result)
    ]

    print(f"Time series: {series_id.space}/{series_id.external_id}")
    print(f"Aggregation: {AGGREGATION}; granularity: {GRANULARITY}")
    print(
        f"Window [{TIME_ZONE.key}, start inclusive/end exclusive): "
        f"{START.isoformat()} .. {END.isoformat()}"
    )
    print(f"Buckets returned: {len(rows)}")
    print(f"timestamp_{TIME_ZONE.key}\tvalue")
    for timestamp, value in rows:
        formatted = datetime.fromtimestamp(timestamp / 1_000, TIME_ZONE).isoformat()
        print(f"{formatted}\t{value if value is not None else 'null'}")


def _resolve_series(
    client: CogniteClient, external_id: str, space: str | None
) -> NodeId:
    filters: dict[str, object] = {"externalId": {"eq": external_id}}
    if space:
        filters["space"] = {"eq": space}
    matches = CogniteCoreClient(client).cognite_time_series.query_all_pages(
        filters=filters
    )
    if not matches:
        raise SystemExit(f"Nenhuma CogniteTimeSeries encontrada para {external_id!r}.")
    if len(matches) > 1:
        spaces = ", ".join(sorted(item.space for item in matches))
        raise SystemExit(
            f"ExternalId ambíguo em {len(matches)} spaces ({spaces}); "
            "configure TIME_SERIES_SPACE."
        )
    item = matches[0]
    return NodeId(space=item.space, external_id=item.external_id)


if __name__ == "__main__":
    main()
