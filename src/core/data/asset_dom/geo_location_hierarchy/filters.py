from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
)


GeoLocationHierarchyFilter = TypedDict(
    "GeoLocationHierarchyFilter",
    {
        "class": StringFilter,
        "externalId": StringFilter,
        "space": StringFilter,
        "timeZone": InstanceIdFilter,
        "type": StringFilter,
        "OR": "list[GeoLocationHierarchyFilter]",
        "AND": "list[GeoLocationHierarchyFilter]",
        "NOT": "GeoLocationHierarchyFilter",
    },
    total=False,
)
