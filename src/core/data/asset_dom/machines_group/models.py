from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import MachinesGroup


class MachinesGroupAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "MachinesGroup",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    location: InstanceId | None = None

    plant: InstanceId | None = None


__all__ = ["MachinesGroup", "MachinesGroupAggregation"]
