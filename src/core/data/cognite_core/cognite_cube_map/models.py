from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteCubeMap


class CogniteCubeMapAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteCubeMap",
        "group_by_behavior": "NONE",
    }

    front: InstanceId | None = None

    back: InstanceId | None = None

    left: InstanceId | None = None

    right: InstanceId | None = None

    top: InstanceId | None = None

    bottom: InstanceId | None = None


__all__ = ["CogniteCubeMap", "CogniteCubeMapAggregation"]
