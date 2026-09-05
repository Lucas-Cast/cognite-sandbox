from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
)


ScrapReasonFilter = TypedDict(
    "ScrapReasonFilter",
    {
        "code": StringFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "space": StringFilter,
        "OR": "list[ScrapReasonFilter]",
        "AND": "list[ScrapReasonFilter]",
        "NOT": "ScrapReasonFilter",
    },
    total=False,
)
