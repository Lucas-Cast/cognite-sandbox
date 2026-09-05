from __future__ import annotations

from typing import Literal, TypeAlias

GeoLocationHierarchyQueryProperty: TypeAlias = Literal["class", "type"]
GeoLocationHierarchyGroupByProperty: TypeAlias = Literal["class", "timeZone", "type"]
GeoLocationHierarchyAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "class", "timeZone", "type"
]
GeoLocationHierarchyIncludeProperty: TypeAlias = str
