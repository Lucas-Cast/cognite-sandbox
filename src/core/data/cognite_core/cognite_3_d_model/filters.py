from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_file.filters import CogniteFileFilter


Cognite3DModelFilter = TypedDict(
    "Cognite3DModelFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "thumbnail": "InstanceIdFilter | CogniteFileFilter",
        "type": StringFilter,
        "OR": "list[Cognite3DModelFilter]",
        "AND": "list[Cognite3DModelFilter]",
        "NOT": "Cognite3DModelFilter",
    },
    total=False,
)
