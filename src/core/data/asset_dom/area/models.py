from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Area


class AreaAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Area",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    functional_location: str | None = None

    plant: InstanceId | None = None

    site: InstanceId | None = None


__all__ = ["Area", "AreaAggregation"]
