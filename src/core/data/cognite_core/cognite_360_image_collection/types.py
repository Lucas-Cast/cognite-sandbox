from __future__ import annotations

from typing import Literal, TypeAlias

Cognite360ImageCollectionQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "status", "type"
]
Cognite360ImageCollectionGroupByProperty: TypeAlias = Literal[
    "name", "description", "published", "model3D"
]
Cognite360ImageCollectionAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "published", "model3D"
]
Cognite360ImageCollectionIncludeProperty: TypeAlias = Literal["model3D"]
