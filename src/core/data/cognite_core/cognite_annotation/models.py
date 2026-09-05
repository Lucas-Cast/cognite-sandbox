from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteAnnotation


class CogniteAnnotationAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteAnnotation",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    confidence: float | None = None


__all__ = ["CogniteAnnotation", "CogniteAnnotationAggregation"]
