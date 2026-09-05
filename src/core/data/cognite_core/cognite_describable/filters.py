from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
    StringListFilter,
)


CogniteDescribableFilter = TypedDict(
    "CogniteDescribableFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteDescribableFilter]",
        "AND": "list[CogniteDescribableFilter]",
        "NOT": "CogniteDescribableFilter",
    },
    total=False,
)
