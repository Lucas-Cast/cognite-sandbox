from __future__ import annotations


from industrial_model import AggregatedViewInstance, InstanceId

from ..models import CogniteFile


class CogniteFileAggregation(AggregatedViewInstance):
    view_config = {
        "view_external_id": "CogniteFile",
        "group_by_behavior": "NONE",
    }

    name: str | None = None

    description: str | None = None

    source_id: str | None = None

    source_context: str | None = None

    source: InstanceId | None = None

    source_created_user: str | None = None

    source_updated_user: str | None = None

    mime_type: str | None = None

    directory: str | None = None

    is_uploaded: bool | None = None

    category: InstanceId | None = None


__all__ = ["CogniteFile", "CogniteFileAggregation"]
