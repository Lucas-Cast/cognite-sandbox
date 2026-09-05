from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteStateSet


class CogniteStateSetAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteStateSet",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None


__all__ = ["CogniteStateSet", "CogniteStateSetAggregation"]
