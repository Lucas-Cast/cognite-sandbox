from __future__ import annotations

from typing import Literal, TypeAlias

UnitQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "functionalLocation"
]
UnitGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "class",
    "type",
    "area",
    "functionalLocation",
    "location",
    "plant",
]
UnitAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "class",
    "type",
    "area",
    "functionalLocation",
    "location",
    "plant",
]
UnitIncludeProperty: TypeAlias = Literal["area", "location", "plant"]
