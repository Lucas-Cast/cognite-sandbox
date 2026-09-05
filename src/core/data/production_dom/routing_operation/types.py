from __future__ import annotations

from typing import Literal, TypeAlias

RoutingOperationQueryProperty: TypeAlias = Literal[
    "sourceId", "sourceContext", "sourceCreatedUser", "sourceUpdatedUser", "workCenter"
]
RoutingOperationGroupByProperty: TypeAlias = Literal[
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "material",
    "operationNumber",
    "routing",
    "sequenceGroup",
    "workCenter",
]
RoutingOperationAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "material",
    "operationNumber",
    "routing",
    "sequenceGroup",
    "workCenter",
]
RoutingOperationIncludeProperty: TypeAlias = Literal["routing"]
