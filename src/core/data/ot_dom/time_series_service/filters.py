from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
    StringListFilter,
)


TimeSeriesServiceFilter = TypedDict(
    "TimeSeriesServiceFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "OR": "list[TimeSeriesServiceFilter]",
        "AND": "list[TimeSeriesServiceFilter]",
        "NOT": "TimeSeriesServiceFilter",
    },
    total=False,
)
