from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Routing


class RoutingAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Routing",
        "group_by_behavior": "NONE",
    }

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    number: str | None = None


__all__ = ["Routing", "RoutingAggregation"]
