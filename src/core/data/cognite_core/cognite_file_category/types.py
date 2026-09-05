from __future__ import annotations

from typing import Literal, TypeAlias

CogniteFileCategoryQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "code", "standard", "standardReference"
]
CogniteFileCategoryGroupByProperty: TypeAlias = Literal[
    "name", "description", "code", "standard", "standardReference"
]
CogniteFileCategoryAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "code",
    "standard",
    "standardReference",
]
CogniteFileCategoryIncludeProperty: TypeAlias = str
