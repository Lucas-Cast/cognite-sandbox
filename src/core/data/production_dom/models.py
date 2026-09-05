from __future__ import annotations

import datetime

from pydantic import Field

from industrial_model import InstanceId, WritableViewInstance


class ProductionOrder(WritableViewInstance):
    view_config = {"view_external_id": "ProductionOrder"}

    actual_finish_date_time: datetime.datetime | None = None

    actual_quantity: float | None = None

    actual_scrap_quantity: float | None = None

    actual_start_date_time: datetime.datetime | None = None

    batch_number: str | None = None

    bom: InstanceId | None = None

    description: str | None = None

    line: InstanceId | None = None

    material: InstanceId | None = None

    order_creation_date: datetime.date | None = None

    order_number: str | None = None

    planned_quantity: float | None = None

    quantity_uom: InstanceId | None = None

    routing: InstanceId | Routing | None = None

    scheduled_finish_date_time: datetime.datetime | None = None

    scheduled_start_date_time: datetime.datetime | None = None

    site: InstanceId | None = None

    status: InstanceId | None = None

    type: InstanceId | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class ProductionOrderComponent(WritableViewInstance):
    view_config = {"view_external_id": "ProductionOrderComponent"}

    actual_consumed_quantity: float | None = None

    actual_scrap_quantity: float | None = None

    component: InstanceId | None = None

    is_bom_component: bool | None = Field(alias="isBOMComponent", default=None)

    order: InstanceId | ProductionOrder | None = None

    planned_consumed_quantity: float | None = None

    quantity_uom: InstanceId | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class ProductionOrderOperation(WritableViewInstance):
    view_config = {"view_external_id": "ProductionOrderOperation"}

    actual_quantity: float | None = None

    end_date_time: datetime.datetime | None = None

    operation: InstanceId | RoutingOperation | None = None

    production_order: InstanceId | ProductionOrder | None = None

    quantity_uom: InstanceId | None = None

    scrap_quantity: float | None = None

    start_date_time: datetime.datetime | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class ProductionOrderOutput(WritableViewInstance):
    view_config = {"view_external_id": "ProductionOrderOutput"}

    actual_quantity: float | None = None

    material: InstanceId | None = None

    production_order: InstanceId | ProductionOrder | None = None

    quantity_uom: InstanceId | None = None

    serial_number: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class ProductionOrderStatusChange(WritableViewInstance):
    view_config = {"view_external_id": "ProductionOrderStatusChange"}

    end_date_time: datetime.datetime | None = None

    production_order: InstanceId | ProductionOrder | None = None

    start_date_time: datetime.datetime | None = None

    status: InstanceId | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class ProductionOutput(WritableViewInstance):
    view_config = {"view_external_id": "ProductionOutput"}

    asset: InstanceId | None = None

    design_output: float | None = None

    material: InstanceId | None = None

    nominal_speed: float | None = None

    uom: InstanceId | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Routing(WritableViewInstance):
    view_config = {"view_external_id": "Routing"}

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    number: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class RoutingOperation(WritableViewInstance):
    view_config = {"view_external_id": "RoutingOperation"}

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    assets: list[InstanceId] = Field(default_factory=list)

    material: InstanceId | None = None

    operation_number: int | None = None

    routing: InstanceId | Routing | None = None

    sequence_group: int | None = None

    valid_from: datetime.date | None = None

    valid_to: datetime.date | None = None

    work_center: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )
