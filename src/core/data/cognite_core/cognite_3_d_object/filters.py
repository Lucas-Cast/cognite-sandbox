from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    FloatFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_asset.filters import CogniteAssetFilter


Cognite3DObjectFilter = TypedDict(
    "Cognite3DObjectFilter",
    {
        "aliases": StringListFilter,
        "asset": "CogniteAssetFilter",
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "xMax": FloatFilter,
        "xMin": FloatFilter,
        "yMax": FloatFilter,
        "yMin": FloatFilter,
        "zMax": FloatFilter,
        "zMin": FloatFilter,
        "OR": "list[Cognite3DObjectFilter]",
        "AND": "list[Cognite3DObjectFilter]",
        "NOT": "Cognite3DObjectFilter",
    },
    total=False,
)
