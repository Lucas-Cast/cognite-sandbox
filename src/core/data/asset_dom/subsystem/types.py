from __future__ import annotations

from typing import Literal, TypeAlias

SubsystemQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "siteAssetTag"
]
SubsystemGroupByProperty: TypeAlias = Literal[
    "name", "description", "class", "type", "siteAssetTag"
]
SubsystemAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "class", "type", "siteAssetTag"
]
SubsystemIncludeProperty: TypeAlias = Literal["system"]
