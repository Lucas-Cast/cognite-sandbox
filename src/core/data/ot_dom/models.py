from __future__ import annotations

import datetime
from typing import Any

from pydantic import Field

from industrial_model import InstanceId, WritableViewInstance


class CuratedTimeSeries(WritableViewInstance):
    view_config = {"view_external_id": "CuratedTimeSeries"}

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

    is_step: bool

    type: str

    source_unit: str | None = None

    unit: InstanceId | None = None

    assets: list[InstanceId] = Field(default_factory=list)

    equipment: list[InstanceId] = Field(default_factory=list)

    state_set: InstanceId | None = None

    input_tags: list[InstanceId | RawTimeSeries] = Field(default_factory=list)

    is_active: bool | None = None

    is_manual_input: bool | None = None

    max_value: float | None = None

    min_value: float | None = None

    scrap_reason: InstanceId | ScrapReason | None = None

    target_value: float | None = None

    time_series_service: InstanceId | TimeSeriesService | None = None

    time_series_subservice: InstanceId | TimeSeriesSubservice | None = None

    typical_value: float | None = None

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


class CuratedTimeSeriesMapping(WritableViewInstance):
    view_config = {"view_external_id": "CuratedTimeSeriesMapping"}

    curated_time_series: InstanceId | CuratedTimeSeries | None = None

    input_data_type: str | None = None

    output_description: str | None = None

    output_value: float | None = None

    raw_time_series: InstanceId | RawTimeSeries | None = None

    rule: int | None = None

    rule_condition: Any | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class DowntimeReason(WritableViewInstance):
    view_config = {"view_external_id": "DowntimeReason"}

    default_category: InstanceId | None = None

    default_subcategory: InstanceId | None = None

    description: str | None = None

    need_recontextualization: bool | None = None

    need_recontextualization_minutes: int | None = None

    reason_code: int | None = None

    related_asset: InstanceId | None = None

    related_asset_state: InstanceId | None = None

    time_series: InstanceId | RawTimeSeries | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class RawTimeSeries(WritableViewInstance):
    view_config = {"view_external_id": "RawTimeSeries"}

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

    is_step: bool

    type: str

    source_unit: str | None = None

    unit: InstanceId | None = None

    assets: list[InstanceId] = Field(default_factory=list)

    equipment: list[InstanceId] = Field(default_factory=list)

    state_set: InstanceId | None = None

    counter_max_delta: int | None = None

    counter_roll_over: int | None = None

    is_active: bool | None = None

    is_manual_input: bool | None = None

    max_value: float | None = None

    min_value: float | None = None

    reset_type: InstanceId | ResetType | None = None

    scrap_reason: InstanceId | ScrapReason | None = None

    source_metadata: Any | None = None

    target_value: float | None = None

    time_series_service: InstanceId | TimeSeriesService | None = None

    time_series_subservice: InstanceId | TimeSeriesSubservice | None = None

    typical_value: float | None = None

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


class ResetType(WritableViewInstance):
    view_config = {"view_external_id": "ResetType"}

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


class ScrapReason(WritableViewInstance):
    view_config = {"view_external_id": "ScrapReason"}

    code: str | None = None

    description: str | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )


class TimeSeriesService(WritableViewInstance):
    view_config = {"view_external_id": "TimeSeriesService"}

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


class TimeSeriesSubservice(WritableViewInstance):
    view_config = {"view_external_id": "TimeSeriesSubservice"}

    name: str | None = None

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    aliases: list[str] = Field(default_factory=list)

    time_series_service: InstanceId | TimeSeriesService | None = None

    def edge_id_factory(
        self, target_node: InstanceId, edge_type: InstanceId
    ) -> InstanceId:
        return InstanceId(
            external_id=(
                f"{self.external_id}-{target_node.external_id}-{edge_type.external_id}"
            ),
            space=self.space,
        )
