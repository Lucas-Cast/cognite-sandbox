from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import CogniteSourceSystem


class CogniteSourceSystemAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteSourceSystem",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    version: str | None = None

    manufacturer: str | None = None


__all__ = ["CogniteSourceSystem", "CogniteSourceSystemAggregation"]
