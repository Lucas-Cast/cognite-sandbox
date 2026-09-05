from __future__ import annotations

from typing import Literal, TypeAlias

Cognite360ImageModelQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "type"
]
Cognite360ImageModelGroupByProperty: TypeAlias = Literal[
    "name", "description", "thumbnail"
]
Cognite360ImageModelAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "thumbnail"
]
Cognite360ImageModelIncludeProperty: TypeAlias = Literal["thumbnail"]
