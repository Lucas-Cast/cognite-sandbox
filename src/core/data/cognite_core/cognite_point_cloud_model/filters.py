from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_file.filters import CogniteFileFilter


CognitePointCloudModelFilter = TypedDict(
    "CognitePointCloudModelFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "thumbnail": "InstanceIdFilter | CogniteFileFilter",
        "type": StringFilter,
        "OR": "list[CognitePointCloudModelFilter]",
        "AND": "list[CognitePointCloudModelFilter]",
        "NOT": "CognitePointCloudModelFilter",
    },
    total=False,
)
