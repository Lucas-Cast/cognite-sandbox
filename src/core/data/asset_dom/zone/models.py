from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Zone


class ZoneAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Zone",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    functional_location: str | None = None

    is_botteneck_asset: bool | None = None

    is_production_output: bool | None = None

    site_asset_tag: str | None = None

    work_center: str | None = None


__all__ = ["Zone", "ZoneAggregation"]
