from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..location_hierarchy.filters import LocationHierarchyFilter

    from ..plant.filters import PlantFilter


MachinesGroupFilter = TypedDict(
    "MachinesGroupFilter",
    {
        "aliases": StringListFilter,
        "businessUnit": InstanceIdListFilter,
        "class": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "location": "InstanceIdFilter | LocationHierarchyFilter",
        "name": StringFilter,
        "plant": "InstanceIdFilter | PlantFilter",
        "product": InstanceIdListFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "unit": InstanceIdListFilter,
        "workCenter": StringListFilter,
        "OR": "list[MachinesGroupFilter]",
        "AND": "list[MachinesGroupFilter]",
        "NOT": "MachinesGroupFilter",
    },
    total=False,
)
