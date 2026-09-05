from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_source_system.filters import CogniteSourceSystemFilter


CogniteActivityFilter = TypedDict(
    "CogniteActivityFilter",
    {
        "aliases": StringListFilter,
        "assets": InstanceIdListFilter,
        "description": StringFilter,
        "endTime": DatetimeFilter,
        "equipment": InstanceIdListFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "scheduledEndTime": DatetimeFilter,
        "scheduledStartTime": DatetimeFilter,
        "source": "InstanceIdFilter | CogniteSourceSystemFilter",
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "startTime": DatetimeFilter,
        "tags": StringListFilter,
        "timeSeries": InstanceIdListFilter,
        "OR": "list[CogniteActivityFilter]",
        "AND": "list[CogniteActivityFilter]",
        "NOT": "CogniteActivityFilter",
    },
    total=False,
)
