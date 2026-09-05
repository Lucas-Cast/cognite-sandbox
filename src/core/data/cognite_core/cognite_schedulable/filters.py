from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    DatetimeFilter,
    StringFilter,
)


CogniteSchedulableFilter = TypedDict(
    "CogniteSchedulableFilter",
    {
        "endTime": DatetimeFilter,
        "externalId": StringFilter,
        "scheduledEndTime": DatetimeFilter,
        "scheduledStartTime": DatetimeFilter,
        "space": StringFilter,
        "startTime": DatetimeFilter,
        "OR": "list[CogniteSchedulableFilter]",
        "AND": "list[CogniteSchedulableFilter]",
        "NOT": "CogniteSchedulableFilter",
    },
    total=False,
)
