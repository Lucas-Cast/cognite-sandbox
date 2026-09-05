from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
    StringListFilter,
)


CogniteSourceSystemFilter = TypedDict(
    "CogniteSourceSystemFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "manufacturer": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "version": StringFilter,
        "OR": "list[CogniteSourceSystemFilter]",
        "AND": "list[CogniteSourceSystemFilter]",
        "NOT": "CogniteSourceSystemFilter",
    },
    total=False,
)
