from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import Cognite3DObject


class Cognite3DObjectAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Cognite3DObject",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    x_min: float | None = None

    x_max: float | None = None

    y_min: float | None = None

    y_max: float | None = None

    z_min: float | None = None

    z_max: float | None = None


__all__ = ["Cognite3DObject", "Cognite3DObjectAggregation"]
