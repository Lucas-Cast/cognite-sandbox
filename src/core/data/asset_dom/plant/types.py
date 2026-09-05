from __future__ import annotations

from typing import Literal, TypeAlias

PlantQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "sourceId",
    "sourceContext",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "code",
    "functionalLocation",
]
PlantGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "code",
    "functionalLocation",
    "site",
    "class",
    "type",
]
PlantAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "code",
    "functionalLocation",
    "site",
    "class",
    "type",
]
PlantIncludeProperty: TypeAlias = Literal["site"]
