from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteEquipment


class CogniteEquipmentAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteEquipment",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    asset: InstanceId | None = None

    serial_number: str | None = None

    manufacturer: str | None = None

    equipment_type: InstanceId | None = None


__all__ = ["CogniteEquipment", "CogniteEquipmentAggregation"]
