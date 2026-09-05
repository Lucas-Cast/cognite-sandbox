from __future__ import annotations

from typing import Literal, TypeAlias

Cognite3DObjectQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases"
]
Cognite3DObjectGroupByProperty: TypeAlias = Literal[
    "name", "description", "xMin", "xMax", "yMin", "yMax", "zMin", "zMax"
]
Cognite3DObjectAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "xMin",
    "xMax",
    "yMin",
    "yMax",
    "zMin",
    "zMax",
]
Cognite3DObjectIncludeProperty: TypeAlias = Literal["asset", "images360"]
