from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..location_hierarchy.filters import LocationHierarchyFilter


MachineFilter = TypedDict(
    "MachineFilter",
    {
        "aliases": StringListFilter,
        "businessUnit": InstanceIdListFilter,
        "class": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "isBotteneckAsset": BoolFilter,
        "isProductionOutput": BoolFilter,
        "line": InstanceIdListFilter,
        "location": "InstanceIdFilter | LocationHierarchyFilter",
        "name": StringFilter,
        "siteAssetTag": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "workCenter": StringListFilter,
        "zone": InstanceIdListFilter,
        "OR": "list[MachineFilter]",
        "AND": "list[MachineFilter]",
        "NOT": "MachineFilter",
    },
    total=False,
)
