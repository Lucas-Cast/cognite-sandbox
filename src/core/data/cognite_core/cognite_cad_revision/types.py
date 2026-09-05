from __future__ import annotations

from typing import Literal, TypeAlias

CogniteCadRevisionQueryProperty: TypeAlias = Literal["status", "type"]
CogniteCadRevisionGroupByProperty: TypeAlias = Literal[
    "published", "model3D", "revisionId"
]
CogniteCadRevisionAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "published", "model3D", "revisionId"
]
CogniteCadRevisionIncludeProperty: TypeAlias = Literal["model3D"]
