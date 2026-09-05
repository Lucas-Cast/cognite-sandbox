from __future__ import annotations


from pydantic import Field

from industrial_model import AggregatedViewInstance, InstanceId

from ..models import ProductionOrderComponent


class ProductionOrderComponentAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "ProductionOrderComponent",
        "group_by_behavior": "NONE",
    }

    actual_consumed_quantity: float | None = None

    actual_scrap_quantity: float | None = None

    component: InstanceId | None = None

    is_bom_component: bool | None = Field(alias="isBOMComponent", default=None)

    order: InstanceId | None = None

    planned_consumed_quantity: float | None = None

    quantity_uom: InstanceId | None = None


__all__ = ["ProductionOrderComponent", "ProductionOrderComponentAggregation"]
