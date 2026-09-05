from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    FloatFilter,
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_source_system.filters import CogniteSourceSystemFilter


Cognite360ImageAnnotationFilter = TypedDict(
    "Cognite360ImageAnnotationFilter",
    {
        "aliases": StringListFilter,
        "confidence": FloatFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "formatVersion": StringFilter,
        "name": StringFilter,
        "source": "InstanceIdFilter | CogniteSourceSystemFilter",
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "status": StringFilter,
        "tags": StringListFilter,
        "OR": "list[Cognite360ImageAnnotationFilter]",
        "AND": "list[Cognite360ImageAnnotationFilter]",
        "NOT": "Cognite360ImageAnnotationFilter",
    },
    total=False,
)
