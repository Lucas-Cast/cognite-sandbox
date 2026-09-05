from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


SubsystemFilter = TypedDict(
    "SubsystemFilter",
    {
        "aliases": StringListFilter,
        "class": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "siteAssetTag": StringFilter,
        "space": StringFilter,
        "system": InstanceIdListFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "OR": "list[SubsystemFilter]",
        "AND": "list[SubsystemFilter]",
        "NOT": "SubsystemFilter",
    },
    total=False,
)
