from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_3_d_object.filters import Cognite3DObjectFilter

    from ..cognite_asset_class.filters import CogniteAssetClassFilter

    from ..cognite_asset_type.filters import CogniteAssetTypeFilter

    from ..cognite_source_system.filters import CogniteSourceSystemFilter


CogniteAssetFilter = TypedDict(
    "CogniteAssetFilter",
    {
        "aliases": StringListFilter,
        "assetClass": "InstanceIdFilter | CogniteAssetClassFilter",
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "object3D": "InstanceIdFilter | Cognite3DObjectFilter",
        "parent": "InstanceIdFilter | CogniteAssetFilter",
        "path": InstanceIdListFilter,
        "pathLastUpdatedTime": DatetimeFilter,
        "root": "InstanceIdFilter | CogniteAssetFilter",
        "source": "InstanceIdFilter | CogniteSourceSystemFilter",
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "type": "InstanceIdFilter | CogniteAssetTypeFilter",
        "OR": "list[CogniteAssetFilter]",
        "AND": "list[CogniteAssetFilter]",
        "NOT": "CogniteAssetFilter",
    },
    total=False,
)
