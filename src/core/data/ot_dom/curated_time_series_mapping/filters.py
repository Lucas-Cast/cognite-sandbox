from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    FloatFilter,
    InstanceIdFilter,
    IntFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..curated_time_series.filters import CuratedTimeSeriesFilter

    from ..raw_time_series.filters import RawTimeSeriesFilter


CuratedTimeSeriesMappingFilter = TypedDict(
    "CuratedTimeSeriesMappingFilter",
    {
        "curatedTimeSeries": "InstanceIdFilter | CuratedTimeSeriesFilter",
        "externalId": StringFilter,
        "inputDataType": StringFilter,
        "outputDescription": StringFilter,
        "outputValue": FloatFilter,
        "rawTimeSeries": "InstanceIdFilter | RawTimeSeriesFilter",
        "rule": IntFilter,
        "space": StringFilter,
        "OR": "list[CuratedTimeSeriesMappingFilter]",
        "AND": "list[CuratedTimeSeriesMappingFilter]",
        "NOT": "CuratedTimeSeriesMappingFilter",
    },
    total=False,
)
