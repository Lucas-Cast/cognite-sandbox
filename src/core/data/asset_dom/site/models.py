from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Site


class SiteAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Site",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    city: InstanceId | None = None

    code: str | None = None

    siam_code: str | None = None


__all__ = ["Site", "SiteAggregation"]
