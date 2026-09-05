from __future__ import annotations

from typing import Literal, TypeAlias

CogniteAssetTypeQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "code", "standard"
]
CogniteAssetTypeGroupByProperty: TypeAlias = Literal[
    "name", "description", "code", "standard", "assetClass"
]
CogniteAssetTypeAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "code", "standard", "assetClass"
]
CogniteAssetTypeIncludeProperty: TypeAlias = Literal["assetClass"]
