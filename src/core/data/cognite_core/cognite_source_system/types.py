from __future__ import annotations

from typing import Literal, TypeAlias

CogniteSourceSystemQueryProperty: TypeAlias = Literal[
    "name", "description", "tags", "aliases", "version", "manufacturer"
]
CogniteSourceSystemGroupByProperty: TypeAlias = Literal[
    "name", "description", "version", "manufacturer"
]
CogniteSourceSystemAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "version", "manufacturer"
]
CogniteSourceSystemIncludeProperty: TypeAlias = str
