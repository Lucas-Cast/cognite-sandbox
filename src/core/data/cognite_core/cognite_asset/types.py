from __future__ import annotations

from typing import Literal, TypeAlias

CogniteAssetQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "sourceId",
    "sourceContext",
    "sourceCreatedUser",
    "sourceUpdatedUser",
]
CogniteAssetGroupByProperty: TypeAlias = Literal[
    "object3D",
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "parent",
    "root",
    "assetClass",
    "type",
]
CogniteAssetAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "object3D",
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "parent",
    "root",
    "assetClass",
    "type",
]
CogniteAssetIncludeProperty: TypeAlias = Literal[
    "object3D", "source", "parent", "root", "path", "assetClass", "type"
]
