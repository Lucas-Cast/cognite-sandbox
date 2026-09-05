from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_3_d_object.filters import Cognite3DObjectFilter

    from ..cognite_cad_model.filters import CogniteCadModelFilter


CogniteCadNodeFilter = TypedDict(
    "CogniteCadNodeFilter",
    {
        "aliases": StringListFilter,
        "cadNodeReference": StringFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "model3D": "InstanceIdFilter | CogniteCadModelFilter",
        "name": StringFilter,
        "object3D": "InstanceIdFilter | Cognite3DObjectFilter",
        "revisions": InstanceIdListFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteCadNodeFilter]",
        "AND": "list[CogniteCadNodeFilter]",
        "NOT": "CogniteCadNodeFilter",
    },
    total=False,
)
