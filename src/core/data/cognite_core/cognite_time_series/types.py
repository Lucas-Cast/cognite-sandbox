from __future__ import annotations

from typing import Literal, TypeAlias

CogniteTimeSeriesQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "sourceId",
    "sourceContext",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "type",
    "sourceUnit",
]
CogniteTimeSeriesGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "isStep",
    "sourceUnit",
    "unit",
    "stateSet",
]
CogniteTimeSeriesAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "isStep",
    "sourceUnit",
    "unit",
    "stateSet",
]
CogniteTimeSeriesIncludeProperty: TypeAlias = Literal[
    "source", "unit", "assets", "equipment"
]
