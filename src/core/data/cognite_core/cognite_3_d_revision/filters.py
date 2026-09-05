from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..cognite_3_d_model.filters import Cognite3DModelFilter


Cognite3DRevisionFilter = TypedDict(
    "Cognite3DRevisionFilter",
    {
        "externalId": StringFilter,
        "model3D": "InstanceIdFilter | Cognite3DModelFilter",
        "published": BoolFilter,
        "space": StringFilter,
        "status": StringFilter,
        "type": StringFilter,
        "OR": "list[Cognite3DRevisionFilter]",
        "AND": "list[Cognite3DRevisionFilter]",
        "NOT": "Cognite3DRevisionFilter",
    },
    total=False,
)
