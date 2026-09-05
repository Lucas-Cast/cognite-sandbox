from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
    StringListFilter,
)


ResetTypeFilter = TypedDict(
    "ResetTypeFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "OR": "list[ResetTypeFilter]",
        "AND": "list[ResetTypeFilter]",
        "NOT": "ResetTypeFilter",
    },
    total=False,
)
