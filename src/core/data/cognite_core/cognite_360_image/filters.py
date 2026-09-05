from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    FloatFilter,
    InstanceIdFilter,
    StringFilter,
)


if TYPE_CHECKING:
    from ..cognite_360_image_collection.filters import Cognite360ImageCollectionFilter

    from ..cognite_360_image_station.filters import Cognite360ImageStationFilter

    from ..cognite_file.filters import CogniteFileFilter


Cognite360ImageFilter = TypedDict(
    "Cognite360ImageFilter",
    {
        "back": "InstanceIdFilter | CogniteFileFilter",
        "bottom": "InstanceIdFilter | CogniteFileFilter",
        "collection360": "InstanceIdFilter | Cognite360ImageCollectionFilter",
        "eulerRotationX": FloatFilter,
        "eulerRotationY": FloatFilter,
        "eulerRotationZ": FloatFilter,
        "externalId": StringFilter,
        "front": "InstanceIdFilter | CogniteFileFilter",
        "left": "InstanceIdFilter | CogniteFileFilter",
        "right": "InstanceIdFilter | CogniteFileFilter",
        "scaleX": FloatFilter,
        "scaleY": FloatFilter,
        "scaleZ": FloatFilter,
        "space": StringFilter,
        "station360": "InstanceIdFilter | Cognite360ImageStationFilter",
        "takenAt": DatetimeFilter,
        "top": "InstanceIdFilter | CogniteFileFilter",
        "translationX": FloatFilter,
        "translationY": FloatFilter,
        "translationZ": FloatFilter,
        "OR": "list[Cognite360ImageFilter]",
        "AND": "list[Cognite360ImageFilter]",
        "NOT": "Cognite360ImageFilter",
    },
    total=False,
)
