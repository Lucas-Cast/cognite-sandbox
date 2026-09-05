from __future__ import annotations

from typing import Literal, TypeAlias

CognitePointCloudVolumeQueryProperty: TypeAlias = Literal[
    "name",
    "description",
    "tags",
    "aliases",
    "volumeReferences",
    "volumeType",
    "formatVersion",
]
CognitePointCloudVolumeGroupByProperty: TypeAlias = Literal[
    "name", "description", "object3D", "model3D", "formatVersion"
]
CognitePointCloudVolumeAggregationProperty: TypeAlias = Literal[
    "externalId", "space", "name", "description", "object3D", "model3D", "formatVersion"
]
CognitePointCloudVolumeIncludeProperty: TypeAlias = Literal[
    "object3D", "model3D", "revisions"
]
