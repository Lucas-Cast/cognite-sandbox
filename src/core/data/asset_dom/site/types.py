from __future__ import annotations

from typing import Literal, TypeAlias

SiteQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "code", "siamCode"
]
SiteGroupByProperty: TypeAlias = Literal[
    "name", "description", "class", "type", "city", "code", "siamCode"
]
SiteAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "class",
    "type",
    "city",
    "code",
    "siamCode",
]
SiteIncludeProperty: TypeAlias = Literal["city"]
