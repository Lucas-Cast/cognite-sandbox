from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteSourceable


class CogniteSourceableAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteSourceable",
        "group_by_behavior": "NONE",
    }

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None


__all__ = ["CogniteSourceable", "CogniteSourceableAggregation"]
