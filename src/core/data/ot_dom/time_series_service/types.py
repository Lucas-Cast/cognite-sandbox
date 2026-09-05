from __future__ import annotations

from typing import Literal, TypeAlias

TimeSeriesServiceQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases"
]
TimeSeriesServiceGroupByProperty: TypeAlias = Literal["name", "description"]
TimeSeriesServiceAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description"
]
TimeSeriesServiceIncludeProperty: TypeAlias = str
