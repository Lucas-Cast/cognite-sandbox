from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
    StringListFilter,
)


CogniteEquipmentTypeFilter = TypedDict(
    "CogniteEquipmentTypeFilter",
    {
        "aliases": StringListFilter,
        "code": StringFilter,
        "description": StringFilter,
        "equipmentClass": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "standard": StringFilter,
        "standardReference": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteEquipmentTypeFilter]",
        "AND": "list[CogniteEquipmentTypeFilter]",
        "NOT": "CogniteEquipmentTypeFilter",
    },
    total=False,
)
