from __future__ import annotations

from typing import Literal, TypeAlias

LineQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "functionalLocation", "workCenter"
]
LineGroupByProperty: TypeAlias = Literal[
    "name", "description", "class", "type", "functionalLocation", "location", "plant"
]
LineAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "class",
    "type",
    "functionalLocation",
    "location",
    "plant",
]
LineIncludeProperty: TypeAlias = Literal["location", "plant", "unit"]
