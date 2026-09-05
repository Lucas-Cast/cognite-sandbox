from __future__ import annotations

from typing import Literal, TypeAlias

CogniteDescribableQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases"
]
CogniteDescribableGroupByProperty: TypeAlias = Literal["name", "description"]
CogniteDescribableAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description"
]
CogniteDescribableIncludeProperty: TypeAlias = str
