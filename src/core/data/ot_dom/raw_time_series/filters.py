from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    DatetimeFilter,
    FloatFilter,
    InstanceIdFilter,
    InstanceIdListFilter,
    IntFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..reset_type.filters import ResetTypeFilter

    from ..scrap_reason.filters import ScrapReasonFilter

    from ..time_series_service.filters import TimeSeriesServiceFilter

    from ..time_series_subservice.filters import TimeSeriesSubserviceFilter


RawTimeSeriesFilter = TypedDict(
    "RawTimeSeriesFilter",
    {
        "aliases": StringListFilter,
        "assets": InstanceIdListFilter,
        "counterMaxDelta": IntFilter,
        "counterRollOver": IntFilter,
        "description": StringFilter,
        "equipment": InstanceIdListFilter,
        "externalId": StringFilter,
        "isActive": BoolFilter,
        "isManualInput": BoolFilter,
        "isStep": BoolFilter,
        "maxValue": FloatFilter,
        "minValue": FloatFilter,
        "name": StringFilter,
        "resetType": "InstanceIdFilter | ResetTypeFilter",
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
        "OR": "list[RawTimeSeriesFilter]",
        "AND": "list[RawTimeSeriesFilter]",
        "NOT": "RawTimeSeriesFilter",
    },
    total=False,
)
