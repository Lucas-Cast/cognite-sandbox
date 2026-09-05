from __future__ import annotations

from typing import Literal, TypeAlias

Cognite3DTransformationQueryProperty: TypeAlias = str
Cognite3DTransformationGroupByProperty: TypeAlias = Literal[
    "translationX",
    "translationY",
    "translationZ",
    "eulerRotationX",
    "eulerRotationY",
    "eulerRotationZ",
    "scaleX",
    "scaleY",
    "scaleZ",
]
Cognite3DTransformationAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "translationX",
    "translationY",
    "translationZ",
    "eulerRotationX",
    "eulerRotationY",
    "eulerRotationZ",
    "scaleX",
    "scaleY",
    "scaleZ",
]
Cognite3DTransformationIncludeProperty: TypeAlias = str
