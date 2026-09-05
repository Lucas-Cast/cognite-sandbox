from __future__ import annotations

from typing import Literal, TypeAlias

ZoneQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "functionalLocation",
    "siteAssetTag",
    "workCenter",
]
ZoneGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "class",
    "type",
    "functionalLocation",
    "isBotteneckAsset",
    "isProductionOutput",
    "siteAssetTag",
    "workCenter",
]
ZoneAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "class",
    "type",
    "functionalLocation",
    "isBotteneckAsset",
    "isProductionOutput",
    "siteAssetTag",
    "workCenter",
]
ZoneIncludeProperty: TypeAlias = Literal["line"]
