from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteCadModel


class CogniteCadModelAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteCADModel",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    thumbnail: InstanceId | None = None


__all__ = ["CogniteCadModel", "CogniteCadModelAggregation"]
