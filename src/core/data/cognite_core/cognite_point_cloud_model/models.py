from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CognitePointCloudModel


class CognitePointCloudModelAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CognitePointCloudModel",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    thumbnail: InstanceId | None = None


__all__ = ["CognitePointCloudModel", "CognitePointCloudModelAggregation"]
