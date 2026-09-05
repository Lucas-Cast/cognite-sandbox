from __future__ import annotations

from typing import Literal, TypeAlias

Cognite360ImageStationQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "groupType"
]
Cognite360ImageStationGroupByProperty: TypeAlias = Literal["name", "description"]
Cognite360ImageStationAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description"
]
Cognite360ImageStationIncludeProperty: TypeAlias = str
