from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import ProductionOrderStatusChange


class ProductionOrderStatusChangeAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "ProductionOrderStatusChange",
        "group_by_behavior": "NONE",
    }

    production_order: InstanceId | None = None

    status: InstanceId | None = None


__all__ = ["ProductionOrderStatusChange", "ProductionOrderStatusChangeAggregation"]
