from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CognitePointCloudVolume


class CognitePointCloudVolumeAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CognitePointCloudVolume",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    object_3_d: InstanceId | None = None

    model_3_d: InstanceId | None = None

    format_version: str | None = None


__all__ = ["CognitePointCloudVolume", "CognitePointCloudVolumeAggregation"]
