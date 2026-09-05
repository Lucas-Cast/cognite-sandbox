from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteVisualizable


class CogniteVisualizableAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteVisualizable",
        "group_by_behavior": "NONE",
    }

    object_3_d: InstanceId | None = None


__all__ = ["CogniteVisualizable", "CogniteVisualizableAggregation"]
