from __future__ import annotations

from typing import Literal, TypeAlias

CogniteCadModelQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "type"
]
CogniteCadModelGroupByProperty: TypeAlias = Literal["name", "description", "thumbnail"]
CogniteCadModelAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "thumbnail"
]
CogniteCadModelIncludeProperty: TypeAlias = Literal["thumbnail"]
