from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..cognite_3_d_object.filters import Cognite3DObjectFilter


CogniteVisualizableFilter = TypedDict(
    "CogniteVisualizableFilter",
    {
        "externalId": StringFilter,
        "object3D": "InstanceIdFilter | Cognite3DObjectFilter",
        "space": StringFilter,
        "OR": "list[CogniteVisualizableFilter]",
        "AND": "list[CogniteVisualizableFilter]",
        "NOT": "CogniteVisualizableFilter",
    },
    total=False,
)
