from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import CogniteSchedulable


class CogniteSchedulableAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteSchedulable",
        "group_by_behavior": "NONE",
    }

    pass


__all__ = ["CogniteSchedulable", "CogniteSchedulableAggregation"]
