from __future__ import annotations

from typing import Literal, TypeAlias

MachinesGroupQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "workCenter"
]
MachinesGroupGroupByProperty: TypeAlias = Literal[
    "name", "description", "class", "type", "location", "plant"
]
MachinesGroupAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "class", "type", "location", "plant"
]
MachinesGroupIncludeProperty: TypeAlias = Literal["location", "plant", "unit"]
