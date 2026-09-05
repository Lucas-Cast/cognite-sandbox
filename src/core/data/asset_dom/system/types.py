from __future__ import annotations

from typing import Literal, TypeAlias

SystemQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "siteAssetTag"
]
SystemGroupByProperty: TypeAlias = Literal[
    "name", "description", "class", "type", "isProductionOutput", "siteAssetTag"
]
SystemAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "class",
    "type",
    "isProductionOutput",
    "siteAssetTag",
]
SystemIncludeProperty: TypeAlias = Literal["machine"]
