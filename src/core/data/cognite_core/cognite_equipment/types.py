from __future__ import annotations

from typing import Literal, TypeAlias

CogniteEquipmentQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "sourceId",
    "sourceContext",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "serialNumber",
    "manufacturer",
]
CogniteEquipmentGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "asset",
    "serialNumber",
    "manufacturer",
    "equipmentType",
]
CogniteEquipmentAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "asset",
    "serialNumber",
    "manufacturer",
    "equipmentType",
]
CogniteEquipmentIncludeProperty: TypeAlias = Literal[
    "source", "asset", "equipmentType", "files"
]
