from __future__ import annotations

from typing import Literal, TypeAlias

ElementQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "siteAssetTag"
]
ElementGroupByProperty: TypeAlias = Literal[
    "name", "description", "class", "type", "material", "siteAssetTag"
]
ElementAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "class",
    "type",
    "material",
    "siteAssetTag",
]
ElementIncludeProperty: TypeAlias = Literal["component"]
