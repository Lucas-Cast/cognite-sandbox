from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    DatetimeFilter,
    FloatFilter,
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..scrap_reason.filters import ScrapReasonFilter

    from ..time_series_service.filters import TimeSeriesServiceFilter

    from ..time_series_subservice.filters import TimeSeriesSubserviceFilter


CuratedTimeSeriesFilter = TypedDict(
    "CuratedTimeSeriesFilter",
    {
        "aliases": StringListFilter,
        "assets": InstanceIdListFilter,
        "description": StringFilter,
        "equipment": InstanceIdListFilter,
        "externalId": StringFilter,
        "inputTags": InstanceIdListFilter,
        "isActive": BoolFilter,
        "isManualInput": BoolFilter,
        "isStep": BoolFilter,
        "maxValue": FloatFilter,
        "minValue": FloatFilter,
        "name": StringFilter,
        "scrapReason": "InstanceIdFilter | ScrapReasonFilter",
        "source": InstanceIdFilter,
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUnit": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "stateSet": InstanceIdFilter,
        "tags": StringListFilter,
        "targetValue": FloatFilter,
        "timeSeriesService": "InstanceIdFilter | TimeSeriesServiceFilter",
        "timeSeriesSubservice": "InstanceIdFilter | TimeSeriesSubserviceFilter",
        "type": StringFilter,
        "typicalValue": FloatFilter,
        "unit": InstanceIdFilter,
        "uom": InstanceIdFilter,
        "OR": "list[CuratedTimeSeriesFilter]",
        "AND": "list[CuratedTimeSeriesFilter]",
        "NOT": "CuratedTimeSeriesFilter",
    },
    total=False,
)
