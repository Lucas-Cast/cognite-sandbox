from __future__ import annotations

from typing import Literal, TypeAlias

CuratedTimeSeriesQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "sourceId",
    "sourceContext",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "type",
    "sourceUnit",
]
CuratedTimeSeriesGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "isStep",
    "sourceUnit",
    "unit",
    "stateSet",
    "isActive",
    "isManualInput",
    "maxValue",
    "minValue",
    "scrapReason",
    "targetValue",
    "timeSeriesService",
    "timeSeriesSubservice",
    "typicalValue",
    "uom",
]
CuratedTimeSeriesAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "isStep",
    "sourceUnit",
    "unit",
    "stateSet",
    "isActive",
    "isManualInput",
    "maxValue",
    "minValue",
    "scrapReason",
    "targetValue",
    "timeSeriesService",
    "timeSeriesSubservice",
    "typicalValue",
    "uom",
]
CuratedTimeSeriesIncludeProperty: TypeAlias = Literal[
    "inputTags", "scrapReason", "timeSeriesService", "timeSeriesSubservice"
]
