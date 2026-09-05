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


CogniteAnnotationFilter = TypedDict(
    "CogniteAnnotationFilter",
    {
        "aliases": StringListFilter,
        "confidence": FloatFilter,
        "description": StringFilter,
        "externalId": StringFilter,
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
        "OR": "list[CogniteAnnotationFilter]",
        "AND": "list[CogniteAnnotationFilter]",
        "NOT": "CogniteAnnotationFilter",
    },
    total=False,
)
