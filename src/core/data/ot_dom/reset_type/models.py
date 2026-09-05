from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import ResetType


class ResetTypeAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "ResetType",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None


__all__ = ["ResetType", "ResetTypeAggregation"]
