from __future__ import annotations

from typing import Literal, TypeAlias

TimeSeriesSubserviceQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases"
]
TimeSeriesSubserviceGroupByProperty: TypeAlias = Literal[
    "name", "description", "timeSeriesService"
]
TimeSeriesSubserviceAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "timeSeriesService"
]
TimeSeriesSubserviceIncludeProperty: TypeAlias = Literal["timeSeriesService"]
