from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    FloatFilter,
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..production_order.filters import ProductionOrderFilter


ProductionOrderOutputFilter = TypedDict(
    "ProductionOrderOutputFilter",
    {
        "actualQuantity": FloatFilter,
        "externalId": StringFilter,
        "material": InstanceIdFilter,
        "productionOrder": "InstanceIdFilter | ProductionOrderFilter",
        "quantityUom": InstanceIdFilter,
        "serialNumber": StringFilter,
        "space": StringFilter,
        "OR": "list[ProductionOrderOutputFilter]",
        "AND": "list[ProductionOrderOutputFilter]",
        "NOT": "ProductionOrderOutputFilter",
    },
    total=False,
)
