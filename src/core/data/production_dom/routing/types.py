from __future__ import annotations

from typing import Literal, TypeAlias

RoutingQueryProperty: TypeAlias = Literal[
    "sourceId", "sourceContext", "sourceCreatedUser", "sourceUpdatedUser", "number"
]
RoutingGroupByProperty: TypeAlias = Literal[
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "number",
]
RoutingAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "number",
]
RoutingIncludeProperty: TypeAlias = str
