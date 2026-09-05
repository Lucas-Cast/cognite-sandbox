from __future__ import annotations

from typing import Literal, TypeAlias

CogniteUnitQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "symbol",
    "quantity",
    "source",
    "sourceReference",
]
CogniteUnitGroupByProperty: TypeAlias = Literal[
    "name", "description", "symbol", "quantity", "source", "sourceReference"
]
CogniteUnitAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "symbol",
    "quantity",
    "source",
    "sourceReference",
]
CogniteUnitIncludeProperty: TypeAlias = str
