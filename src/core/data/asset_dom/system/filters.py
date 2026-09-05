from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


SystemFilter = TypedDict(
    "SystemFilter",
    {
        "aliases": StringListFilter,
        "class": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "isProductionOutput": BoolFilter,
        "machine": InstanceIdListFilter,
        "name": StringFilter,
        "siteAssetTag": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "OR": "list[SystemFilter]",
        "AND": "list[SystemFilter]",
        "NOT": "SystemFilter",
    },
    total=False,
)
