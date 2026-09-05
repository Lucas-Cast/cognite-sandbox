from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
    StringListFilter,
)


CogniteFileCategoryFilter = TypedDict(
    "CogniteFileCategoryFilter",
    {
        "aliases": StringListFilter,
        "code": StringFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "standard": StringFilter,
        "standardReference": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteFileCategoryFilter]",
        "AND": "list[CogniteFileCategoryFilter]",
        "NOT": "CogniteFileCategoryFilter",
    },
    total=False,
)
