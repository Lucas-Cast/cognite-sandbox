from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import CogniteAssetClass


class CogniteAssetClassAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteAssetClass",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    code: str | None = None

    standard: str | None = None


__all__ = ["CogniteAssetClass", "CogniteAssetClassAggregation"]
