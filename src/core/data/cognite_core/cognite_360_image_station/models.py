from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import Cognite360ImageStation


class Cognite360ImageStationAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Cognite360ImageStation",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None


__all__ = ["Cognite360ImageStation", "Cognite360ImageStationAggregation"]
