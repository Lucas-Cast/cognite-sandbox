from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    BoolFilter,
    DatetimeFilter,
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_source_system.filters import CogniteSourceSystemFilter

    from ..cognite_unit.filters import CogniteUnitFilter


CogniteTimeSeriesFilter = TypedDict(
    "CogniteTimeSeriesFilter",
    {
        "aliases": StringListFilter,
        "assets": InstanceIdListFilter,
        "description": StringFilter,
        "equipment": InstanceIdListFilter,
        "externalId": StringFilter,
        "isStep": BoolFilter,
        "name": StringFilter,
        "source": "InstanceIdFilter | CogniteSourceSystemFilter",
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUnit": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "stateSet": InstanceIdFilter,
        "tags": StringListFilter,
        "type": StringFilter,
        "unit": "InstanceIdFilter | CogniteUnitFilter",
        "OR": "list[CogniteTimeSeriesFilter]",
        "AND": "list[CogniteTimeSeriesFilter]",
        "NOT": "CogniteTimeSeriesFilter",
    },
    total=False,
)
