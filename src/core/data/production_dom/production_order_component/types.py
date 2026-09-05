from __future__ import annotations

from typing import Literal, TypeAlias

ProductionOrderComponentQueryProperty: TypeAlias = str
ProductionOrderComponentGroupByProperty: TypeAlias = Literal[
    "actualConsumedQuantity",
    "actualScrapQuantity",
    "component",
    "isBOMComponent",
    "order",
    "plannedConsumedQuantity",
    "quantityUom",
]
ProductionOrderComponentAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "actualConsumedQuantity",
    "actualScrapQuantity",
    "component",
    "isBOMComponent",
    "order",
    "plannedConsumedQuantity",
    "quantityUom",
]
ProductionOrderComponentIncludeProperty: TypeAlias = Literal["order"]
