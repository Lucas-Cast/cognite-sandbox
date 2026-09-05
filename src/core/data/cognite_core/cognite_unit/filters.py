from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
    StringListFilter,
)


CogniteUnitFilter = TypedDict(
    "CogniteUnitFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "quantity": StringFilter,
        "source": StringFilter,
        "sourceReference": StringFilter,
        "space": StringFilter,
        "symbol": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteUnitFilter]",
        "AND": "list[CogniteUnitFilter]",
        "NOT": "CogniteUnitFilter",
    },
    total=False,
)
