from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import TimeSeriesSubservice


class TimeSeriesSubserviceAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "TimeSeriesSubservice",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    time_series_service: InstanceId | None = None


__all__ = ["TimeSeriesSubservice", "TimeSeriesSubserviceAggregation"]
