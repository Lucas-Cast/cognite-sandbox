from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..site.filters import SiteFilter


LocationHierarchyFilter = TypedDict(
    "LocationHierarchyFilter",
    {
        "class": StringFilter,
        "externalId": StringFilter,
        "site": "InstanceIdFilter | SiteFilter",
        "space": StringFilter,
        "type": StringFilter,
        "OR": "list[LocationHierarchyFilter]",
        "AND": "list[LocationHierarchyFilter]",
        "NOT": "LocationHierarchyFilter",
    },
    total=False,
)
