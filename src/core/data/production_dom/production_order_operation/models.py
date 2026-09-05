from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import ProductionOrderOperation


class ProductionOrderOperationAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "ProductionOrderOperation",
        "group_by_behavior": "NONE",
    }

    actual_quantity: float | None = None

    operation: InstanceId | None = None

    production_order: InstanceId | None = None

    quantity_uom: InstanceId | None = None

    scrap_quantity: float | None = None


__all__ = ["ProductionOrderOperation", "ProductionOrderOperationAggregation"]
