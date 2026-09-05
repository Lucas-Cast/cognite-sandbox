from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..cognite_file.filters import CogniteFileFilter


CogniteCubeMapFilter = TypedDict(
    "CogniteCubeMapFilter",
    {
        "back": "InstanceIdFilter | CogniteFileFilter",
        "bottom": "InstanceIdFilter | CogniteFileFilter",
        "externalId": StringFilter,
        "front": "InstanceIdFilter | CogniteFileFilter",
        "left": "InstanceIdFilter | CogniteFileFilter",
        "right": "InstanceIdFilter | CogniteFileFilter",
        "space": StringFilter,
        "top": "InstanceIdFilter | CogniteFileFilter",
        "OR": "list[CogniteCubeMapFilter]",
        "AND": "list[CogniteCubeMapFilter]",
        "NOT": "CogniteCubeMapFilter",
    },
    total=False,
)
