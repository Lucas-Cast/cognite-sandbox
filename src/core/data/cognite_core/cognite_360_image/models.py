from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import Cognite360Image


class Cognite360ImageAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "Cognite360Image",
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

    front: InstanceId | None = None

    back: InstanceId | None = None

    left: InstanceId | None = None

    right: InstanceId | None = None

    top: InstanceId | None = None

    bottom: InstanceId | None = None

    collection_360: InstanceId | None = None

    station_360: InstanceId | None = None


__all__ = ["Cognite360Image", "Cognite360ImageAggregation"]
