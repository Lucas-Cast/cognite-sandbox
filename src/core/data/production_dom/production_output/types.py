from __future__ import annotations

from typing import Literal, TypeAlias

ProductionOutputQueryProperty: TypeAlias = str
ProductionOutputGroupByProperty: TypeAlias = Literal[
    "asset", "designOutput", "material", "nominalSpeed", "uom"
]
ProductionOutputAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "asset", "designOutput", "material", "nominalSpeed", "uom"
]
ProductionOutputIncludeProperty: TypeAlias = str
