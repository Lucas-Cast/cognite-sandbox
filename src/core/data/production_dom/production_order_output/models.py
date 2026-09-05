from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import ProductionOrderOutput


class ProductionOrderOutputAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "ProductionOrderOutput",
        "group_by_behavior": "NONE",
    }

    actual_quantity: float | None = None

    material: InstanceId | None = None

    production_order: InstanceId | None = None

    quantity_uom: InstanceId | None = None

    serial_number: str | None = None


__all__ = ["ProductionOrderOutput", "ProductionOrderOutputAggregation"]
