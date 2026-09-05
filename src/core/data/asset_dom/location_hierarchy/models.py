from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import LocationHierarchy


class LocationHierarchyAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "LocationHierarchy",
        "group_by_behavior": "NONE",
    }

    class_: str | None = Field(alias="class", default=None)

    site: InstanceId | None = None

    type: str | None = None


__all__ = ["LocationHierarchy", "LocationHierarchyAggregation"]
