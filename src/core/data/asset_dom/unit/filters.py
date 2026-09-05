from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..area.filters import AreaFilter

    from ..location_hierarchy.filters import LocationHierarchyFilter

    from ..plant.filters import PlantFilter


UnitFilter = TypedDict(
    "UnitFilter",
    {
        "aliases": StringListFilter,
        "area": "InstanceIdFilter | AreaFilter",
        "class": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "functionalLocation": StringFilter,
        "location": "InstanceIdFilter | LocationHierarchyFilter",
        "name": StringFilter,
        "plant": "InstanceIdFilter | PlantFilter",
        "space": StringFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "OR": "list[UnitFilter]",
        "AND": "list[UnitFilter]",
        "NOT": "UnitFilter",
    },
    total=False,
)
