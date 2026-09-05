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
    from ..cognite_file_category.filters import CogniteFileCategoryFilter

    from ..cognite_source_system.filters import CogniteSourceSystemFilter


CogniteFileFilter = TypedDict(
    "CogniteFileFilter",
    {
        "aliases": StringListFilter,
        "assets": InstanceIdListFilter,
        "category": "InstanceIdFilter | CogniteFileCategoryFilter",
        "description": StringFilter,
        "directory": StringFilter,
        "externalId": StringFilter,
        "isUploaded": BoolFilter,
        "mimeType": StringFilter,
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
        "uploadedTime": DatetimeFilter,
        "OR": "list[CogniteFileFilter]",
        "AND": "list[CogniteFileFilter]",
        "NOT": "CogniteFileFilter",
    },
    total=False,
)
