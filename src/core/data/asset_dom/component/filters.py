from __future__ import annotations

from typing import TypedDict

from industrial_model.queries.filter_types import (
    InstanceIdFilter,
    InstanceIdListFilter,
    StringFilter,
    StringListFilter,
)


ComponentFilter = TypedDict(
    "ComponentFilter",
    {
        "aliases": StringListFilter,
        "class": InstanceIdFilter,
        "description": StringFilter,
        "externalId": StringFilter,
        "material": InstanceIdFilter,
        "name": StringFilter,
        "siteAssetTag": StringFilter,
        "space": StringFilter,
        "subsystem": InstanceIdListFilter,
        "tags": StringListFilter,
        "type": InstanceIdFilter,
        "OR": "list[ComponentFilter]",
        "AND": "list[ComponentFilter]",
        "NOT": "ComponentFilter",
    },
    total=False,
)
