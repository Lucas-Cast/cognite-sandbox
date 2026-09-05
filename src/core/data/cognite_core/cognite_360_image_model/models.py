from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Cognite360ImageModel


class Cognite360ImageModelAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Cognite360ImageModel",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    thumbnail: InstanceId | None = None


__all__ = ["Cognite360ImageModel", "Cognite360ImageModelAggregation"]
