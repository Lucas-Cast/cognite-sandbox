from __future__ import annotations

from typing import Literal, TypeAlias

ResetTypeQueryProperty: TypeAlias = Literal["name", "description", "tags", "aliases"]
ResetTypeGroupByProperty: TypeAlias = Literal["name", "description"]
ResetTypeAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description"
]
ResetTypeIncludeProperty: TypeAlias = str
