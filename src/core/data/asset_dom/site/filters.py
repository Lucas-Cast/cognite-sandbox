from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..geo_location_hierarchy.filters import GeoLocationHierarchyFilter


SiteFilter = TypedDict(
    "SiteFilter",
    {
        "aliases": StringListFilter,
        "businessUnit": InstanceIdListFilter,
        "city": "InstanceIdFilter | GeoLocationHierarchyFilter",
        "class": InstanceIdFilter,
        "code": StringFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "siamCode": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "OR": "list[SiteFilter]",
        "AND": "list[SiteFilter]",
        "NOT": "SiteFilter",
    },
    total=False,
)
