from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..site.filters import SiteFilter


PlantFilter = TypedDict(
    "PlantFilter",
    {
        "aliases": StringListFilter,
        "class": InstanceIdFilter,
        "code": StringFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "functionalLocation": StringFilter,
        "name": StringFilter,
        "site": "InstanceIdFilter | SiteFilter",
        "source": InstanceIdFilter,
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "OR": "list[PlantFilter]",
        "AND": "list[PlantFilter]",
        "NOT": "PlantFilter",
    },
    total=False,
)
