from __future__ import annotations

from typing import Literal, TypeAlias

ProductionOrderOutputQueryProperty: TypeAlias = Literal["serialNumber"]
ProductionOrderOutputGroupByProperty: TypeAlias = Literal[
    "actualQuantity", "material", "productionOrder", "quantityUom", "serialNumber"
]
ProductionOrderOutputAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "actualQuantity",
    "material",
    "productionOrder",
    "quantityUom",
    "serialNumber",
]
ProductionOrderOutputIncludeProperty: TypeAlias = Literal["productionOrder"]
