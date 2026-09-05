from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_asset_class.filters import CogniteAssetClassFilter


CogniteAssetTypeFilter = TypedDict(
    "CogniteAssetTypeFilter",
    {
        "aliases": StringListFilter,
        "assetClass": "InstanceIdFilter | CogniteAssetClassFilter",
        "code": StringFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "standard": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteAssetTypeFilter]",
        "AND": "list[CogniteAssetTypeFilter]",
        "NOT": "CogniteAssetTypeFilter",
    },
    total=False,
)
