from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..time_series_service.filters import TimeSeriesServiceFilter


TimeSeriesSubserviceFilter = TypedDict(
    "TimeSeriesSubserviceFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "timeSeriesService": "InstanceIdFilter | TimeSeriesServiceFilter",
        "OR": "list[TimeSeriesSubserviceFilter]",
        "AND": "list[TimeSeriesSubserviceFilter]",
        "NOT": "TimeSeriesSubserviceFilter",
    },
    total=False,
)
