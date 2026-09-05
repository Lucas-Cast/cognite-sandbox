from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..production_order.filters import ProductionOrderFilter


ProductionOrderStatusChangeFilter = TypedDict(
    "ProductionOrderStatusChangeFilter",
    {
        "endDateTime": DatetimeFilter,
        "externalId": StringFilter,
        "productionOrder": "InstanceIdFilter | ProductionOrderFilter",
        "space": StringFilter,
        "startDateTime": DatetimeFilter,
        "status": InstanceIdFilter,
        "OR": "list[ProductionOrderStatusChangeFilter]",
        "AND": "list[ProductionOrderStatusChangeFilter]",
        "NOT": "ProductionOrderStatusChangeFilter",
    },
    total=False,
)
