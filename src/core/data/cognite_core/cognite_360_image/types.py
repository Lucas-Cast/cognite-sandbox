from __future__ import annotations

from typing import Literal, TypeAlias

Cognite360ImageQueryProperty: TypeAlias = str
Cognite360ImageGroupByProperty: TypeAlias = Literal[
    "translationX",
    "translationY",
    "translationZ",
    "eulerRotationX",
    "eulerRotationY",
    "eulerRotationZ",
    "scaleX",
    "scaleY",
    "scaleZ",
    "front",
    "back",
    "left",
    "right",
    "top",
    "bottom",
    "collection360",
    "station360",
]
Cognite360ImageAggregationProperty: TypeAlias = Literal[
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
    "front",
    "back",
    "left",
    "right",
    "top",
    "bottom",
    "collection360",
    "station360",
]
Cognite360ImageIncludeProperty: TypeAlias = Literal[
    "front", "back", "left", "right", "top", "bottom", "collection360", "station360"
]
