from __future__ import annotations

import datetime
from typing import Any

from pydantic import Field

from industrial_model import InstanceId, WritableViewInstance


class Cognite360Image(WritableViewInstance):
    view_config = {"view_external_id": "Cognite360Image"}

    translation_x: float | None = None

    translation_y: float | None = None

    translation_z: float | None = None

    euler_rotation_x: float | None = None

    euler_rotation_y: float | None = None

    euler_rotation_z: float | None = None

    scale_x: float | None = None

    scale_y: float | None = None

    scale_z: float | None = None

    front: InstanceId | CogniteFile | None = None

    back: InstanceId | CogniteFile | None = None

    left: InstanceId | CogniteFile | None = None

    right: InstanceId | CogniteFile | None = None

    top: InstanceId | CogniteFile | None = None

    bottom: InstanceId | CogniteFile | None = None

    collection_360: InstanceId | Cognite360ImageCollection | None = None

    station_360: InstanceId | Cognite360ImageStation | None = None

    taken_at: datetime.datetime | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Cognite360ImageAnnotation(WritableViewInstance):
    view_config = {"view_external_id": "Cognite360ImageAnnotation"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    confidence: float | None = None

    status: str | None = None

    polygon: list[float] = Field(default_factory=list)

    format_version: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Cognite360ImageCollection(WritableViewInstance):
    view_config = {"view_external_id": "Cognite360ImageCollection"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    status: str | None = None

    published: bool | None = None

    type: str | None = None

    model_3_d: InstanceId | Cognite360ImageModel | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Cognite360ImageModel(WritableViewInstance):
    view_config = {"view_external_id": "Cognite360ImageModel"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    thumbnail: InstanceId | CogniteFile | None = None

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


class Cognite360ImageStation(WritableViewInstance):
    view_config = {"view_external_id": "Cognite360ImageStation"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    group_type: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Cognite3DModel(WritableViewInstance):
    view_config = {"view_external_id": "Cognite3DModel"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    thumbnail: InstanceId | CogniteFile | None = None

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


class Cognite3DObject(WritableViewInstance):
    view_config = {"view_external_id": "Cognite3DObject"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    x_min: float | None = None

    x_max: float | None = None

    y_min: float | None = None

    y_max: float | None = None

    z_min: float | None = None

    z_max: float | None = None

    asset: InstanceId | CogniteAsset | None = None

    images_360: list[InstanceId | Cognite360Image] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Cognite3DRevision(WritableViewInstance):
    view_config = {"view_external_id": "Cognite3DRevision"}

    status: str | None = None

    published: bool | None = None

    type: str | None = None

    model_3_d: InstanceId | Cognite3DModel | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class Cognite3DTransformation(WritableViewInstance):
    view_config = {"view_external_id": "Cognite3DTransformation"}

    translation_x: float | None = None

    translation_y: float | None = None

    translation_z: float | None = None

    euler_rotation_x: float | None = None

    euler_rotation_y: float | None = None

    euler_rotation_z: float | None = None

    scale_x: float | None = None

    scale_y: float | None = None

    scale_z: float | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteActivity(WritableViewInstance):
    view_config = {"view_external_id": "CogniteActivity"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    start_time: datetime.datetime | None = None

    end_time: datetime.datetime | None = None

    scheduled_start_time: datetime.datetime | None = None

    scheduled_end_time: datetime.datetime | None = None

    assets: list[InstanceId | CogniteAsset] = Field(default_factory=list)

    equipment: list[InstanceId | CogniteEquipment] = Field(default_factory=list)

    time_series: list[InstanceId | CogniteTimeSeries] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteAnnotation(WritableViewInstance):
    view_config = {"view_external_id": "CogniteAnnotation"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    confidence: float | None = None

    status: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteAsset(WritableViewInstance):
    view_config = {"view_external_id": "CogniteAsset"}

    object_3_d: InstanceId | Cognite3DObject | None = None

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    parent: InstanceId | CogniteAsset | None = None

    root: InstanceId | CogniteAsset | None = None

    path: list[InstanceId | CogniteAsset] = Field(default_factory=list)

    path_last_updated_time: datetime.datetime | None = None

    asset_class: InstanceId | CogniteAssetClass | None = None

    type: InstanceId | CogniteAssetType | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteAssetClass(WritableViewInstance):
    view_config = {"view_external_id": "CogniteAssetClass"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    code: str | None = None

    standard: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteAssetType(WritableViewInstance):
    view_config = {"view_external_id": "CogniteAssetType"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    code: str | None = None

    standard: str | None = None

    asset_class: InstanceId | CogniteAssetClass | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteCadModel(WritableViewInstance):
    view_config = {"view_external_id": "CogniteCADModel"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    thumbnail: InstanceId | CogniteFile | None = None

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


class CogniteCadNode(WritableViewInstance):
    view_config = {"view_external_id": "CogniteCADNode"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    object_3_d: InstanceId | Cognite3DObject | None = None

    model_3_d: InstanceId | CogniteCadModel | None = None

    cad_node_reference: str | None = None

    revisions: list[InstanceId | CogniteCadRevision] = Field(default_factory=list)

    tree_indexes: list[int] = Field(default_factory=list)

    sub_tree_sizes: list[int] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteCadRevision(WritableViewInstance):
    view_config = {"view_external_id": "CogniteCADRevision"}

    status: str | None = None

    published: bool | None = None

    type: str | None = None

    model_3_d: InstanceId | CogniteCadModel | None = None

    revision_id: int | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteCubeMap(WritableViewInstance):
    view_config = {"view_external_id": "CogniteCubeMap"}

    front: InstanceId | CogniteFile | None = None

    back: InstanceId | CogniteFile | None = None

    left: InstanceId | CogniteFile | None = None

    right: InstanceId | CogniteFile | None = None

    top: InstanceId | CogniteFile | None = None

    bottom: InstanceId | CogniteFile | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteDescribable(WritableViewInstance):
    view_config = {"view_external_id": "CogniteDescribable"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteDiagramAnnotation(WritableViewInstance):
    view_config = {"view_external_id": "CogniteDiagramAnnotation"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    confidence: float | None = None

    status: str | None = None

    start_node_page_number: int | None = None

    end_node_page_number: int | None = None

    start_node_x_min: float | None = None

    start_node_x_max: float | None = None

    start_node_y_min: float | None = None

    start_node_y_max: float | None = None

    start_node_text: str | None = None

    end_node_x_min: float | None = None

    end_node_x_max: float | None = None

    end_node_y_min: float | None = None

    end_node_y_max: float | None = None

    end_node_text: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteEquipment(WritableViewInstance):
    view_config = {"view_external_id": "CogniteEquipment"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    asset: InstanceId | CogniteAsset | None = None

    serial_number: str | None = None

    manufacturer: str | None = None

    equipment_type: InstanceId | CogniteEquipmentType | None = None

    files: list[InstanceId | CogniteFile] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteEquipmentType(WritableViewInstance):
    view_config = {"view_external_id": "CogniteEquipmentType"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    code: str | None = None

    equipment_class: str | None = None

    standard: str | None = None

    standard_reference: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteFile(WritableViewInstance):
    view_config = {"view_external_id": "CogniteFile"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    assets: list[InstanceId | CogniteAsset] = Field(default_factory=list)

    mime_type: str | None = None

    directory: str | None = None

    is_uploaded: bool | None = None

    uploaded_time: datetime.datetime | None = None

    category: InstanceId | CogniteFileCategory | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteFileCategory(WritableViewInstance):
    view_config = {"view_external_id": "CogniteFileCategory"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    code: str

    standard: str | None = None

    standard_reference: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CognitePointCloudModel(WritableViewInstance):
    view_config = {"view_external_id": "CognitePointCloudModel"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    thumbnail: InstanceId | CogniteFile | None = None

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


class CognitePointCloudRevision(WritableViewInstance):
    view_config = {"view_external_id": "CognitePointCloudRevision"}

    status: str | None = None

    published: bool | None = None

    type: str | None = None

    model_3_d: InstanceId | CognitePointCloudModel | None = None

    revision_id: int | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CognitePointCloudVolume(WritableViewInstance):
    view_config = {"view_external_id": "CognitePointCloudVolume"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    object_3_d: InstanceId | Cognite3DObject | None = None

    model_3_d: InstanceId | CogniteCadModel | None = None

    volume_references: list[str] = Field(default_factory=list)

    revisions: list[InstanceId | CogniteCadRevision] = Field(default_factory=list)

    volume_type: str | None = None

    volume: list[float] = Field(default_factory=list)

    format_version: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteSchedulable(WritableViewInstance):
    view_config = {"view_external_id": "CogniteSchedulable"}

    start_time: datetime.datetime | None = None

    end_time: datetime.datetime | None = None

    scheduled_start_time: datetime.datetime | None = None

    scheduled_end_time: datetime.datetime | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteSourceSystem(WritableViewInstance):
    view_config = {"view_external_id": "CogniteSourceSystem"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    version: str | None = None

    manufacturer: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteSourceable(WritableViewInstance):
    view_config = {"view_external_id": "CogniteSourceable"}

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteStateSet(WritableViewInstance):
    view_config = {"view_external_id": "CogniteStateSet"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    states: list[Any] = Field(default_factory=list)

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteTimeSeries(WritableViewInstance):
    view_config = {"view_external_id": "CogniteTimeSeries"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | CogniteSourceSystem | None = None

    source_created_time: datetime.datetime | None = None

    source_updated_time: datetime.datetime | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    is_step: bool

    type: str

    source_unit: str | None = None

    unit: InstanceId | CogniteUnit | None = None

    assets: list[InstanceId | CogniteAsset] = Field(default_factory=list)

    equipment: list[InstanceId | CogniteEquipment] = Field(default_factory=list)

    state_set: InstanceId | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteUnit(WritableViewInstance):
    view_config = {"view_external_id": "CogniteUnit"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    symbol: str | None = None

    quantity: str | None = None

    source: str | None = None

    source_reference: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class CogniteVisualizable(WritableViewInstance):
    view_config = {"view_external_id": "CogniteVisualizable"}

    object_3_d: InstanceId | Cognite3DObject | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )
