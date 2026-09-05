from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import CogniteFileCategory


class CogniteFileCategoryAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteFileCategory",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    code: str | None = None

    standard: str | None = None

    standard_reference: str | None = None


__all__ = ["CogniteFileCategory", "CogniteFileCategoryAggregation"]
