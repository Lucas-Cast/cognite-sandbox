from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    FloatFilter,
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..production_order.filters import ProductionOrderFilter

    from ..routing_operation.filters import RoutingOperationFilter


ProductionOrderOperationFilter = TypedDict(
    "ProductionOrderOperationFilter",
    {
        "actualQuantity": FloatFilter,
        "endDateTime": DatetimeFilter,
        "externalId": StringFilter,
        "operation": "InstanceIdFilter | RoutingOperationFilter",
        "productionOrder": "InstanceIdFilter | ProductionOrderFilter",
        "quantityUom": InstanceIdFilter,
        "scrapQuantity": FloatFilter,
        "space": StringFilter,
        "startDateTime": DatetimeFilter,
        "OR": "list[ProductionOrderOperationFilter]",
        "AND": "list[ProductionOrderOperationFilter]",
        "NOT": "ProductionOrderOperationFilter",
    },
    total=False,
)
