from __future__ import annotations

from typing import Literal, TypeAlias

CogniteFileQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "sourceId",
    "sourceContext",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "mimeType",
    "directory",
]
CogniteFileGroupByProperty: TypeAlias = Literal[
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "mimeType",
    "directory",
    "isUploaded",
    "category",
]
CogniteFileAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "name",
    "description",
    "sourceId",
    "sourceContext",
    "source",
    "sourceCreatedUser",
    "sourceUpdatedUser",
    "mimeType",
    "directory",
    "isUploaded",
    "category",
]
CogniteFileIncludeProperty: TypeAlias = Literal["source", "assets", "category"]
