from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    StringFilter,
    StringListFilter,
)


Cognite360ImageStationFilter = TypedDict(
    "Cognite360ImageStationFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "groupType": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "OR": "list[Cognite360ImageStationFilter]",
        "AND": "list[Cognite360ImageStationFilter]",
        "NOT": "Cognite360ImageStationFilter",
    },
    total=False,
)
