from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import DowntimeReason


class DowntimeReasonAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "DowntimeReason",
        "group_by_behavior": "NONE",
    }

    default_category: InstanceId | None = None

    default_subcategory: InstanceId | None = None

    description: str | None = None

    need_recontextualization: bool | None = None

    need_recontextualization_minutes: int | None = None

    reason_code: int | None = None

    related_asset: InstanceId | None = None

    related_asset_state: InstanceId | None = None

    time_series: InstanceId | None = None


__all__ = ["DowntimeReason", "DowntimeReasonAggregation"]
