from __future__ import annotations

from typing import Literal, TypeAlias

ProductionOrderQueryProperty: TypeAlias = Literal[
    "batchNumber", "description", "orderNumber"
]
ProductionOrderGroupByProperty: TypeAlias = Literal[
    "actualQuantity",
    "actualScrapQuantity",
    "batchNumber",
    "bom",
    "description",
    "line",
    "material",
    "orderNumber",
    "plannedQuantity",
    "quantityUom",
    "routing",
    "site",
    "status",
    "type",
]
ProductionOrderAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "actualQuantity",
    "actualScrapQuantity",
    "batchNumber",
    "bom",
    "description",
    "line",
    "material",
    "orderNumber",
    "plannedQuantity",
    "quantityUom",
    "routing",
    "site",
    "status",
    "type",
]
ProductionOrderIncludeProperty: TypeAlias = Literal["routing"]
