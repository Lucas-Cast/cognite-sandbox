from __future__ import annotations

from typing import Literal, TypeAlias

AreaQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "functionalLocation"
]
AreaGroupByProperty: TypeAlias = Literal[
    "name", "description", "class", "type", "functionalLocation", "plant", "site"
]
AreaAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "class",
    "type",
    "functionalLocation",
    "plant",
    "site",
]
AreaIncludeProperty: TypeAlias = Literal["plant", "site"]
