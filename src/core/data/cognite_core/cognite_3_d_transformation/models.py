from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import Cognite3DTransformation


class Cognite3DTransformationAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Cognite3DTransformation",
        "group_by_behavior": "NONE",
    }

    translation_x: float | None = None

    translation_y: float | None = None

    translation_z: float | None = None

    euler_rotation_x: float | None = None

    euler_rotation_y: float | None = None

    euler_rotation_z: float | None = None

    scale_x: float | None = None

    scale_y: float | None = None

    scale_z: float | None = None


__all__ = ["Cognite3DTransformation", "Cognite3DTransformationAggregation"]
