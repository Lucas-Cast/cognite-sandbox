"""Export a timeline by asset for the selected BaseEvent external IDs.

The script resolves the ``BaseEvent`` view from CDF at runtime and retrieves
only the configured events. It creates one timeline row per event/asset
association, plus an asset summary.

Edit the configuration below, then run from the repository root:

    uv run python src/scripts/export_base_events_timeline.py
"""

from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import NodeId, ViewId

# The script lives in src/scripts/events; core is a sibling package in src.
sys.path.insert(0, str(Path(__file__).parents[2]))

from core.cognite import create_cognite_client
from core.csv_generator import generate_csv

# --- Configuration ---------------------------------------------------------
# Canonical BaseEvent view. The similarly named views in ``sp_evt_glb_ing``
# and ``sp_oee_glb_dml_temp`` are ingestion and temporary-model variants.
BASE_EVENT_VIEW: ViewId | None = ViewId("sp_evt_glb_dmd", "BaseEvent", "v1.0.0")
BASE_EVENT_VIEW_EXTERNAL_ID = "BaseEvent"

# The same BaseEvents configured in update_base_event_subcategory.py.
EVENT_INSTANCE_SPACE = "sp_otm_san_dat"
EVENT_EXTERNAL_IDS: list[str] = [
    "BEVT-s=1010-PRA-AFA-AFA10-ZN02-CH01.PLC01.gMES_Status_2026-09-01T00:00:10.430000+00:00_9003_0",
    "BEVT-s=1010-PRA-AFA-AFA10-ZN02-CH01.PLC01.gMES_Status_2026-09-01T00:02:57.427000+00:00_9003_0",
    "BEVT-s=1010-PRA-AFA-AFA10-ZN05-CH01.PLC01.gC52_HMI_Cell_StatusDisplay_2026-09-01T00:00:57.816000+00:00_13_4",
    "BEVT-s=1010-PRA-AFA-AFA10-ZN05-CH01.PLC01.gC52_HMI_Cell_StatusDisplay_2026-09-01T00:05:13.023000+00:00_13_0",
    "BEVT-s=1010-PRA-AFA-AFA10-ZN05-CH01.PLC01.gC53_HMI_Cell_StatusDisplay_2026-09-01T00:00:04.561000+00:00_13_3",
    "BEVT-s=1010-PRA-AFA-AFA10-ZN05-CH01.PLC01.gC53_HMI_Cell_StatusDisplay_2026-09-01T00:00:06.817000+00:00_14_0",
    "BEVT-s=1010-PRA-AFA-AFA10-ZN04-CH01.PLC01.gC43_HMI_Cell_StatusDisplay_2026-09-01T00:03:42.375000+00:00_10_0",
    "BEVT-s=1010-PRA-AFA-AFA10-ZN04-CH01.PLC01.gC43_HMI_Cell_StatusDisplay_2026-09-01T00:05:12.952000+00:00_6_0",
]

# The auto-detection below covers common property names. Set any of these when
# the BaseEvent view uses a different name; errors list all available fields.
SUBCATEGORY_PROPERTY: str | None = None
ASSET_PROPERTY: str | None = "assets"
START_TIME_PROPERTY: str | None = None
END_TIME_PROPERTY: str | None = None
NAME_PROPERTY: str | None = None
DESCRIPTION_PROPERTY: str | None = None

# Optional asset external ID to restrict the export. This is an asset value,
# not the name of a BaseEvent property. Leave None to export every asset.
ASSET_EXTERNAL_ID_FILTER: str | None = None

TIMELINE_OUTPUT_FILENAME = "selected_base_events_timeline.csv"
ASSET_SUMMARY_OUTPUT_FILENAME = "selected_base_events_by_asset.csv"
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class InstanceReference:
    space: str
    external_id: str


@dataclass(frozen=True)
class EventTimelineEntry:
    event: InstanceReference
    asset: InstanceReference | None
    subcategory: InstanceReference | None
    start_time: datetime | None
    end_time: datetime | None
    name: str | None
    description: str | None


def main() -> None:
    """Export the selected BaseEvents, grouped and ordered by asset."""
    _validate_configuration()
    cognite_client = create_cognite_client()
    base_event_view = _resolve_base_event_view(cognite_client)
    property_names = _resolve_available_property_names(
        _view_properties(cognite_client, base_event_view),
        _configured_property_names(),
    )
    entries = _matching_event_entries(
        cognite_client,
        base_event_view,
        property_names,
    )
    timeline_rows = _timeline_rows(entries)
    summary_rows = _asset_summary_rows(entries)

    timeline_path = generate_csv(
        TIMELINE_OUTPUT_FILENAME,
        (
            "asset_space",
            "asset_external_id",
            "asset_timeline_order",
            "event_space",
            "event_external_id",
            "event_name",
            "event_description",
            "start_utc",
            "end_utc",
            "duration_minutes",
            "subcategory_space",
            "subcategory_external_id",
        ),
        timeline_rows,
    )
    summary_path = generate_csv(
        ASSET_SUMMARY_OUTPUT_FILENAME,
        (
            "asset_space",
            "asset_external_id",
            "event_count",
            "first_event_utc",
            "last_event_utc",
        ),
        summary_rows,
    )

    print(f"BaseEvent view: {_view_label(base_event_view)}")
    print(f"Selected event external IDs: {len(EVENT_EXTERNAL_IDS)}")
    print(f"Asset external ID filter: {ASSET_EXTERNAL_ID_FILTER or 'None'}")
    print(f"Timeline rows (event/asset): {len(timeline_rows)}")
    print(f"Assets: {len(summary_rows)}")
    print(f"Timeline CSV saved to: {timeline_path}")
    print(f"Asset summary CSV saved to: {summary_path}")


def _resolve_base_event_view(cognite_client: CogniteClient) -> ViewId:
    """Return the configured view or discover the unique BaseEvent view."""
    if BASE_EVENT_VIEW is not None:
        views = cognite_client.data_modeling.views.retrieve(
            BASE_EVENT_VIEW,
            include_inherited_properties=True,
            all_versions=False,
        )
        if not views:
            raise ValueError(
                f"BaseEvent view not found: {_view_label(BASE_EVENT_VIEW)}"
            )
        return views[0].as_id()

    matching_views = [
        view
        for view in cognite_client.data_modeling.views.list(
            limit=None,
            include_inherited_properties=True,
            all_versions=False,
            include_global=True,
        )
        if view.external_id == BASE_EVENT_VIEW_EXTERNAL_ID
    ]
    if len(matching_views) == 1:
        return matching_views[0].as_id()
    if not matching_views:
        raise ValueError(
            f'No view with external ID "{BASE_EVENT_VIEW_EXTERNAL_ID}" was found. '
            "Set BASE_EVENT_VIEW to the exact view ID."
        )

    candidates = ", ".join(_view_label(view.as_id()) for view in matching_views)
    raise ValueError(
        f'More than one view has external ID "{BASE_EVENT_VIEW_EXTERNAL_ID}": '
        f"{candidates}. Set BASE_EVENT_VIEW to one of them."
    )


def _configured_property_names() -> dict[str, str | None]:
    """Resolve expected BaseEvent properties, with explicit overrides available."""
    # Properties are obtained in _matching_event_entries from the selected view.
    # These candidate names are kept here to make the expected model explicit.
    return {
        "subcategory": SUBCATEGORY_PROPERTY,
        "assets": ASSET_PROPERTY,
        "start_time": START_TIME_PROPERTY,
        "end_time": END_TIME_PROPERTY,
        "name": NAME_PROPERTY,
        "description": DESCRIPTION_PROPERTY,
    }


def _view_properties(
    cognite_client: CogniteClient, base_event_view: ViewId
) -> Mapping[str, Any]:
    views = cognite_client.data_modeling.views.retrieve(
        base_event_view,
        include_inherited_properties=True,
        all_versions=False,
    )
    if not views:
        raise ValueError(f"BaseEvent view not found: {_view_label(base_event_view)}")
    return views[0].properties


def _matching_event_entries(
    cognite_client: CogniteClient,
    base_event_view: ViewId,
    property_names: dict[str, str | None],
) -> list[EventTimelineEntry]:
    """Read selected BaseEvents and return one entry per event/asset pair."""
    entries: list[EventTimelineEntry] = []

    result = cognite_client.data_modeling.instances.retrieve(
        nodes=[
            NodeId(EVENT_INSTANCE_SPACE, external_id)
            for external_id in EVENT_EXTERNAL_IDS
        ],
        sources=base_event_view,
    )
    events_by_external_id = {event.external_id: event for event in result.nodes}
    missing_external_ids = [
        external_id
        for external_id in EVENT_EXTERNAL_IDS
        if external_id not in events_by_external_id
    ]
    if missing_external_ids:
        raise ValueError(
            "The following BaseEvent node(s) were not found in "
            f"{EVENT_INSTANCE_SPACE}: {', '.join(missing_external_ids)}"
        )

    for external_id in EVENT_EXTERNAL_IDS:
        event = events_by_external_id[external_id]
        properties = (
            event.properties.get(base_event_view, {}) if event.properties else {}
        )

        subcategory = _first_reference(properties.get(property_names["subcategory"]))
        assets = _references(properties.get(property_names["assets"]))
        if ASSET_EXTERNAL_ID_FILTER is not None:
            assets = [
                asset
                for asset in assets
                if asset.external_id == ASSET_EXTERNAL_ID_FILTER
            ]
        event_reference = InstanceReference(event.space, event.external_id)
        # An event with no matching asset must not appear when a filter is set.
        assets_to_export = assets or (
            [] if ASSET_EXTERNAL_ID_FILTER is not None else [None]
        )
        for asset in assets_to_export:
            entries.append(
                EventTimelineEntry(
                    event=event_reference,
                    asset=asset,
                    subcategory=subcategory,
                    start_time=_as_datetime(
                        properties.get(property_names["start_time"])
                    ),
                    end_time=_as_datetime(properties.get(property_names["end_time"])),
                    name=_as_text(properties.get(property_names["name"])),
                    description=_as_text(properties.get(property_names["description"])),
                )
            )
    return entries


def _resolve_available_property_names(
    properties: Mapping[str, Any],
    configured_names: Mapping[str, str | None],
) -> dict[str, str | None]:
    """Resolve property names using explicit overrides or common alternatives."""
    candidates = {
        "subcategory": ("subCategory", "subcategory", "eventSubcategory"),
        "assets": ("assets", "asset", "relatedAsset", "relatedAssets"),
        "start_time": (
            "startTime",
            "startDateTime",
            "eventStartTime",
            "eventTime",
            "start",
        ),
        "end_time": ("endTime", "endDateTime", "eventEndTime", "end"),
        "name": ("name", "title"),
        "description": ("description", "details"),
    }
    available_by_normalized_name = {
        _normalize_property_name(name): name for name in properties
    }
    optional_properties = {"end_time", "name", "description"}
    result: dict[str, str | None] = {}
    for key, choices in candidates.items():
        configured_name = configured_names.get(key)
        if configured_name is not None:
            if configured_name not in properties:
                raise ValueError(
                    f'Configured {key} property "{configured_name}" is not available. '
                    f"Available properties: {', '.join(sorted(properties))}"
                )
            result[key] = configured_name
            continue

        property_name = next(
            (
                available_by_normalized_name.get(_normalize_property_name(choice))
                for choice in choices
                if _normalize_property_name(choice) in available_by_normalized_name
            ),
            None,
        )
        if property_name is None:
            if key in optional_properties:
                result[key] = None
                continue
            raise ValueError(
                f"Could not determine the BaseEvent {key} property. "
                f"Set {key.upper()}_PROPERTY. Available properties: "
                f"{', '.join(sorted(properties))}"
            )
        result[key] = property_name
    return result


def _timeline_rows(entries: Iterable[EventTimelineEntry]) -> list[dict[str, str]]:
    sorted_entries = sorted(entries, key=_entry_sort_key)
    timeline_order_by_asset: dict[InstanceReference | None, int] = defaultdict(int)
    rows: list[dict[str, str]] = []
    for entry in sorted_entries:
        timeline_order_by_asset[entry.asset] += 1
        rows.append(
            {
                "asset_space": entry.asset.space if entry.asset else "",
                "asset_external_id": entry.asset.external_id if entry.asset else "",
                "asset_timeline_order": str(timeline_order_by_asset[entry.asset]),
                "event_space": entry.event.space,
                "event_external_id": entry.event.external_id,
                "event_name": entry.name or "",
                "event_description": entry.description or "",
                "start_utc": _format_timestamp(entry.start_time),
                "end_utc": _format_timestamp(entry.end_time),
                "duration_minutes": _format_duration_minutes(entry),
                "subcategory_space": entry.subcategory.space
                if entry.subcategory
                else "",
                "subcategory_external_id": (
                    entry.subcategory.external_id if entry.subcategory else ""
                ),
            }
        )
    return rows


def _asset_summary_rows(entries: Iterable[EventTimelineEntry]) -> list[dict[str, str]]:
    entries_by_asset: dict[InstanceReference | None, list[EventTimelineEntry]] = (
        defaultdict(list)
    )
    for entry in entries:
        entries_by_asset[entry.asset].append(entry)

    rows: list[dict[str, str]] = []
    for asset, asset_entries in sorted(
        entries_by_asset.items(),
        key=lambda item: _asset_sort_key(item[0]),
    ):
        timestamps = [entry.start_time for entry in asset_entries if entry.start_time]
        rows.append(
            {
                "asset_space": asset.space if asset else "",
                "asset_external_id": asset.external_id if asset else "",
                "event_count": str(len(asset_entries)),
                "first_event_utc": _format_timestamp(
                    min(timestamps) if timestamps else None
                ),
                "last_event_utc": _format_timestamp(
                    max(timestamps) if timestamps else None
                ),
            }
        )
    return rows


def _references(value: object) -> list[InstanceReference]:
    values = value if isinstance(value, list) else [value]
    return [reference for item in values if (reference := _reference(item))]


def _first_reference(value: object) -> InstanceReference | None:
    references = _references(value)
    return references[0] if references else None


def _reference(value: object) -> InstanceReference | None:
    if isinstance(value, Mapping):
        space = value.get("space")
        external_id = value.get("externalId", value.get("external_id"))
    else:
        space = getattr(value, "space", None)
        external_id = getattr(value, "external_id", None)
    if isinstance(space, str) and isinstance(external_id, str):
        return InstanceReference(space, external_id)
    return None


def _as_datetime(value: object) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return None


def _as_text(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _format_timestamp(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def _format_duration_minutes(entry: EventTimelineEntry) -> str:
    if entry.start_time is None or entry.end_time is None:
        return ""
    duration = (entry.end_time - entry.start_time).total_seconds() / 60
    return format(duration, ".15g").replace(".", ",")


def _entry_sort_key(entry: EventTimelineEntry) -> tuple[str, str, datetime, str]:
    asset_space, asset_external_id = _asset_sort_key(entry.asset)
    return (
        asset_space,
        asset_external_id,
        entry.start_time or datetime.min.replace(tzinfo=UTC),
        entry.event.external_id,
    )


def _asset_sort_key(asset: InstanceReference | None) -> tuple[str, str]:
    return (asset.space, asset.external_id) if asset else ("", "")


def _normalize_property_name(value: str) -> str:
    return "".join(character.lower() for character in value if character.isalnum())


def _view_label(view: ViewId) -> str:
    return f"{view.space}/{view.external_id}/{view.version}"


def _validate_configuration() -> None:
    if not BASE_EVENT_VIEW_EXTERNAL_ID:
        raise ValueError("Set BASE_EVENT_VIEW_EXTERNAL_ID.")
    if not EVENT_INSTANCE_SPACE.strip():
        raise ValueError("Set EVENT_INSTANCE_SPACE.")
    if not EVENT_EXTERNAL_IDS or any(
        not external_id.strip() for external_id in EVENT_EXTERNAL_IDS
    ):
        raise ValueError(
            "Set EVENT_EXTERNAL_IDS with one or more non-empty external IDs."
        )
    if len(set(EVENT_EXTERNAL_IDS)) != len(EVENT_EXTERNAL_IDS):
        raise ValueError("EVENT_EXTERNAL_IDS contains duplicates.")
    for filename in (TIMELINE_OUTPUT_FILENAME, ASSET_SUMMARY_OUTPUT_FILENAME):
        if Path(filename).name != filename or Path(filename).suffix.lower() != ".csv":
            raise ValueError("Output filenames must be CSV filenames without paths.")


if __name__ == "__main__":
    main()
