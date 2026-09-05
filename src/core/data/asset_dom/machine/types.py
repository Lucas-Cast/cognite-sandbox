from __future__ import annotations

from typing import Literal, TypeAlias

MachineQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "siteAssetTag", "workCenter"
]
MachineGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "class",
    "type",
    "isBotteneckAsset",
    "isProductionOutput",
    "location",
    "siteAssetTag",
]
MachineAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "class",
    "type",
    "isBotteneckAsset",
    "isProductionOutput",
    "location",
    "siteAssetTag",
]
MachineIncludeProperty: TypeAlias = Literal["line", "location", "zone"]
