from __future__ import annotations

from typing import Literal, TypeAlias

CogniteAssetClassQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "code", "standard"
]
CogniteAssetClassGroupByProperty: TypeAlias = Literal[
    "name", "description", "code", "standard"
]
CogniteAssetClassAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "code", "standard"
]
CogniteAssetClassIncludeProperty: TypeAlias = str
