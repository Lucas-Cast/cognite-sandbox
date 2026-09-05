from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DateFilter,
    DatetimeFilter,
    InstanceIdFilter,
    InstanceIdListFilter,
    IntFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..routing.filters import RoutingFilter


RoutingOperationFilter = TypedDict(
    "RoutingOperationFilter",
    {
        "assets": InstanceIdListFilter,
        "externalId": StringFilter,
        "material": InstanceIdFilter,
        "operationNumber": IntFilter,
        "routing": "InstanceIdFilter | RoutingFilter",
        "sequenceGroup": IntFilter,
        "source": InstanceIdFilter,
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "validFrom": DateFilter,
        "validTo": DateFilter,
        "workCenter": StringFilter,
        "OR": "list[RoutingOperationFilter]",
        "AND": "list[RoutingOperationFilter]",
        "NOT": "RoutingOperationFilter",
    },
    total=False,
)
