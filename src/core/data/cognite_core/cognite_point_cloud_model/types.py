from __future__ import annotations

from typing import Literal, TypeAlias

CognitePointCloudModelQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "type"
]
CognitePointCloudModelGroupByProperty: TypeAlias = Literal[
    "name", "description", "thumbnail"
]
CognitePointCloudModelAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "thumbnail"
]
CognitePointCloudModelIncludeProperty: TypeAlias = Literal["thumbnail"]
