from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteAssetType


class CogniteAssetTypeAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteAssetType",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    code: str | None = None

    standard: str | None = None

    asset_class: InstanceId | None = None


__all__ = ["CogniteAssetType", "CogniteAssetTypeAggregation"]
