from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteAsset


class CogniteAssetAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteAsset",
        "group_by_behavior": "NONE",
    }

    object_3_d: InstanceId | None = None

    name: str | None = None

    description: str | None = None

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    parent: InstanceId | None = None

    root: InstanceId | None = None

    asset_class: InstanceId | None = None

    type: InstanceId | None = None


__all__ = ["CogniteAsset", "CogniteAssetAggregation"]
