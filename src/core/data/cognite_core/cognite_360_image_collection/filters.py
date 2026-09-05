from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_360_image_model.filters import Cognite360ImageModelFilter


Cognite360ImageCollectionFilter = TypedDict(
    "Cognite360ImageCollectionFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "model3D": "InstanceIdFilter | Cognite360ImageModelFilter",
        "name": StringFilter,
        "published": BoolFilter,
        "space": StringFilter,
        "status": StringFilter,
        "tags": StringListFilter,
        "type": StringFilter,
        "OR": "list[Cognite360ImageCollectionFilter]",
        "AND": "list[Cognite360ImageCollectionFilter]",
        "NOT": "Cognite360ImageCollectionFilter",
    },
    total=False,
)
