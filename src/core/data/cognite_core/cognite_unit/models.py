from __future__ import annotations


from industrial_model import AggregatedViewInstance

from ..models import CogniteUnit


class CogniteUnitAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteUnit",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    symbol: str | None = None

    quantity: str | None = None

    source: str | None = None

    source_reference: str | None = None


__all__ = ["CogniteUnit", "CogniteUnitAggregation"]
