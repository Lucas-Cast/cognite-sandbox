from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteCadNode


class CogniteCadNodeAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteCADNode",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    object_3_d: InstanceId | None = None

    model_3_d: InstanceId | None = None

    cad_node_reference: str | None = None


__all__ = ["CogniteCadNode", "CogniteCadNodeAggregation"]
