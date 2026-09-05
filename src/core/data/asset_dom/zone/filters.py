from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


ZoneFilter = TypedDict(
    "ZoneFilter",
    {
        "aliases": StringListFilter,
        "class": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "functionalLocation": StringFilter,
        "isBotteneckAsset": BoolFilter,
        "isProductionOutput": BoolFilter,
        "line": InstanceIdListFilter,
        "name": StringFilter,
        "siteAssetTag": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "workCenter": StringFilter,
        "OR": "list[ZoneFilter]",
        "AND": "list[ZoneFilter]",
        "NOT": "ZoneFilter",
    },
    total=False,
)
