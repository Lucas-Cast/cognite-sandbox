from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


ElementFilter = TypedDict(
    "ElementFilter",
    {
        "aliases": StringListFilter,
        "class": InstanceIdFilter,
        "component": InstanceIdListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "material": InstanceIdFilter,
        "name": StringFilter,
        "siteAssetTag": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "OR": "list[ElementFilter]",
        "AND": "list[ElementFilter]",
        "NOT": "ElementFilter",
    },
    total=False,
)
