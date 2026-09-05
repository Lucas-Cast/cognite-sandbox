from __future__ import annotations

from typing import Literal, TypeAlias

CogniteSourceableQueryProperty: TypeAlias = Literal[
    "sourceId", "sourceContext", "sourceCreatedUser", "sourceUpdatedUser"
]
CogniteSourceableGroupByProperty: TypeAlias = Literal[
    "sourceId", "sourceContext", "source", "sourceCreatedUser", "sourceUpdatedUser"
]
CogniteSourceableAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
]
CogniteSourceableIncludeProperty: TypeAlias = Literal["source"]
