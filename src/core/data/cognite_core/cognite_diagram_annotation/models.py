from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteDiagramAnnotation


class CogniteDiagramAnnotationAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteDiagramAnnotation",
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

    start_node_page_number: int | None = None

    end_node_page_number: int | None = None

    start_node_x_min: float | None = None

    start_node_x_max: float | None = None

    start_node_y_min: float | None = None

    start_node_y_max: float | None = None

    start_node_text: str | None = None

    end_node_x_min: float | None = None

    end_node_x_max: float | None = None

    end_node_y_min: float | None = None

    end_node_y_max: float | None = None

    end_node_text: str | None = None


__all__ = ["CogniteDiagramAnnotation", "CogniteDiagramAnnotationAggregation"]
