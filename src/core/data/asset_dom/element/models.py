from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Element


class ElementAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Element",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    material: InstanceId | None = None

    site_asset_tag: str | None = None


__all__ = ["Element", "ElementAggregation"]
