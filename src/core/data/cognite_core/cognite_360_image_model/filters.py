from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_file.filters import CogniteFileFilter


Cognite360ImageModelFilter = TypedDict(
    "Cognite360ImageModelFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "thumbnail": "InstanceIdFilter | CogniteFileFilter",
        "type": StringFilter,
        "OR": "list[Cognite360ImageModelFilter]",
        "AND": "list[Cognite360ImageModelFilter]",
        "NOT": "Cognite360ImageModelFilter",
    },
    total=False,
)
