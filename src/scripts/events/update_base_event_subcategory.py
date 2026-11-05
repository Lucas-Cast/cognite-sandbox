"""Set the category, and optionally the subcategory, on selected BaseEvent nodes.

Leave ``SUBCATEGORY_EXTERNAL_ID`` empty to keep each event's current subcategory.
Leave ``IS_RECONTEXTUALIZED`` as ``None`` to keep the current flag.
Set ``DELETED_BY_VALUE`` to ``None`` to clear deletedBy.
Edit the configuration below, run once with ``DRY_RUN = True`` to review the
affected events, then change it to ``False`` to write the updates:

    uv run python src/scripts/events/update_base_event_subcategory.py
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
CATEGORY_PROPERTY = "category"
SUBCATEGORY_PROPERTY = "subcategory"
IS_RECONTEXTUALIZED_PROPERTY = "isRecontextualized"
UPDATED_BY_PROPERTY = "updatedBy"
DELETED_BY_PROPERTY = "deletedBy"
UPDATED_BY_VALUE = "PRIN-lucas.castelano@radixeng"
# None clears deletedBy. A non-empty string writes that value.
DELETED_BY_VALUE: str | None = None
# This timestamp is written only when the property is present in BaseEvent.
UPDATED_DATE_PROPERTY = "updatedDate"

# Node spaces used by the event, category, and subcategory nodes.
EVENT_SPACE = "sp_otm_san_dat"
CATEGORY_SPACE = "sp_evt_glb_ref"
SUBCATEGORY_SPACE = "sp_evt_glb_dat"

# Add the external IDs of the events that must receive the category.
EVENT_EXTERNAL_IDS: list[str] = [
    "BEVT-s=1010-PRA-AFA-AFA10-ZN02-CH01.PLC01.gMES_Status_2026-09-01T00:00:10.430000+00:00_9003_0",
    "BEVT-s=1010-PRA-AFA-AFA10-ZN02-CH01.PLC01.gMES_Status_2026-09-01T00:02:57.427000+00:00_9003_0",
]

# The external ID of the target category node, for example "EVCT-SHS".
CATEGORY_EXTERNAL_ID = "EVCT-CHA"

# Leave empty to keep the subcategory already stored on each event.
SUBCATEGORY_EXTERNAL_ID = ""

# True or False writes the flag. None leaves isRecontextualized unchanged.
IS_RECONTEXTUALIZED: bool | None = None

# Keep True to only show the planned changes. Set False to write to CDF.
DRY_RUN = False

# CDF supports bulk writes; this keeps each request at a manageable size.
BATCH_SIZE = 1_000
# ---------------------------------------------------------------------------


def main() -> None:
    """Validate the selected nodes and set their BaseEvent category."""
    event_external_ids = _validated_event_external_ids(EVENT_EXTERNAL_IDS)
    category = _configured_category()
    subcategory = _configured_subcategory()
    is_recontextualized = _configured_is_recontextualized()
    _validate_configuration(event_external_ids, category, subcategory)

    cognite_client = create_cognite_client()
    has_updated_date_property = _validate_view_properties(
        cognite_client,
        subcategory is not None,
        is_recontextualized is not None,
    )
    _validate_node_exists(cognite_client, category, "Category")
    if subcategory is not None:
        _validate_node_exists(cognite_client, subcategory, "Subcategory")
    events = _retrieve_base_events(cognite_client, event_external_ids)

    events_to_update, already_configured = _events_requiring_update(
        events, category, subcategory, is_recontextualized
    )
    updated_date = _utc_timestamp() if has_updated_date_property else None

    print(f"BaseEvent view: {_view_label(BASE_EVENT_VIEW)}")
    print(f"Target category: {_node_label(category)}")
    if subcategory is None:
        print("Target subcategory: unchanged")
    else:
        print(f"Target subcategory: {_node_label(subcategory)}")
    if is_recontextualized is None:
        print("isRecontextualized: unchanged")
    else:
        print(f"isRecontextualized: {is_recontextualized}")
    print(f"Updated by: {UPDATED_BY_VALUE}")
    print(f"Deleted by: {DELETED_BY_VALUE}")
    if updated_date:
        print(f"Updated date: {updated_date}")
    else:
        print(f'Property "{UPDATED_DATE_PROPERTY}" is not in the view; skipping it.')
    print(f"Requested events: {len(event_external_ids)}")
    if already_configured:
        print(f"Already using the target relation(s): {len(already_configured)}")
        for external_id in already_configured:
            print(f"  unchanged: {EVENT_SPACE}/{external_id}")

    if not events_to_update:
        print("No events require an update.")
        return

    print(f"Events to update: {len(events_to_update)}")
    for external_id in events_to_update:
        print(f"  {EVENT_SPACE}/{external_id} -> {_node_label(category)}")

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
                            properties=_properties_to_apply(
                                category,
                                subcategory,
                                is_recontextualized,
                                updated_date,
                            ),
                        )
                    ],
                )
                for external_id in external_id_batch
            ],
            # Do not silently create the target category or subcategory.
            auto_create_direct_relations=False,
        )

    print(f"Updated {len(events_to_update)} BaseEvent node(s).")


def _validate_view_properties(
    cognite_client: CogniteClient,
    subcategory_required: bool,
    is_recontextualized_required: bool,
) -> bool:
    views = cognite_client.data_modeling.views.retrieve(
        BASE_EVENT_VIEW,
        include_inherited_properties=True,
        all_versions=False,
    )
    if not views:
        raise ValueError(f"BaseEvent view not found: {_view_label(BASE_EVENT_VIEW)}")
    properties = views[0].properties
    required_properties = [CATEGORY_PROPERTY, UPDATED_BY_PROPERTY, DELETED_BY_PROPERTY]
    if subcategory_required:
        required_properties.append(SUBCATEGORY_PROPERTY)
    if is_recontextualized_required:
        required_properties.append(IS_RECONTEXTUALIZED_PROPERTY)
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


def _validate_node_exists(
    cognite_client: CogniteClient, target: NodeId, label: str
) -> None:
    result = cognite_client.data_modeling.instances.retrieve(nodes=target)
    if not result.nodes:
        raise ValueError(f"{label} node not found: {_node_label(target)}")


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
    category: NodeId,
    subcategory: NodeId | None,
    is_recontextualized: bool | None,
) -> tuple[list[str], list[str]]:
    events_to_update: list[str] = []
    already_configured: list[str] = []

    for external_id, event in events.items():
        properties = (event.properties or {}).get(BASE_EVENT_VIEW, {})
        category_matches = _same_node_reference(
            properties.get(CATEGORY_PROPERTY), category
        )
        subcategory_matches = subcategory is None or _same_node_reference(
            properties.get(SUBCATEGORY_PROPERTY), subcategory
        )
        flag_matches = is_recontextualized is None or (
            properties.get(IS_RECONTEXTUALIZED_PROPERTY) is is_recontextualized
        )
        deleted_by_matches = properties.get(DELETED_BY_PROPERTY) == DELETED_BY_VALUE
        if (
            category_matches
            and subcategory_matches
            and flag_matches
            and deleted_by_matches
        ):
            already_configured.append(external_id)
        # Audit fields must be updated even when the relations already match.
        events_to_update.append(external_id)
    return events_to_update, already_configured


def _properties_to_apply(
    category: NodeId,
    subcategory: NodeId | None,
    is_recontextualized: bool | None,
    updated_date: str | None,
) -> dict[str, object]:
    """Return the properties to patch. Omitted optional fields stay unchanged."""
    properties: dict[str, object] = {
        CATEGORY_PROPERTY: category,
        UPDATED_BY_PROPERTY: UPDATED_BY_VALUE,
        DELETED_BY_PROPERTY: DELETED_BY_VALUE,
    }
    if subcategory is not None:
        properties[SUBCATEGORY_PROPERTY] = subcategory
    if is_recontextualized is not None:
        properties[IS_RECONTEXTUALIZED_PROPERTY] = is_recontextualized
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


def _configured_category() -> NodeId:
    space = CATEGORY_SPACE.strip()
    external_id = CATEGORY_EXTERNAL_ID.strip()
    if not space or not external_id:
        raise ValueError("Set CATEGORY_SPACE and CATEGORY_EXTERNAL_ID.")
    return NodeId(space, external_id)


def _configured_is_recontextualized() -> bool | None:
    """Return the flag to write, or None when it must stay unchanged."""
    if IS_RECONTEXTUALIZED is not None and not isinstance(IS_RECONTEXTUALIZED, bool):
        raise ValueError("IS_RECONTEXTUALIZED must be True, False, or None.")
    return IS_RECONTEXTUALIZED


def _configured_subcategory() -> NodeId | None:
    """Return the subcategory to write, or None when it must stay unchanged."""
    external_id = SUBCATEGORY_EXTERNAL_ID.strip()
    if not external_id:
        return None
    space = SUBCATEGORY_SPACE.strip()
    if not space:
        raise ValueError("Set SUBCATEGORY_SPACE when SUBCATEGORY_EXTERNAL_ID is set.")
    return NodeId(space, external_id)


def _validate_configuration(
    event_external_ids: Sequence[str],
    category: NodeId,
    subcategory: NodeId | None,
) -> None:
    required_values = {
        "EVENT_SPACE": EVENT_SPACE,
        "CATEGORY_PROPERTY": CATEGORY_PROPERTY,
        "UPDATED_BY_VALUE": UPDATED_BY_VALUE,
    }
    if subcategory is not None:
        required_values["SUBCATEGORY_PROPERTY"] = SUBCATEGORY_PROPERTY
    missing = [name for name, value in required_values.items() if not value.strip()]
    if missing:
        raise ValueError(
            f"Set the following configuration values: {', '.join(missing)}"
        )
    if DELETED_BY_VALUE is not None and (
        not isinstance(DELETED_BY_VALUE, str) or not DELETED_BY_VALUE.strip()
    ):
        raise ValueError(
            "DELETED_BY_VALUE must be a non-empty string, or None to clear deletedBy."
        )
    if not category.external_id.strip():
        raise ValueError("Set CATEGORY_EXTERNAL_ID.")
    if BATCH_SIZE < 1:
        raise ValueError("BATCH_SIZE must be at least 1.")
    if not event_external_ids:
        raise ValueError("Set EVENT_EXTERNAL_IDS.")


def _node_label(node: NodeId) -> str:
    return f"{node.space}/{node.external_id}"


def _batches(values: Sequence[str], size: int) -> Iterable[Sequence[str]]:
    for index in range(0, len(values), size):
        yield values[index : index + size]


def _view_label(view: ViewId) -> str:
    return f"{view.space}/{view.external_id}/{view.version}"


if __name__ == "__main__":
    main()
