from __future__ import annotations

from typing import Literal, TypeAlias

LocationHierarchyQueryProperty: TypeAlias = Literal["class", "type"]
LocationHierarchyGroupByProperty: TypeAlias = Literal["class", "site", "type"]
LocationHierarchyAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "class", "site", "type"
]
LocationHierarchyIncludeProperty: TypeAlias = Literal["site"]
