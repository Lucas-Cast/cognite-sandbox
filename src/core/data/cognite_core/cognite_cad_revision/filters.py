from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    InstanceIdFilter,
    IntFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..cognite_cad_model.filters import CogniteCadModelFilter


CogniteCadRevisionFilter = TypedDict(
    "CogniteCadRevisionFilter",
    {
        "externalId": StringFilter,
        "model3D": "InstanceIdFilter | CogniteCadModelFilter",
        "published": BoolFilter,
        "revisionId": IntFilter,
        "space": StringFilter,
        "status": StringFilter,
        "type": StringFilter,
        "OR": "list[CogniteCadRevisionFilter]",
        "AND": "list[CogniteCadRevisionFilter]",
        "NOT": "CogniteCadRevisionFilter",
    },
    total=False,
)
