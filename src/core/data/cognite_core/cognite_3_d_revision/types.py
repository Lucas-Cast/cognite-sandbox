from __future__ import annotations

from typing import Literal, TypeAlias

Cognite3DRevisionQueryProperty: TypeAlias = Literal["status", "type"]
Cognite3DRevisionGroupByProperty: TypeAlias = Literal["published", "model3D"]
Cognite3DRevisionAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "published", "model3D"
]
Cognite3DRevisionIncludeProperty: TypeAlias = Literal["model3D"]
