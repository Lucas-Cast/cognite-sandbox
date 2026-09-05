from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Cognite3DModel


class Cognite3DModelAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Cognite3DModel",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    thumbnail: InstanceId | None = None


__all__ = ["Cognite3DModel", "Cognite3DModelAggregation"]
