from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CuratedTimeSeries


class CuratedTimeSeriesAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CuratedTimeSeries",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    is_step: bool | None = None

    source_unit: str | None = None

    unit: InstanceId | None = None

    state_set: InstanceId | None = None

    is_active: bool | None = None

    is_manual_input: bool | None = None

    max_value: float | None = None

    min_value: float | None = None

    scrap_reason: InstanceId | None = None

    target_value: float | None = None

    time_series_service: InstanceId | None = None

    time_series_subservice: InstanceId | None = None

    typical_value: float | None = None

    uom: InstanceId | None = None


__all__ = ["CuratedTimeSeries", "CuratedTimeSeriesAggregation"]
