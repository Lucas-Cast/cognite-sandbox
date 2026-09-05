from __future__ import annotations

from typing import Literal, TypeAlias

CogniteCadNodeQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "cadNodeReference"
]
CogniteCadNodeGroupByProperty: TypeAlias = Literal[
    "name", "description", "object3D", "model3D", "cadNodeReference"
]
CogniteCadNodeAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "object3D",
    "model3D",
    "cadNodeReference",
]
CogniteCadNodeIncludeProperty: TypeAlias = Literal["object3D", "model3D", "revisions"]
