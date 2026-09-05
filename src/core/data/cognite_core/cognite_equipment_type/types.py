from __future__ import annotations

from typing import Literal, TypeAlias

CogniteEquipmentTypeQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "code",
    "equipmentClass",
    "standard",
    "standardReference",
]
CogniteEquipmentTypeGroupByProperty: TypeAlias = Literal[
    "name", "description", "code", "equipmentClass", "standard", "standardReference"
]
CogniteEquipmentTypeAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "code",
    "equipmentClass",
    "standard",
    "standardReference",
]
CogniteEquipmentTypeIncludeProperty: TypeAlias = str
