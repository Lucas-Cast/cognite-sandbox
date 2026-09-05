from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteTimeSeries


class CogniteTimeSeriesAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteTimeSeries",
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


__all__ = ["CogniteTimeSeries", "CogniteTimeSeriesAggregation"]
