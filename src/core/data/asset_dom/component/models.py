from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Component


class ComponentAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Component",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    material: InstanceId | None = None

    site_asset_tag: str | None = None


__all__ = ["Component", "ComponentAggregation"]
