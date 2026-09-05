from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import ProductionOrder


class ProductionOrderAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "ProductionOrder",
        "group_by_behavior": "NONE",
    }

    actual_quantity: float | None = None

    actual_scrap_quantity: float | None = None

    batch_number: str | None = None

    bom: InstanceId | None = None

    description: str | None = None

    line: InstanceId | None = None

    material: InstanceId | None = None

    order_number: str | None = None

    planned_quantity: float | None = None

    quantity_uom: InstanceId | None = None

    routing: InstanceId | None = None

    site: InstanceId | None = None

    status: InstanceId | None = None

    type: InstanceId | None = None


__all__ = ["ProductionOrder", "ProductionOrderAggregation"]
