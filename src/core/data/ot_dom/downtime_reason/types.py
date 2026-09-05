from __future__ import annotations

from typing import Literal, TypeAlias

DowntimeReasonQueryProperty: TypeAlias = Literal["description"]
DowntimeReasonGroupByProperty: TypeAlias = Literal[
    "defaultCategory",
    "defaultSubcategory",
    "description",
    "needRecontextualization",
    "needRecontextualizationMinutes",
    "reasonCode",
    "relatedAsset",
    "relatedAssetState",
    "timeSeries",
]
DowntimeReasonAggregationProperty: TypeAlias = Literal[
    "externalId",
    "space",
    "defaultCategory",
    "defaultSubcategory",
    "description",
    "needRecontextualization",
    "needRecontextualizationMinutes",
    "reasonCode",
    "relatedAsset",
    "relatedAssetState",
    "timeSeries",
]
DowntimeReasonIncludeProperty: TypeAlias = Literal["timeSeries"]
