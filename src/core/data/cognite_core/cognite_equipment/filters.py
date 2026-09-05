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
    from ..cognite_asset.filters import CogniteAssetFilter

    from ..cognite_equipment_type.filters import CogniteEquipmentTypeFilter

    from ..cognite_source_system.filters import CogniteSourceSystemFilter


CogniteEquipmentFilter = TypedDict(
    "CogniteEquipmentFilter",
    {
        "aliases": StringListFilter,
        "asset": "InstanceIdFilter | CogniteAssetFilter",
        "description": StringFilter,
        "equipmentType": "InstanceIdFilter | CogniteEquipmentTypeFilter",
        "externalId": StringFilter,
        "files": InstanceIdListFilter,
        "manufacturer": StringFilter,
        "name": StringFilter,
        "serialNumber": StringFilter,
        "source": "InstanceIdFilter | CogniteSourceSystemFilter",
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteEquipmentFilter]",
        "AND": "list[CogniteEquipmentFilter]",
        "NOT": "CogniteEquipmentFilter",
    },
    total=False,
)
