from __future__ import annotations

from typing import Literal, TypeAlias

Cognite360ImageAnnotationQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "sourceId",
    "sourceContext",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "status",
    "formatVersion",
]
Cognite360ImageAnnotationGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "confidence",
    "formatVersion",
]
Cognite360ImageAnnotationAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "confidence",
    "formatVersion",
]
Cognite360ImageAnnotationIncludeProperty: TypeAlias = Literal["source"]
