from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Cognite360ImageCollection


class Cognite360ImageCollectionAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Cognite360ImageCollection",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    published: bool | None = None

    model_3_d: InstanceId | None = None


__all__ = ["Cognite360ImageCollection", "Cognite360ImageCollectionAggregation"]
