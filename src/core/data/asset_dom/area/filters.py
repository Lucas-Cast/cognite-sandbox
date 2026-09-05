from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..plant.filters import PlantFilter

    from ..site.filters import SiteFilter


AreaFilter = TypedDict(
    "AreaFilter",
    {
        "aliases": StringListFilter,
        "class": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "functionalLocation": StringFilter,
        "name": StringFilter,
        "plant": "InstanceIdFilter | PlantFilter",
        "site": "InstanceIdFilter | SiteFilter",
        "space": StringFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "OR": "list[AreaFilter]",
        "AND": "list[AreaFilter]",
        "NOT": "AreaFilter",
    },
    total=False,
)
