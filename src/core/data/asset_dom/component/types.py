from __future__ import annotations

from typing import Literal, TypeAlias

ComponentQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "siteAssetTag"
]
ComponentGroupByProperty: TypeAlias = Literal[
    "name", "description", "class", "type", "material", "siteAssetTag"
]
ComponentAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "class",
    "type",
    "material",
    "siteAssetTag",
]
ComponentIncludeProperty: TypeAlias = Literal["subsystem"]
