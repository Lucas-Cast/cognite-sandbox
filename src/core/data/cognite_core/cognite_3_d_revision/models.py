from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Cognite3DRevision


class Cognite3DRevisionAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Cognite3DRevision",
        "group_by_behavior": "NONE",
    }

    published: bool | None = None

    model_3_d: InstanceId | None = None


__all__ = ["Cognite3DRevision", "Cognite3DRevisionAggregation"]
