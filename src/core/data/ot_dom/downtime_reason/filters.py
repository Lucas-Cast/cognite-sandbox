from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    InstanceIdFilter,
    IntFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..raw_time_series.filters import RawTimeSeriesFilter


DowntimeReasonFilter = TypedDict(
    "DowntimeReasonFilter",
    {
        "defaultCategory": InstanceIdFilter,
        "defaultSubcategory": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "needRecontextualization": BoolFilter,
        "needRecontextualizationMinutes": IntFilter,
        "reasonCode": IntFilter,
        "relatedAsset": InstanceIdFilter,
        "relatedAssetState": InstanceIdFilter,
        "space": StringFilter,
        "timeSeries": "InstanceIdFilter | RawTimeSeriesFilter",
        "OR": "list[DowntimeReasonFilter]",
        "AND": "list[DowntimeReasonFilter]",
        "NOT": "DowntimeReasonFilter",
    },
    total=False,
)
