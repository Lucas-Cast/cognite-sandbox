"""Count Line assets covered by time series datapoints.

For ``CogniteTimeSeries``, the script filters by an exact KPI tag and counts
the leaf assets directly attached to time series with datapoints.

For ``raw`` and ``curated``, it filters OT time series by service/subservice.
Only System-leaf series with datapoints are counted directly; their parent
Machines and Zones are then counted through the Asset DOM hierarchy.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import UTC, datetime
from pathlib import Path
import sys
from typing import Literal, Protocol, cast

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import NodeId
from cognite.client.data_classes.datapoints import DatapointsQuery
from industrial_model import InstanceId

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client
from core.data.cognite_core import CogniteCoreClient
from core.data.cognite_core.cognite_time_series.filters import CogniteTimeSeriesFilter
from core.data.cognite_core.models import CogniteTimeSeries
from core.data.asset_dom import AssetClient
from core.data.asset_dom.models import Machine, System
from core.data.ot_dom import OtClient
from core.data.ot_dom.curated_time_series.filters import CuratedTimeSeriesFilter
from core.data.ot_dom.models import CuratedTimeSeries, RawTimeSeries
from core.data.ot_dom.raw_time_series.filters import RawTimeSeriesFilter
from core.line_asset_tree_service import AssetExternalIdsByLevel, LineAssetTreeService

# --- Configuration ---------------------------------------------------------
# Choose which time series source to inspect: "raw", "curated", or
# "CogniteTimeSeries" (the CDF Cognite Core view).
TIME_SERIES_KIND: Literal["raw", "curated", "CogniteTimeSeries"] = "raw"

# Applied only when TIME_SERIES_KIND is "CogniteTimeSeries". It is an exact
# tag match; for example, "Kpi:IdleTime:Duration".
KPI_TAG = "Kpi:IDT:1m"

# Applied only when TIME_SERIES_KIND is "raw" or "curated".
SERVICE_EXTERNAL_ID = "TSSE-PC"
SUBSERVICE_EXTERNAL_ID = "TSSS-IT"

# Asset DOM Line whose descendant Zone, Machine, and System assets are counted.
LINE_EXTERNAL_ID = "LNE-a33832a03a11376bd957d576abed79de"

# A matching time series counts only when it has at least one datapoint inside
# this half-open window: WINDOW_START <= timestamp < WINDOW_END.
WINDOW_START = datetime(2026, 1, 1, tzinfo=UTC)
WINDOW_END = datetime(2026, 10, 1, tzinfo=UTC)

# CDF retrieves datapoints in batches. Keep this at or below 1,000.
BATCH_SIZE = 1_000

# Asset external ID prefixes used to identify the Asset DOM level.
LEAF_ASSET_PREFIX_BY_LEVEL = {
    "Machine": "MCH",
    "System": "SYS",
    "Zone": "ZNE",
}
# ---------------------------------------------------------------------------


class AggregateDatapointsResponse(Protocol):
    """Fields used from one aggregate datapoints response."""

    instance_id: NodeId | None
    count: list[int] | None


TimeSeries = RawTimeSeries | CuratedTimeSeries | CogniteTimeSeries
ResolvedTimeSeries = tuple[TimeSeries, str, str]


def main() -> None:
    """Print KPI datapoint coverage for the configured Line assets."""
    _validate_configuration()

    cognite_client = create_cognite_client()
    line_assets = LineAssetTreeService(cognite_client).descendant_asset_external_ids(
        LINE_EXTERNAL_ID
    )
    time_series = _query_time_series(cognite_client)
    line_time_series = _time_series_for_line(time_series, line_assets)
    ids_with_datapoints = _ids_with_datapoints_in_window(
        cognite_client,
        [
            NodeId(space=item.space, external_id=item.external_id)
            for item, _, _ in line_time_series
        ],
    )
    system_machines, machine_zones, system_names = _line_system_hierarchy(
        cognite_client, line_assets
    )
    system_assets_with_time_series = _system_assets_with_time_series(line_time_series)
    missing_systems = _missing_systems(
        line_assets["System"],
        system_assets_with_time_series,
        system_names,
    )
    if TIME_SERIES_KIND == "CogniteTimeSeries":
        assets_with_datapoints = _assets_with_datapoints_by_level(
            line_time_series, ids_with_datapoints
        )
        coverage_rule = "assets-folha diretamente associados às Time Series"
    else:
        system_assets_with_datapoints = _system_assets_with_datapoints(
            line_time_series, ids_with_datapoints
        )
        assets_with_datapoints = _assets_covered_by_systems(
            system_assets_with_datapoints,
            system_machines,
            machine_zones,
        )
        coverage_rule = "Systems com datapontos e suas Machines/Zones pai no Asset DOM"

    _print_summary(
        line_assets,
        time_series,
        line_time_series,
        ids_with_datapoints,
        assets_with_datapoints,
        coverage_rule,
        missing_systems,
    )


def _query_time_series(cognite_client: CogniteClient) -> list[TimeSeries]:
    ot_client = OtClient(cognite_client)
    if TIME_SERIES_KIND == "raw":
        return list(
            ot_client.raw_time_series.query_all_pages(
                filters=_raw_time_series_filters()
            )
        )
    if TIME_SERIES_KIND == "curated":
        return list(
            ot_client.curated_time_series.query_all_pages(
                filters=_curated_time_series_filters()
            )
        )
    return list(
        CogniteCoreClient(cognite_client).cognite_time_series.query_all_pages(
            filters=_cognite_time_series_filters(),
            include=["assets"],
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


def _cognite_time_series_filters() -> CogniteTimeSeriesFilter:
    return {"tags": {"containsAll": [KPI_TAG]}}


def _time_series_for_line(
    time_series: Iterable[TimeSeries], line_assets: AssetExternalIdsByLevel
) -> list[ResolvedTimeSeries]:
    """Keep time series whose resolved leaf asset belongs to the Line."""
    result: list[ResolvedTimeSeries] = []
    for item in time_series:
        asset_level, asset_external_id = _leaf_asset_metadata(item)
        if (
            asset_level is not None
            and asset_external_id is not None
            and asset_external_id in line_assets.get(asset_level, set())
        ):
            result.append((item, asset_level, asset_external_id))
    return result


def _leaf_asset_metadata(item: TimeSeries) -> tuple[str | None, str | None]:
    if isinstance(item, CogniteTimeSeries):
        return _cognite_time_series_asset_metadata(item)

    asset_level = next(
        (
            tag.removeprefix("LeafAssetType:")
            for tag in item.tags
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
            for asset in item.assets
            if asset.external_id.startswith(f"{prefix}-")
        ),
        None,
    )
    return asset_level, asset_external_id


def _cognite_time_series_asset_metadata(
    item: CogniteTimeSeries,
) -> tuple[str | None, str | None]:
    """Resolve the direct asset relation of a CogniteTimeSeries.

    CogniteTimeSeries does not carry the ``LeafAssetType:*`` tag used by OT
    time series. Its ``assets`` relation is the authoritative asset reference.
    """
    for asset in item.assets:
        for asset_level, prefix in LEAF_ASSET_PREFIX_BY_LEVEL.items():
            if asset.external_id.startswith(f"{prefix}-"):
                return asset_level, asset.external_id
    return None, None


def _ids_with_datapoints_in_window(
    cognite_client: CogniteClient, ids: Sequence[NodeId]
) -> set[tuple[str, str]]:
    """Return time series that have at least one datapoint in the window."""
    ids_with_datapoints: set[tuple[str, str]] = set()
    for start in range(0, len(ids), BATCH_SIZE):
        batch: list[NodeId | DatapointsQuery] = list(ids[start : start + BATCH_SIZE])
        response = cognite_client.time_series.data.retrieve(
            instance_id=batch,
            start=WINDOW_START,
            end=WINDOW_END,
            aggregates="count",
            granularity="1d",
            limit=_window_days(),
            ignore_bad_datapoints=False,
            treat_uncertain_as_bad=False,
            ignore_unknown_ids=True,
        )
        for datapoint in cast(Sequence[AggregateDatapointsResponse], response):
            if datapoint.instance_id is not None and any(
                count > 0 for count in datapoint.count or []
            ):
                ids_with_datapoints.add(_id_key(datapoint.instance_id))
    return ids_with_datapoints


def _assets_with_datapoints_by_level(
    line_time_series: Iterable[ResolvedTimeSeries],
    ids_with_datapoints: set[tuple[str, str]],
) -> dict[str, set[str]]:
    result = {asset_level: set() for asset_level in LEAF_ASSET_PREFIX_BY_LEVEL}
    for item, asset_level, asset_external_id in line_time_series:
        if _time_series_key(item) in ids_with_datapoints:
            result[asset_level].add(asset_external_id)
    return result


def _system_assets_with_datapoints(
    line_time_series: Iterable[ResolvedTimeSeries],
    ids_with_datapoints: set[tuple[str, str]],
) -> set[str]:
    """Return System leaf assets whose raw/curated series has a datapoint."""
    return {
        asset_external_id
        for item, asset_level, asset_external_id in line_time_series
        if asset_level == "System" and _time_series_key(item) in ids_with_datapoints
    }


def _system_assets_with_time_series(
    line_time_series: Iterable[ResolvedTimeSeries],
) -> set[str]:
    """Return Systems that have a matching time series, regardless of data."""
    return {
        asset_external_id
        for _, asset_level, asset_external_id in line_time_series
        if asset_level == "System"
    }


def _line_system_hierarchy(
    cognite_client: CogniteClient,
    line_assets: AssetExternalIdsByLevel,
) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, str | None]]:
    """Return System -> Machine and Machine -> Zone relations for the Line."""
    asset_client = AssetClient(cognite_client)
    lines = asset_client.line.query_all_pages(
        filters={"externalId": {"eq": LINE_EXTERNAL_ID}}
    )
    if not lines:
        raise ValueError(f'No Line found with external ID "{LINE_EXTERNAL_ID}".')
    if len(lines) > 1:
        raise ValueError(
            f'More than one Line found with external ID "{LINE_EXTERNAL_ID}". '
            "Use a unique external ID."
        )

    line = lines[0]
    machines = asset_client.machine.query_all_pages(
        filters={
            "line": {
                "containsAny": [
                    InstanceId(space=line.space, external_id=line.external_id)
                ]
            }
        },
        include=["zone"],
    )
    machine_ids = [
        InstanceId(space=machine.space, external_id=machine.external_id)
        for machine in machines
    ]
    systems = (
        asset_client.system.query_all_pages(
            filters={"machine": {"containsAny": machine_ids}},
            include=["machine"],
        )
        if machine_ids
        else []
    )

    return (
        _system_machines(systems, line_assets["Machine"]),
        _machine_zones(machines, line_assets["Zone"]),
        {
            system.external_id: system.name
            for system in systems
            if system.external_id in line_assets["System"]
        },
    )


def _system_machines(
    systems: Iterable[System], expected_machine_ids: set[str]
) -> dict[str, set[str]]:
    return {
        system.external_id: {
            machine.external_id
            for machine in system.machine
            if machine.external_id in expected_machine_ids
        }
        for system in systems
    }


def _machine_zones(
    machines: Iterable[Machine], expected_zone_ids: set[str]
) -> dict[str, set[str]]:
    return {
        machine.external_id: {
            zone.external_id
            for zone in machine.zone
            if zone.external_id in expected_zone_ids
        }
        for machine in machines
    }


def _assets_covered_by_systems(
    system_assets_with_datapoints: set[str],
    system_machines: dict[str, set[str]],
    machine_zones: dict[str, set[str]],
) -> dict[str, set[str]]:
    """Propagate raw/curated System coverage to its Machine and Zone parents."""
    machine_assets = {
        machine_external_id
        for system_external_id in system_assets_with_datapoints
        for machine_external_id in system_machines.get(system_external_id, set())
    }
    return {
        "System": system_assets_with_datapoints,
        "Machine": machine_assets,
        "Zone": {
            zone_external_id
            for machine_external_id in machine_assets
            for zone_external_id in machine_zones.get(machine_external_id, set())
        },
    }


def _missing_systems(
    expected_system_ids: set[str],
    systems_with_time_series: set[str],
    system_names: dict[str, str | None],
) -> list[tuple[str, str | None]]:
    return [
        (system_external_id, system_names.get(system_external_id))
        for system_external_id in sorted(expected_system_ids - systems_with_time_series)
    ]


def _print_summary(
    line_assets: AssetExternalIdsByLevel,
    queried_time_series: Sequence[TimeSeries],
    line_time_series: Sequence[ResolvedTimeSeries],
    ids_with_datapoints: set[tuple[str, str]],
    assets_with_datapoints: dict[str, set[str]],
    coverage_rule: str,
    missing_systems: Sequence[tuple[str, str | None]],
) -> None:
    print(f"Line external ID: {LINE_EXTERNAL_ID}")
    print(f"Time series kind: {TIME_SERIES_KIND}")
    if TIME_SERIES_KIND == "CogniteTimeSeries":
        print(f"KPI tag: {KPI_TAG}")
    else:
        print(f"Service external ID: {SERVICE_EXTERNAL_ID}")
        print(f"Subservice external ID: {SUBSERVICE_EXTERNAL_ID}")
    print(f"Window: {WINDOW_START.isoformat()} to {WINDOW_END.isoformat()}")
    print(f"Time series retornadas pelo filtro: {len(queried_time_series)}")
    print(f"Time series for Line leaf assets: {len(line_time_series)}")
    print(f"Time series with datapoints in window: {len(ids_with_datapoints)}")
    print(f"Regra de cobertura: {coverage_rule}")
    print("\nAssets distintos cobertos na janela:")

    for asset_level in ("Zone", "Machine", "System"):
        assets_with_datapoints_at_level = assets_with_datapoints[asset_level]
        total_assets_at_level = line_assets[asset_level]
        print(
            f"{asset_level}: "
            f"{len(assets_with_datapoints_at_level)}/{len(total_assets_at_level)}"
        )

    if missing_systems:
        print(
            "\nSystems sem Time Series correspondente ao filtro (external_id | name):"
        )
        for system_external_id, system_name in missing_systems:
            print(f"- {system_external_id} | {system_name or '(sem nome)'}")


def _id_key(instance_id: NodeId) -> tuple[str, str]:
    return instance_id.space, instance_id.external_id


def _time_series_key(item: TimeSeries) -> tuple[str, str]:
    return item.space, item.external_id


def _window_days() -> int:
    return max(1, (WINDOW_END - WINDOW_START).days)


def _validate_configuration() -> None:
    if TIME_SERIES_KIND not in {"raw", "curated", "CogniteTimeSeries"}:
        raise ValueError(
            'TIME_SERIES_KIND must be "raw", "curated", or "CogniteTimeSeries".'
        )
    if TIME_SERIES_KIND == "CogniteTimeSeries" and not KPI_TAG:
        raise ValueError("Set KPI_TAG when using CogniteTimeSeries.")
    if TIME_SERIES_KIND != "CogniteTimeSeries" and not any(
        (SERVICE_EXTERNAL_ID, SUBSERVICE_EXTERNAL_ID)
    ):
        raise ValueError(
            "Set SERVICE_EXTERNAL_ID or SUBSERVICE_EXTERNAL_ID for raw/curated."
        )
    if not LINE_EXTERNAL_ID:
        raise ValueError("Set LINE_EXTERNAL_ID.")
    if BATCH_SIZE < 1 or BATCH_SIZE > 1_000:
        raise ValueError("BATCH_SIZE must be between 1 and 1,000.")
    if WINDOW_START.tzinfo is None or WINDOW_END.tzinfo is None:
        raise ValueError("WINDOW_START and WINDOW_END must include a timezone.")
    if WINDOW_END <= WINDOW_START:
        raise ValueError("WINDOW_END must be after WINDOW_START.")


if __name__ == "__main__":
    main()
