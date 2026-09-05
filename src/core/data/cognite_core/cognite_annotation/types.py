from __future__ import annotations

from typing import Literal, TypeAlias

CogniteAnnotationQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "sourceId",
    "sourceContext",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "status",
]
CogniteAnnotationGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "confidence",
]
CogniteAnnotationAggregationProperty: TypeAlias = Literal[
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
]
CogniteAnnotationIncludeProperty: TypeAlias = Literal["source"]
