from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import ProductionOutput


class ProductionOutputAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "ProductionOutput",
        "group_by_behavior": "NONE",
    }

    asset: InstanceId | None = None

    design_output: float | None = None

    material: InstanceId | None = None

    nominal_speed: float | None = None

    uom: InstanceId | None = None


__all__ = ["ProductionOutput", "ProductionOutputAggregation"]
