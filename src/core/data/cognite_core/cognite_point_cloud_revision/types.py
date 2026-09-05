from __future__ import annotations

from typing import Literal, TypeAlias

CognitePointCloudRevisionQueryProperty: TypeAlias = Literal["status", "type"]
CognitePointCloudRevisionGroupByProperty: TypeAlias = Literal[
    "published", "model3D", "revisionId"
]
CognitePointCloudRevisionAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "published", "model3D", "revisionId"
]
CognitePointCloudRevisionIncludeProperty: TypeAlias = Literal["model3D"]
