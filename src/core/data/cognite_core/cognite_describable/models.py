from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import CogniteDescribable


class CogniteDescribableAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteDescribable",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None


__all__ = ["CogniteDescribable", "CogniteDescribableAggregation"]
