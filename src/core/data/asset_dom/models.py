from __future__ import annotations

import datetime

from pydantic import Field

from industrial_model import InstanceId, WritableViewInstance


class Area(WritableViewInstance):
    view_config = {"view_external_id": "Area"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    functional_location: str | None = None

    plant: InstanceId | Plant | None = None

    site: InstanceId | Site | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Component(WritableViewInstance):
    view_config = {"view_external_id": "Component"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    material: InstanceId | None = None

    site_asset_tag: str | None = None

    subsystem: list[InstanceId | Subsystem] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Element(WritableViewInstance):
    view_config = {"view_external_id": "Element"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    component: list[InstanceId | Component] = Field(default_factory=list)

    material: InstanceId | None = None

    site_asset_tag: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class GeoLocationHierarchy(WritableViewInstance):
    view_config = {"view_external_id": "GeoLocationHierarchy"}

    class_: str | None = Field(alias="class", default=None)

    time_zone: InstanceId | None = None

    type: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Line(WritableViewInstance):
    view_config = {"view_external_id": "Line"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    business_unit: list[InstanceId] = Field(default_factory=list)

    functional_location: str | None = None

    location: InstanceId | LocationHierarchy | None = None

    plant: InstanceId | Plant | None = None

    product: list[InstanceId] = Field(default_factory=list)

    unit: list[InstanceId | Unit] = Field(default_factory=list)

    work_center: list[str] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class LocationHierarchy(WritableViewInstance):
    view_config = {"view_external_id": "LocationHierarchy"}

    class_: str | None = Field(alias="class", default=None)

    site: InstanceId | Site | None = None

    type: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Machine(WritableViewInstance):
    view_config = {"view_external_id": "Machine"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    business_unit: list[InstanceId] = Field(default_factory=list)

    is_botteneck_asset: bool | None = None

    is_production_output: bool | None = None

    line: list[InstanceId | Line] = Field(default_factory=list)

    location: InstanceId | LocationHierarchy | None = None

    site_asset_tag: str | None = None

    work_center: list[str] = Field(default_factory=list)

    zone: list[InstanceId | Zone] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class MachinesGroup(WritableViewInstance):
    view_config = {"view_external_id": "MachinesGroup"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    business_unit: list[InstanceId] = Field(default_factory=list)

    location: InstanceId | LocationHierarchy | None = None

    plant: InstanceId | Plant | None = None

    product: list[InstanceId] = Field(default_factory=list)

    unit: list[InstanceId | Unit] = Field(default_factory=list)

    work_center: list[str] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Plant(WritableViewInstance):
    view_config = {"view_external_id": "Plant"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    code: str | None = None

    functional_location: str | None = None

    site: InstanceId | Site | None = None

    class_: InstanceId | None = Field(alias="class", default=None)

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


class Site(WritableViewInstance):
    view_config = {"view_external_id": "Site"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    business_unit: list[InstanceId] = Field(default_factory=list)

    city: InstanceId | GeoLocationHierarchy | None = None

    code: str | None = None

    siam_code: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Subsystem(WritableViewInstance):
    view_config = {"view_external_id": "Subsystem"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    site_asset_tag: str | None = None

    system: list[InstanceId | System] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class System(WritableViewInstance):
    view_config = {"view_external_id": "System"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    is_production_output: bool | None = None

    machine: list[InstanceId | Machine] = Field(default_factory=list)

    site_asset_tag: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Unit(WritableViewInstance):
    view_config = {"view_external_id": "Unit"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    area: InstanceId | Area | None = None

    functional_location: str | None = None

    location: InstanceId | LocationHierarchy | None = None

    plant: InstanceId | Plant | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Zone(WritableViewInstance):
    view_config = {"view_external_id": "Zone"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    class_: InstanceId | None = Field(alias="class", default=None)

    type: InstanceId | None = None

    functional_location: str | None = None

    is_botteneck_asset: bool | None = None

    is_production_output: bool | None = None

    line: list[InstanceId | Line] = Field(default_factory=list)

    site_asset_tag: str | None = None

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
