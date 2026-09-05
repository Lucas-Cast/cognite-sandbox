from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    FloatFilter,
    InstanceIdFilter,
    IntFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_source_system.filters import CogniteSourceSystemFilter


CogniteDiagramAnnotationFilter = TypedDict(
    "CogniteDiagramAnnotationFilter",
    {
        "aliases": StringListFilter,
        "confidence": FloatFilter,
        "description": StringFilter,
        "endNodePageNumber": IntFilter,
        "endNodeText": StringFilter,
        "endNodeXMax": FloatFilter,
        "endNodeXMin": FloatFilter,
        "endNodeYMax": FloatFilter,
        "endNodeYMin": FloatFilter,
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
        "startNodePageNumber": IntFilter,
        "startNodeText": StringFilter,
        "startNodeXMax": FloatFilter,
        "startNodeXMin": FloatFilter,
        "startNodeYMax": FloatFilter,
        "startNodeYMin": FloatFilter,
        "status": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteDiagramAnnotationFilter]",
        "AND": "list[CogniteDiagramAnnotationFilter]",
        "NOT": "CogniteDiagramAnnotationFilter",
    },
    total=False,
)
