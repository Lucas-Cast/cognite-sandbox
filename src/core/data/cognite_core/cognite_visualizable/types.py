from __future__ import annotations

from typing import Literal, TypeAlias

CogniteVisualizableQueryProperty: TypeAlias = str
CogniteVisualizableGroupByProperty: TypeAlias = Literal["object3D"]
CogniteVisualizableAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "object3D"
]
CogniteVisualizableIncludeProperty: TypeAlias = Literal["object3D"]
