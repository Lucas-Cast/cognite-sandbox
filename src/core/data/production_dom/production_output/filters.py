from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    FloatFilter,
    InstanceIdFilter,
    StringFilter,
)


ProductionOutputFilter = TypedDict(
    "ProductionOutputFilter",
    {
        "asset": InstanceIdFilter,
        "designOutput": FloatFilter,
        "externalId": StringFilter,
        "material": InstanceIdFilter,
        "nominalSpeed": FloatFilter,
        "space": StringFilter,
        "uom": InstanceIdFilter,
        "OR": "list[ProductionOutputFilter]",
        "AND": "list[ProductionOutputFilter]",
        "NOT": "ProductionOutputFilter",
    },
    total=False,
)
