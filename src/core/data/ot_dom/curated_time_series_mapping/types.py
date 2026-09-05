from __future__ import annotations

from typing import Literal, TypeAlias

CuratedTimeSeriesMappingQueryProperty: TypeAlias = Literal[
    "inputDataType", "outputDescription"
]
CuratedTimeSeriesMappingGroupByProperty: TypeAlias = Literal[
    "curatedTimeSeries", "outputDescription", "outputValue", "rawTimeSeries", "rule"
]
CuratedTimeSeriesMappingAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "curatedTimeSeries",
    "outputDescription",
    "outputValue",
    "rawTimeSeries",
    "rule",
]
CuratedTimeSeriesMappingIncludeProperty: TypeAlias = Literal[
    "curatedTimeSeries", "rawTimeSeries"
]
