from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Unit


class UnitAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Unit",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    area: InstanceId | None = None

    functional_location: str | None = None

    location: InstanceId | None = None

    plant: InstanceId | None = None


__all__ = ["Unit", "UnitAggregation"]
