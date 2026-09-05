from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
    StringListFilter,
)


CogniteAssetClassFilter = TypedDict(
    "CogniteAssetClassFilter",
    {
        "aliases": StringListFilter,
        "code": StringFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "standard": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteAssetClassFilter]",
        "AND": "list[CogniteAssetClassFilter]",
        "NOT": "CogniteAssetClassFilter",
    },
    total=False,
)
