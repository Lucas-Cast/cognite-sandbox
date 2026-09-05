from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DateFilter,
    DatetimeFilter,
    FloatFilter,
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..routing.filters import RoutingFilter


ProductionOrderFilter = TypedDict(
    "ProductionOrderFilter",
    {
        "actualFinishDateTime": DatetimeFilter,
        "actualQuantity": FloatFilter,
        "actualScrapQuantity": FloatFilter,
        "actualStartDateTime": DatetimeFilter,
        "batchNumber": StringFilter,
        "bom": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "line": InstanceIdFilter,
        "material": InstanceIdFilter,
        "orderCreationDate": DateFilter,
        "orderNumber": StringFilter,
        "plannedQuantity": FloatFilter,
        "quantityUom": InstanceIdFilter,
        "routing": "InstanceIdFilter | RoutingFilter",
        "scheduledFinishDateTime": DatetimeFilter,
        "scheduledStartDateTime": DatetimeFilter,
        "site": InstanceIdFilter,
        "space": StringFilter,
        "status": InstanceIdFilter,
        "type": InstanceIdFilter,
        "OR": "list[ProductionOrderFilter]",
        "AND": "list[ProductionOrderFilter]",
        "NOT": "ProductionOrderFilter",
    },
    total=False,
)
