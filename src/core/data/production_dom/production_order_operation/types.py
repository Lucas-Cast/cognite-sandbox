from __future__ import annotations

from typing import Literal, TypeAlias

ProductionOrderOperationQueryProperty: TypeAlias = str
ProductionOrderOperationGroupByProperty: TypeAlias = Literal[
    "actualQuantity", "operation", "productionOrder", "quantityUom", "scrapQuantity"
]
ProductionOrderOperationAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "actualQuantity",
    "operation",
    "productionOrder",
    "quantityUom",
    "scrapQuantity",
]
ProductionOrderOperationIncludeProperty: TypeAlias = Literal[
    "operation", "productionOrder"
]
