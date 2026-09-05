from __future__ import annotations

from typing import Literal, TypeAlias

ScrapReasonQueryProperty: TypeAlias = Literal["code", "description"]
ScrapReasonGroupByProperty: TypeAlias = Literal["code", "description"]
ScrapReasonAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "code", "description"
]
ScrapReasonIncludeProperty: TypeAlias = str
