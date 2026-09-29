"""Export Rolling Average and Good Quantity datapoints side by side for validation."""

from __future__ import annotations

import sys
from collections import deque
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol, cast

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import NodeId
from cognite.client.data_classes.datapoints import DatapointsQuery

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client, generate_csv
from core.data.cognite_core import CogniteCoreClient

# --- Configuration ---------------------------------------------------------
# The current pair belongs to ZN01. Change both IDs together to validate
# another asset's Rolling Average against its Good Quantity input.
ROLLING_AVERAGE_TIME_SERIES_ID = NodeId(
    space="sp_kpi_glb_dat",
    external_id="ZNE-ab47ac65ccbfeda107f81447b2cb00dd-parameter-RAO",
)
GOOD_QUANTITY_TIME_SERIES_ID = NodeId(
    space="sp_otm_san_dat",
    external_id="s=1010-PRA-AFA-AFA10-ZN01-CH01.PLC01.gMES_Good_Parts_DLT",
)
START = datetime(2026, 2, 5, tzinfo=UTC)
END = datetime(2026, 2, 24, tzinfo=UTC)
OUTPUT_FILENAME = "rolling_average_validation.csv"
ROLLING_AVERAGE_DECIMAL_PLACES = 3
GOOD_QUANTITY_GRANULARITY = "1m"
# RAO considers the most recent Good Quantity buckets that exist. This is a
# count of values, not a clock-time interval: gaps between minute buckets do
# not reset the window.
GOOD_QUANTITY_ROLLING_WINDOW_VALUES = 3

# The CDF datapoints API limit. Raise it if the configured window contains
# more than this number of datapoints for either time series.
DATAPOINT_LIMIT = 100_000
# ---------------------------------------------------------------------------


class Datapoint(Protocol):
    """Fields used from a CDF numeric datapoint."""

    timestamp: int
    value: float | None


class DatapointsResponse(Protocol):
    """Fields used from one CDF time series datapoints response."""

    instance_id: NodeId | None

    def __iter__(self) -> object: ...


def main() -> None:
    """Retrieve the configured series and save their values in one CSV."""
    if END <= START:
        raise ValueError("END must be after START.")

    cognite_client = create_cognite_client()
    rolling_average_asset_external_id = _rolling_average_asset_external_id(
        cognite_client
    )
    values_by_series = _retrieve_values(cognite_client)
    rolling_average = values_by_series.get(_id_key(ROLLING_AVERAGE_TIME_SERIES_ID), {})
    good_quantity = values_by_series.get(_id_key(GOOD_QUANTITY_TIME_SERIES_ID), {})
    calculated_rolling_average = _trailing_moving_average(good_quantity)
    timestamps = sorted(rolling_average.keys() | good_quantity.keys())

    rows = [
        {
            "good_quantity_external_id": GOOD_QUANTITY_TIME_SERIES_ID.external_id,
            "rolling_average_asset_external_id": rolling_average_asset_external_id,
            "timestamp_utc": _format_timestamp(timestamp),
            "rolling_average": _format_rolling_average(rolling_average.get(timestamp)),
            f"good_quantity_sum_{GOOD_QUANTITY_GRANULARITY}": _format_value(
                good_quantity.get(timestamp)
            ),
            f"good_quantity_moving_average_last_{GOOD_QUANTITY_ROLLING_WINDOW_VALUES}_values": (
                _format_rolling_average(calculated_rolling_average.get(timestamp))
            ),
        }
        for timestamp in timestamps
    ]
    output_path = generate_csv(
        filename=OUTPUT_FILENAME,
        fieldnames=(
            "good_quantity_external_id",
            "rolling_average_asset_external_id",
            "timestamp_utc",
            "rolling_average",
            f"good_quantity_sum_{GOOD_QUANTITY_GRANULARITY}",
            f"good_quantity_moving_average_last_{GOOD_QUANTITY_ROLLING_WINDOW_VALUES}_values",
        ),
        rows=rows,
    )

    print(f"Rolling Average datapoints: {len(rolling_average)}")
    print(
        f"Good Quantity minute sums: {len(good_quantity)} ({GOOD_QUANTITY_GRANULARITY})"
    )
    print(f"Rows exported: {len(rows)}")
    print(f"CSV saved to: {output_path}")


def _retrieve_values(
    cognite_client: CogniteClient,
) -> dict[tuple[str, str], dict[int, float | None]]:
    """Return numeric datapoints indexed by series ID and timestamp."""
    response = cognite_client.time_series.data.retrieve(
        instance_id=[
            ROLLING_AVERAGE_TIME_SERIES_ID,
            DatapointsQuery(
                instance_id=GOOD_QUANTITY_TIME_SERIES_ID,
                aggregates="sum",
                granularity=GOOD_QUANTITY_GRANULARITY,
            ),
        ],
        start=START,
        end=END,
        limit=DATAPOINT_LIMIT,
        ignore_bad_datapoints=False,
        treat_uncertain_as_bad=False,
        ignore_unknown_ids=False,
    )
    values_by_series: dict[tuple[str, str], dict[int, float | None]] = {}
    for result in cast(list[DatapointsResponse], response):
        if result.instance_id is None:
            continue
        datapoints = cast(list[Datapoint], result)
        value_attribute = (
            "value"
            if _id_key(result.instance_id) == _id_key(ROLLING_AVERAGE_TIME_SERIES_ID)
            else "sum"
        )
        values_by_series[_id_key(result.instance_id)] = {
            datapoint.timestamp: getattr(datapoint, value_attribute)
            for datapoint in datapoints
        }
    return values_by_series


def _trailing_moving_average(
    values_by_timestamp: dict[int, float | None],
) -> dict[int, float]:
    """Average each Good Quantity value with the preceding available values."""
    window: deque[float] = deque()
    window_sum = 0.0
    averages: dict[int, float] = {}

    for timestamp in sorted(values_by_timestamp):
        value = values_by_timestamp[timestamp]
        if value is None:
            continue

        if len(window) == GOOD_QUANTITY_ROLLING_WINDOW_VALUES:
            window_sum -= window.popleft()
        window.append(value)
        window_sum += value
        averages[timestamp] = window_sum / len(window)

    return averages


def _rolling_average_asset_external_id(cognite_client: CogniteClient) -> str:
    """Return the asset external ID associated with the configured RAO series."""
    rolling_average_series = CogniteCoreClient(
        cognite_client
    ).cognite_time_series.query_all_pages(
        filters={
            "externalId": {
                "eq": ROLLING_AVERAGE_TIME_SERIES_ID.external_id,
            },
            "space": {"eq": ROLLING_AVERAGE_TIME_SERIES_ID.space},
        },
        include=["assets"],
    )
    if len(rolling_average_series) != 1:
        raise ValueError(
            "Expected exactly one Rolling Average time series with ID "
            f"{ROLLING_AVERAGE_TIME_SERIES_ID.space}/"
            f"{ROLLING_AVERAGE_TIME_SERIES_ID.external_id}."
        )

    asset_external_ids = sorted(
        asset.external_id for asset in rolling_average_series[0].assets
    )
    if not asset_external_ids:
        raise ValueError("The configured Rolling Average time series has no asset.")
    return ", ".join(asset_external_ids)


def _id_key(instance_id: NodeId) -> tuple[str, str]:
    return instance_id.space, instance_id.external_id


def _format_timestamp(timestamp: int) -> str:
    return (
        datetime.fromtimestamp(timestamp / 1_000, tz=UTC)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _format_rolling_average(value: float | None) -> str | None:
    """Format only the display precision, using a pt-BR decimal separator."""
    if value is None:
        return None
    return f"{value:.{ROLLING_AVERAGE_DECIMAL_PLACES}f}".replace(".", ",")


def _format_value(value: float | None) -> str | None:
    """Use a pt-BR decimal separator so Excel imports numeric values correctly."""
    return str(value).replace(".", ",") if value is not None else None


if __name__ == "__main__":
    main()
