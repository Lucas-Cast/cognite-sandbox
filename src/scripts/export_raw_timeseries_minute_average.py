"""Export raw OT datapoints and their per-minute arithmetic mean to a CSV.

Each CSV row represents one raw datapoint. The per-minute mean is repeated for
every point in that minute, making it straightforward to plot the raw and
aggregated series together.

Edit the constants below, then run from the repository root:

    uv run python src/scripts/export_raw_timeseries_minute_average.py
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol
from zoneinfo import ZoneInfo

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import NodeId
from cognite.client.data_classes.datapoints import DatapointsQuery

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client, generate_csv

# --- Configuration ---------------------------------------------------------
# The OT RawTimeSeries node whose numeric datapoints will be exported.
RAW_TIME_SERIES_ID = NodeId(
    space="sp_kpw_san_dat",
    external_id="s=1010-PRA-AFA-AFA10-ZN05-CH01.PLC01.gC53_HMI_CycleTimes_PalletXferTimes[4]",
)

# Time zone used for the input window and the timestamp columns in the CSV.
MOUNTAIN_TIME = ZoneInfo("America/Denver")

# The time window is half-open: START <= timestamp < END.
START = datetime(2026, 9, 14, 14, tzinfo=MOUNTAIN_TIME)
END = datetime(2026, 9, 14, 15, tzinfo=MOUNTAIN_TIME)

OUTPUT_FILENAME = "raw_time_series_minute_average.csv"

# The CDF datapoints iterator retrieves every point, even when the selected
# window has more than 100,000 datapoints. This value must divide 100,000.
FETCH_CHUNK_SIZE = 100_000
# ---------------------------------------------------------------------------


class NumericDatapoint(Protocol):
    """Fields used from a raw numeric datapoint returned by CDF."""

    timestamp: int
    value: float | str


@dataclass
class ExportStats:
    datapoints: int = 0
    minutes: int = 0


def main() -> None:
    """Fetch raw numeric datapoints and write them with their minute mean."""
    _validate_configuration()

    stats = ExportStats()
    output_path = generate_csv(
        filename=OUTPUT_FILENAME,
        fieldnames=(
            "timestamp_mountain_time",
            "raw_value",
            "minute_mountain_time",
            "raw_value_average_1m",
        ),
        rows=_csv_rows(create_cognite_client(), stats),
    )

    print(f"RawTimeSeries: {RAW_TIME_SERIES_ID.space}/{RAW_TIME_SERIES_ID.external_id}")
    print(
        f"Window: {_format_timestamp(_datetime_to_ms(START))} to {_format_timestamp(_datetime_to_ms(END))}"
    )
    print(f"Raw datapoints exported: {stats.datapoints}")
    print(f"Minutes with datapoints: {stats.minutes}")
    print(f"CSV saved to: {output_path}")


def _csv_rows(
    cognite_client: CogniteClient, stats: ExportStats
) -> Iterator[dict[str, str]]:
    """Yield one CSV row per point after calculating the enclosing minute mean."""
    current_minute: int | None = None
    minute_points: list[tuple[int, float]] = []

    for timestamp, value in _retrieve_numeric_datapoints(cognite_client):
        minute = _minute_start(timestamp)
        if current_minute is None:
            current_minute = minute
        elif minute != current_minute:
            yield from _rows_for_minute(current_minute, minute_points, stats)
            current_minute = minute
            minute_points = []
        minute_points.append((timestamp, value))

    if current_minute is not None:
        yield from _rows_for_minute(current_minute, minute_points, stats)


def _retrieve_numeric_datapoints(
    cognite_client: CogniteClient,
) -> Iterator[tuple[int, float]]:
    """Retrieve all numeric raw datapoints from CDF in chronological chunks."""
    query = DatapointsQuery(
        instance_id=RAW_TIME_SERIES_ID,
        start=START,
        end=END,
        ignore_bad_datapoints=False,
        treat_uncertain_as_bad=False,
    )
    for chunk in cognite_client.time_series.data(
        query,
        chunk_size_datapoints=FETCH_CHUNK_SIZE,
        return_arrays=False,
    ):
        for datapoint in chunk:
            yield datapoint.timestamp, _numeric_value(datapoint)


def _numeric_value(datapoint: NumericDatapoint) -> float:
    """Return a numeric value or fail before writing a misleading average."""
    if isinstance(datapoint.value, bool) or not isinstance(
        datapoint.value, int | float
    ):
        raise ValueError(
            "The configured RawTimeSeries has non-numeric datapoints; "
            "a per-minute arithmetic mean cannot be calculated."
        )
    return float(datapoint.value)


def _rows_for_minute(
    minute: int,
    points: list[tuple[int, float]],
    stats: ExportStats,
) -> Iterator[dict[str, str]]:
    """Return rows for a minute with its arithmetic mean repeated per point."""
    average = sum(value for _, value in points) / len(points)
    stats.datapoints += len(points)
    stats.minutes += 1
    for timestamp, value in points:
        yield {
            "timestamp_mountain_time": _format_timestamp(timestamp),
            "raw_value": _format_excel_number(value),
            "minute_mountain_time": _format_timestamp(minute),
            "raw_value_average_1m": _format_excel_number(average),
        }


def _minute_start(timestamp: int) -> int:
    return timestamp // 60_000 * 60_000


def _datetime_to_ms(value: datetime) -> int:
    return int(value.timestamp() * 1_000)


def _format_timestamp(timestamp: int) -> str:
    """Format the CSV timestamp in America/Denver, including MDT or MST."""
    return datetime.fromtimestamp(timestamp / 1_000, tz=MOUNTAIN_TIME).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )


def _format_excel_number(value: float) -> str:
    """Use a comma decimal separator for the project's semicolon CSV format."""
    return format(value, ".15g").replace(".", ",")


def _validate_configuration() -> None:
    if not RAW_TIME_SERIES_ID.space or not RAW_TIME_SERIES_ID.external_id:
        raise ValueError("Set RAW_TIME_SERIES_ID with both space and external_id.")
    if START.tzinfo is None or END.tzinfo is None:
        raise ValueError("START and END must include a timezone.")
    if END <= START:
        raise ValueError("END must be after START.")
    if FETCH_CHUNK_SIZE < 1 or 100_000 % FETCH_CHUNK_SIZE:
        raise ValueError("FETCH_CHUNK_SIZE must be a positive divisor of 100,000.")


if __name__ == "__main__":
    main()
