from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import ScrapReason


class ScrapReasonAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "ScrapReason",
        "group_by_behavior": "NONE",
    }

    code: str | None = None

    description: str | None = None


__all__ = ["ScrapReason", "ScrapReasonAggregation"]
