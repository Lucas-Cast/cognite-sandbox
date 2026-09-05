from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    FloatFilter,
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..production_order.filters import ProductionOrderFilter


ProductionOrderComponentFilter = TypedDict(
    "ProductionOrderComponentFilter",
    {
        "actualConsumedQuantity": FloatFilter,
        "actualScrapQuantity": FloatFilter,
        "component": InstanceIdFilter,
        "externalId": StringFilter,
        "isBOMComponent": BoolFilter,
        "order": "InstanceIdFilter | ProductionOrderFilter",
        "plannedConsumedQuantity": FloatFilter,
        "quantityUom": InstanceIdFilter,
        "space": StringFilter,
        "OR": "list[ProductionOrderComponentFilter]",
        "AND": "list[ProductionOrderComponentFilter]",
        "NOT": "ProductionOrderComponentFilter",
    },
    total=False,
)
