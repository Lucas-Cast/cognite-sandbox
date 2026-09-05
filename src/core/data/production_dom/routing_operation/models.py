from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import RoutingOperation


class RoutingOperationAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "RoutingOperation",
        "group_by_behavior": "NONE",
    }

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    material: InstanceId | None = None

    operation_number: int | None = None

    routing: InstanceId | None = None

    sequence_group: int | None = None

    work_center: str | None = None


__all__ = ["RoutingOperation", "RoutingOperationAggregation"]
