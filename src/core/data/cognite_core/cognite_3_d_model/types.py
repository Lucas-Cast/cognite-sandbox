from __future__ import annotations

from typing import Literal, TypeAlias

Cognite3DModelQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "type"
]
Cognite3DModelGroupByProperty: TypeAlias = Literal["name", "description", "thumbnail"]
Cognite3DModelAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "thumbnail"
]
Cognite3DModelIncludeProperty: TypeAlias = Literal["thumbnail"]
