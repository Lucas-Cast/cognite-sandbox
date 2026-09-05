from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    InstanceIdFilter,
    StringFilter,
    StringListFilter,
)


if TYPE_CHECKING:
    from ..cognite_source_system.filters import CogniteSourceSystemFilter


CogniteStateSetFilter = TypedDict(
    "CogniteStateSetFilter",
    {
        "aliases": StringListFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "name": StringFilter,
        "source": "InstanceIdFilter | CogniteSourceSystemFilter",
        "sourceContext": StringFilter,
        "sourceCreatedTime": DatetimeFilter,
        "sourceCreatedUser": StringFilter,
        "sourceId": StringFilter,
        "sourceUpdatedTime": DatetimeFilter,
        "sourceUpdatedUser": StringFilter,
        "space": StringFilter,
        "tags": StringListFilter,
        "OR": "list[CogniteStateSetFilter]",
        "AND": "list[CogniteStateSetFilter]",
        "NOT": "CogniteStateSetFilter",
    },
    total=False,
)
