"""Set a subcategory and audit fields on selected BaseEvent nodes in CDF.

Edit the configuration below, run once with ``DRY_RUN = True`` to review the
affected events, then change it to ``False`` to write the updates:

    uv run python src/scripts/update_base_event_subcategory.py
"""

from __future__ import annotations

import sys
from collections.abc import Iterable, Sequence
from datetime import UTC, datetime
from pathlib import Path

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import (
    NodeApply,
    NodeId,
    NodeOrEdgeData,
    ViewId,
)

sys.path.insert(0, str(Path(__file__).parents[2]))

from core import create_cognite_client

# --- Configuration ---------------------------------------------------------
# Canonical BaseEvent view.
BASE_EVENT_VIEW = ViewId("sp_evt_glb_dmd", "BaseEvent", "v1.0.0")
SUBCATEGORY_PROPERTY = "subcategory"
UPDATED_BY_PROPERTY = "updatedBy"
UPDATED_BY_VALUE = "PERS-lucas.castelano@radixeng.com"
# This timestamp is written only when the property is present in BaseEvent.
UPDATED_DATE_PROPERTY = "updatedDate"

# Node spaces used by the event and subcategory nodes.
EVENT_SPACE = "sp_otm_san_dat"
SUBCATEGORY_SPACE = "sp_evt_glb_dat"

# Add the external IDs of the events that must receive the subcategory.
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

# The external ID of the target EventSubcategory node.
SUBCATEGORY_EXTERNAL_ID = "ESCA-RAU-BRK"

# Keep True to only show the planned changes. Set False to write to CDF.
DRY_RUN = False

# CDF supports bulk writes; this keeps each request at a manageable size.
BATCH_SIZE = 1_000
# ---------------------------------------------------------------------------


def main() -> None:
    """Validate the selected nodes and set their BaseEvent subcategory."""
    event_external_ids = _validated_event_external_ids(EVENT_EXTERNAL_IDS)
    _validate_configuration(event_external_ids)

    cognite_client = create_cognite_client()
    has_updated_date_property = _validate_view_properties(cognite_client)
    _validate_subcategory_exists(cognite_client)
    events = _retrieve_base_events(cognite_client, event_external_ids)

    events_to_update, already_configured = _events_requiring_update(events)
    target = f"{SUBCATEGORY_SPACE}/{SUBCATEGORY_EXTERNAL_ID}"
    updated_date = _utc_timestamp() if has_updated_date_property else None

    print(f"BaseEvent view: {_view_label(BASE_EVENT_VIEW)}")
    print(f"Target subcategory: {target}")
    print(f"Updated by: {UPDATED_BY_VALUE}")
    if updated_date:
        print(f"Updated date: {updated_date}")
    else:
        print(f'Property "{UPDATED_DATE_PROPERTY}" is not in the view; skipping it.')
    print(f"Requested events: {len(event_external_ids)}")
    if already_configured:
        print(f"Already using the target subcategory: {len(already_configured)}")
        for external_id in already_configured:
            print(f"  unchanged: {EVENT_SPACE}/{external_id}")

    if not events_to_update:
        print("No events require an update.")
        return

    print(f"Events to update: {len(events_to_update)}")
    for external_id in events_to_update:
        print(f"  {EVENT_SPACE}/{external_id} -> {target}")

    if DRY_RUN:
        print("Dry run enabled: no changes were written to CDF.")
        return

    for external_id_batch in _batches(events_to_update, BATCH_SIZE):
        cognite_client.data_modeling.instances.apply(
            nodes=[
                NodeApply(
                    space=EVENT_SPACE,
                    external_id=external_id,
                    sources=[
                        NodeOrEdgeData(
                            source=BASE_EVENT_VIEW,
                            properties=_properties_to_apply(updated_date),
                        )
                    ],
                )
                for external_id in external_id_batch
            ],
            # Do not silently create the target subcategory when it is invalid.
            auto_create_direct_relations=False,
        )

    print(f"Updated {len(events_to_update)} BaseEvent node(s).")


def _validate_view_properties(cognite_client: CogniteClient) -> bool:
    views = cognite_client.data_modeling.views.retrieve(
        BASE_EVENT_VIEW,
        include_inherited_properties=True,
        all_versions=False,
    )
    if not views:
        raise ValueError(f"BaseEvent view not found: {_view_label(BASE_EVENT_VIEW)}")
    properties = views[0].properties
    required_properties = (SUBCATEGORY_PROPERTY, UPDATED_BY_PROPERTY)
    missing_properties = [
        property_name
        for property_name in required_properties
        if property_name not in properties
    ]
    if missing_properties:
        available = ", ".join(sorted(views[0].properties))
        raise ValueError(
            "The following property/properties are not available in "
            f"{_view_label(BASE_EVENT_VIEW)}: {', '.join(missing_properties)}. "
            f"Available properties: {available}"
        )
    return UPDATED_DATE_PROPERTY in properties


def _validate_subcategory_exists(cognite_client: CogniteClient) -> None:
    target = NodeId(SUBCATEGORY_SPACE, SUBCATEGORY_EXTERNAL_ID)
    result = cognite_client.data_modeling.instances.retrieve(nodes=target)
    if not result.nodes:
        raise ValueError(
            f"Subcategory node not found: {SUBCATEGORY_SPACE}/{SUBCATEGORY_EXTERNAL_ID}"
        )


def _retrieve_base_events(
    cognite_client: CogniteClient, event_external_ids: Sequence[str]
) -> dict[str, object]:
    """Read every requested event before applying changes, avoiding new nodes."""
    result = cognite_client.data_modeling.instances.retrieve(
        nodes=[NodeId(EVENT_SPACE, external_id) for external_id in event_external_ids],
        sources=BASE_EVENT_VIEW,
    )
    events_by_external_id = {event.external_id: event for event in result.nodes}

    missing = [
        external_id
        for external_id in event_external_ids
        if external_id not in events_by_external_id
    ]
    if missing:
        raise ValueError(
            "The following BaseEvent node(s) were not found in "
            f"{EVENT_SPACE}: {', '.join(missing)}"
        )

    not_base_events = [
        external_id
        for external_id, event in events_by_external_id.items()
        if BASE_EVENT_VIEW not in (event.properties or {})
    ]
    if not_base_events:
        raise ValueError(
            "The following node(s) do not have the configured BaseEvent view "
            f"({_view_label(BASE_EVENT_VIEW)}): {', '.join(not_base_events)}"
        )
    return events_by_external_id


def _events_requiring_update(
    events: dict[str, object],
) -> tuple[list[str], list[str]]:
    target = NodeId(SUBCATEGORY_SPACE, SUBCATEGORY_EXTERNAL_ID)
    events_to_update: list[str] = []
    already_configured: list[str] = []

    for external_id, event in events.items():
        properties = (event.properties or {}).get(BASE_EVENT_VIEW, {})
        if _same_node_reference(properties.get(SUBCATEGORY_PROPERTY), target):
            already_configured.append(external_id)
        # Audit fields must be updated even when the subcategory already matches.
        events_to_update.append(external_id)
    return events_to_update, already_configured


def _properties_to_apply(updated_date: str | None) -> dict[str, object]:
    properties: dict[str, object] = {
        SUBCATEGORY_PROPERTY: NodeId(SUBCATEGORY_SPACE, SUBCATEGORY_EXTERNAL_ID),
        UPDATED_BY_PROPERTY: UPDATED_BY_VALUE,
    }
    if updated_date is not None:
        properties[UPDATED_DATE_PROPERTY] = updated_date
    return properties


def _utc_timestamp() -> str:
    """Return an ISO 8601 UTC timestamp accepted by CDF timestamp properties."""
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _same_node_reference(value: object, target: NodeId) -> bool:
    """Return whether a direct-relation value refers to the target node."""
    if isinstance(value, NodeId):
        return value == target
    if isinstance(value, dict):
        return (
            value.get("space") == target.space
            and value.get("externalId", value.get("external_id")) == target.external_id
        )
    return (
        getattr(value, "space", None) == target.space
        and getattr(value, "external_id", None) == target.external_id
    )


def _validated_event_external_ids(event_external_ids: Iterable[str]) -> list[str]:
    cleaned = [external_id.strip() for external_id in event_external_ids]
    if not cleaned or any(not external_id for external_id in cleaned):
        raise ValueError(
            "Set EVENT_EXTERNAL_IDS with at least one non-empty external ID."
        )
    duplicates = sorted(
        {external_id for external_id in cleaned if cleaned.count(external_id) > 1}
    )
    if duplicates:
        raise ValueError(
            f"EVENT_EXTERNAL_IDS contains duplicates: {', '.join(duplicates)}"
        )
    return cleaned


def _validate_configuration(event_external_ids: Sequence[str]) -> None:
    required_values = {
        "EVENT_SPACE": EVENT_SPACE,
        "SUBCATEGORY_SPACE": SUBCATEGORY_SPACE,
        "SUBCATEGORY_EXTERNAL_ID": SUBCATEGORY_EXTERNAL_ID,
        "SUBCATEGORY_PROPERTY": SUBCATEGORY_PROPERTY,
    }
    missing = [name for name, value in required_values.items() if not value.strip()]
    if missing:
        raise ValueError(
            f"Set the following configuration values: {', '.join(missing)}"
        )
    if BATCH_SIZE < 1:
        raise ValueError("BATCH_SIZE must be at least 1.")
    if not event_external_ids:
        raise ValueError("Set EVENT_EXTERNAL_IDS.")


def _batches(values: Sequence[str], size: int) -> Iterable[Sequence[str]]:
    for index in range(0, len(values), size):
        yield values[index : index + size]


def _view_label(view: ViewId) -> str:
    return f"{view.space}/{view.external_id}/{view.version}"


if __name__ == "__main__":
    main()
