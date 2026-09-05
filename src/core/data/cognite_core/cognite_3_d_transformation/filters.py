from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    FloatFilter,
    StringFilter,
)


Cognite3DTransformationFilter = TypedDict(
    "Cognite3DTransformationFilter",
    {
        "eulerRotationX": FloatFilter,
        "eulerRotationY": FloatFilter,
        "eulerRotationZ": FloatFilter,
        "externalId": StringFilter,
        "scaleX": FloatFilter,
        "scaleY": FloatFilter,
        "scaleZ": FloatFilter,
        "space": StringFilter,
        "translationX": FloatFilter,
        "translationY": FloatFilter,
        "translationZ": FloatFilter,
        "OR": "list[Cognite3DTransformationFilter]",
        "AND": "list[Cognite3DTransformationFilter]",
        "NOT": "Cognite3DTransformationFilter",
    },
    total=False,
)
