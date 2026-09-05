from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CuratedTimeSeriesMapping


class CuratedTimeSeriesMappingAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CuratedTimeSeriesMapping",
        "group_by_behavior": "NONE",
    }

    curated_time_series: InstanceId | None = None

    output_description: str | None = None

    output_value: float | None = None

    raw_time_series: InstanceId | None = None

    rule: int | None = None


__all__ = ["CuratedTimeSeriesMapping", "CuratedTimeSeriesMappingAggregation"]
