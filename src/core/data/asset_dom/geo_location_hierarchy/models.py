from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import GeoLocationHierarchy


class GeoLocationHierarchyAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "GeoLocationHierarchy",
        "group_by_behavior": "NONE",
    }

    class_: str | None = Field(alias="class", default=None)

    time_zone: InstanceId | None = None

    type: str | None = None


__all__ = ["GeoLocationHierarchy", "GeoLocationHierarchyAggregation"]
