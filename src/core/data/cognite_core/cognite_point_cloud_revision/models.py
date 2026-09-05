from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CognitePointCloudRevision


class CognitePointCloudRevisionAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CognitePointCloudRevision",
        "group_by_behavior": "NONE",
    }

    published: bool | None = None

    model_3_d: InstanceId | None = None

    revision_id: int | None = None


__all__ = ["CognitePointCloudRevision", "CognitePointCloudRevisionAggregation"]
