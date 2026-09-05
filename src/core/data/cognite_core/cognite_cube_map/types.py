from __future__ import annotations

from typing import Literal, TypeAlias

CogniteCubeMapQueryProperty: TypeAlias = str
CogniteCubeMapGroupByProperty: TypeAlias = Literal[
    "front", "back", "left", "right", "top", "bottom"
]
CogniteCubeMapAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "front", "back", "left", "right", "top", "bottom"
]
CogniteCubeMapIncludeProperty: TypeAlias = Literal[
    "front", "back", "left", "right", "top", "bottom"
]
