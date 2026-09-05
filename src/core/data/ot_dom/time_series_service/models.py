from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import TimeSeriesService


class TimeSeriesServiceAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "TimeSeriesService",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None


__all__ = ["TimeSeriesService", "TimeSeriesServiceAggregation"]
