from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Plant


class PlantAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Plant",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    code: str | None = None

    functional_location: str | None = None

    site: InstanceId | None = None

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None


__all__ = ["Plant", "PlantAggregation"]
