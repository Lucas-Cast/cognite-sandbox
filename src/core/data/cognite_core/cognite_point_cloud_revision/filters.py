from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    InstanceIdFilter,
    IntFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..cognite_point_cloud_model.filters import CognitePointCloudModelFilter


CognitePointCloudRevisionFilter = TypedDict(
    "CognitePointCloudRevisionFilter",
    {
        "externalId": StringFilter,
        "model3D": "InstanceIdFilter | CognitePointCloudModelFilter",
        "published": BoolFilter,
        "revisionId": IntFilter,
        "space": StringFilter,
        "status": StringFilter,
        "type": StringFilter,
        "OR": "list[CognitePointCloudRevisionFilter]",
        "AND": "list[CognitePointCloudRevisionFilter]",
        "NOT": "CognitePointCloudRevisionFilter",
    },
    total=False,
)
