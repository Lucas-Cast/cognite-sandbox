from __future__ import annotations

from typing import Literal, TypeAlias

ProductionOrderStatusChangeQueryProperty: TypeAlias = str
ProductionOrderStatusChangeGroupByProperty: TypeAlias = Literal[
    "productionOrder", "status"
]
ProductionOrderStatusChangeAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "productionOrder", "status"
]
ProductionOrderStatusChangeIncludeProperty: TypeAlias = Literal["productionOrder"]
