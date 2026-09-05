from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    InstanceIdFilter,
    StringFilter,
)


RoutingFilter = TypedDict(
    "RoutingFilter",
    {
        "externalId": StringFilter,
        "number": StringFilter,
        "source": InstanceIdFilter,
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "OR": "list[RoutingFilter]",
        "AND": "list[RoutingFilter]",
        "NOT": "RoutingFilter",
    },
    total=False,
)
